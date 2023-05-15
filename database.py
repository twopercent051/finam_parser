from sqlalchemy import MetaData, inspect, Column, Date, Time, VARCHAR, DOUBLE_PRECISION, TIMESTAMP, \
    PrimaryKeyConstraint, UniqueConstraint, insert, Integer, Float, update, select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, as_declarative
from sqlalchemy.sql.functions import func

from settings import settings


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

    date_record = Column(Date, nullable=False, server_default='2001-01-01')
    date_time_record = Column(Time, nullable=False, server_default='00:00:00')
    symbol_name_record = Column(VARCHAR(length=150), nullable=False, server_default=' ')
    account_prefix_record = Column(VARCHAR(length=50), nullable=False, server_default=' ')
    account_record = Column(VARCHAR(length=50), nullable=False, server_default=' ')
    account_id_record = Column(Integer, nullable=False, server_default='0')  # Уточнить тип данных и дефолт
    isin_record = Column(VARCHAR(length=50), nullable=False, server_default=' ')
    type_record = Column(VARCHAR(length=500), nullable=False, server_default=' ')
    count_record = Column(Integer, nullable=False, server_default='0')
    deal_price_record = Column(Float(precision=2), nullable=False, server_default='0')
    sum_record = Column(DOUBLE_PRECISION, nullable=False, server_default='0')
    deal_id_record = Column(VARCHAR(length=50), nullable=False, server_default='')
    comment_record = Column(VARCHAR(length=500), nullable=False, server_default=' ')
    symbol_record = Column(VARCHAR(length=50), nullable=False, server_default=' ')
    datetime_add = Column(TIMESTAMP, nullable=False, server_default=func.now())
    finam_reports_pkey = PrimaryKeyConstraint(date_record, date_time_record, symbol_name_record, account_record,
                                              sum_record)
    # unique_record = UniqueConstraint(date_record, date_time_record, type_record, comment_record, symbol_name_record,
    #                                  symbol_record, account_record, sum_record)


class FinamReportsDAO(FinamReports):
    """Класс взаимодействия с БД"""

    @classmethod
    async def add(cls, data):
        async with async_session_maker() as session:
            stmt = insert(FinamReports).values(data)
            await session.execute(stmt)
            await session.commit()

    # @classmethod
    # async def get_all(cls):
    #     async with async_session_maker() as session:
    #         query = select(FinamReports.finam_reports_pkey).where(FinamReports.symbol_record == 'SBER')
    #         result = await session.execute(query)
    #         return result.all()

    @classmethod
    async def update(cls, data: dict, conditions: dict):
        async with async_session_maker() as session:
            stmt = update(FinamReports).values(data).filter_by(**conditions)
            await session.execute(stmt)
            await session.commit()
