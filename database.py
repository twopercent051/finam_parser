from typing import Optional

from pydantic import BaseModel
from sqlalchemy import MetaData, inspect, Column, Integer, Date, Time, VARCHAR, DOUBLE_PRECISION, TIMESTAMP, Constraint, \
    PrimaryKeyConstraint, UniqueConstraint, insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, as_declarative
from sqlalchemy.sql.functions import now, func

from settings import settings

from datetime import date, time

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    metadata = MetaData()

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class FinamReports(Base):
    """Класс модели БД"""
    __tablename__ = 'finam_reports'

    date_record = Column(Date, nullable=False, default=date(year=2001, month=1, day=1))
    date_time_record = Column(Time, nullable=False, default=time(hour=0, minute=0, second=0))
    type_record = Column(VARCHAR(length=500), nullable=False, default=' ')
    comment_record = Column(VARCHAR(length=500), nullable=False, default=' ')
    symbol_name_record = Column(VARCHAR(length=150), nullable=False, default=' ')
    symbol_record = Column(VARCHAR(length=50), nullable=False, default=' ')
    account_record = Column(VARCHAR(length=50), nullable=False, default=' ')
    sum_record = Column(DOUBLE_PRECISION, nullable=False, default=0)
    datetime_add = Column(TIMESTAMP, nullable=False, default=func.now())
    finam_reports_pkey = PrimaryKeyConstraint(date_record, date_time_record, type_record, comment_record,
                                              symbol_name_record, symbol_record, account_record, sum_record)
    unique_record = UniqueConstraint(date_record, date_time_record, type_record, comment_record, symbol_name_record,
                                     symbol_record, account_record, sum_record)


class SFinamReports(BaseModel):
    """Базовая модель"""
    date_record: Optional[date]
    date_time_record: Optional[time]
    type_record: str
    comment_record: str
    symbol_name_record: str
    symbol_record: str
    account_record: str
    sum_record: float
    datetime_add: int


class FinamReportsDAO(FinamReports):
    """Класс взаимодействия с БД"""
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(FinamReports).values(**data)
            await session.execute(stmt)
            await session.commit()

