from .config import config
from .db import TableBase, column_windows
from sqlalchemy import Column, Date, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import *
import zlib
import math

class SearchItemStatus:
    new = 'new'
    retry = 'retry'
    canceled = 'canceled'
    failed = 'failed'
    timeout_split = 'timeout-split'
    completed = 'completed'

class SearchItemResult(TableBase):
    __tablename__ = 'query_results'

    id = Column(Integer, primary_key=True)
    search_id = Column(String, ForeignKey('queue.id'))
    nresults = Column(Integer)
    timestamp = Column(DateTime)
    query_seconds = Column(Integer)

    # search_item = relationship('SearchItem', back_populates='results')

    __table_args__ = (UniqueConstraint('search_id', 'timestamp', name='_search_id_timestamp_uc'),
                     )

    def __init__(self, search_id, nresults, timestamp, query_seconds):
        super().__init__(
            search_id = search_id,
            nresults = nresults,
            timestamp = timestamp,
            query_seconds = query_seconds
        )

def clear_queue(db):
    db.execute(
        SearchItem.__table__.update().where(SearchItem.status.in_([SearchItemStatus.new,SearchItemStatus.retry])).values(status=SearchItemStatus.canceled)
    )

def active_items(db, filter=None):
    q = db.query(SearchItem).filter(SearchItem.status.in_([SearchItemStatus.new,SearchItemStatus.retry]))
    if filter:
        q = q.filter(filter)
    return q

def active_count(db, filter=None):
    return active_items(db, filter).count()

def failed_items(db, filter=None):
    q = db.query(SearchItem).filter(SearchItem.status == SearchItemStatus.failed)
    if filter:
        q = q.filter(filter)
    return q

def failed_count(db, filter=None):
    return failed_items(db, filter).count()

def split_date_range(start_date, end_date):
    assert(end_date)
    assert(end_date > start_date)
    days_diff = (end_date - start_date).days
    if days_diff == 1:
        range1 = [start_date, None]
        range2 = [end_date, None]
    elif days_diff == 2:
        range1 = [start_date, start_date + timedelta(1)]
        range2 = [end_date, None]
    else:
        range1 = [start_date, start_date + timedelta(int(days_diff / 2))]
        range2 = [start_date + timedelta(math.ceil((days_diff + 1) / 2)), end_date]
    return range1, range2

class SearchItem(TableBase):
    __tablename__ = 'queue'

    id = Column(String, primary_key=True)
    search_string = Column(String)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    court = Column(String, nullable=True)
    status = Column(String, default=SearchItemStatus.new)
    timeouts = Column(Integer, default=0)
    err500s = Column(Integer, default=0)
    errunknown = Column(String, nullable=True)

    # results = relationship('SearchItemResult', back_populates='search_item')

    def __init__(self, search_string, start_date, end_date=None, court=None, status=SearchItemStatus.new):
        id = search_string + start_date.strftime("%-m/%-d/%Y")
        if end_date:
            id += end_date.strftime("%-m/%-d/%Y")
        if court:
            id += court
        super().__init__(
            id=id,
            search_string=search_string,
            start_date=start_date,
            end_date=end_date,
            court=court,
            status=status,
            timeouts = 0,
            err500s = 0
        )

    def dict(self):
        return {
            'id': self.id,
            'search_string': self.search_string,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'court': self.court,
            'status': self.status,
            'timeouts': self.timeouts,
            'err500s': self.err500s,
            'errunknown': self.errunknown
        }

    def handle_unknown_err(self, error):
        self.errunknown = str(error)
        self.status = SearchItemStatus.failed

    def handle_500(self):
        if self.err500s >= config.QUERY_ERROR_LIMIT:
            self.status = SearchItemStatus.failed
        else:
            self.err500s += 1
            self.status = SearchItemStatus.retry

    def handle_timeout(self, db):
        # For timeouts, split the date range in half and add both to queue
        if self.end_date:
            range1, range2 = split_date_range(self.start_date, self.end_date)
            print("Appending %s from %s to %s" % (self.search_string, range1[0], range1[1]))
            db.merge(SearchItem(
                search_string = self.search_string,
                start_date = range1[0],
                end_date = range1[1],
                court = self.court,
                status = SearchItemStatus.new
            ))
            print("Appending %s from %s to %s" % (self.search_string, range2[0], range2[1]))
            db.merge(SearchItem(
                search_string = self.search_string,
                start_date = range2[0],
                end_date = range2[1],
                court = self.court,
                status = SearchItemStatus.new
            ))
            self.status = SearchItemStatus.timeout_split
        else:
            if self.timeouts >= config.QUERY_TIMEOUTS_LIMIT:
                self.status = SearchItemStatus.failed
            else:
                self.timeouts += 1
                self.status = SearchItemStatus.retry

    def handle_complete(self, db, nresults, query_start, query_time):
        db.add(SearchItemResult(
            search_id = self.id,
            nresults = nresults,
            timestamp = query_start,
            query_seconds = query_time
        ))
        self.status = SearchItemStatus.completed
