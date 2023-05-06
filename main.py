import asyncio
import csv
import logging
import os
from datetime import datetime, date, time
from sys import platform

from sqlalchemy.exc import IntegrityError

from settings import settings
from database import FinamReportsDAO

logger = logging.getLogger(__name__)
file_log = logging.FileHandler("logger.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")


CSV_PATH = settings.CSV_PATH


def change_directory(status: str):
    if not os.path.isdir(status):
        os.mkdir(status)
    if platform == 'win32':
        file_name = CSV_PATH.split('\\')[-1]
        os.replace(CSV_PATH, f'{os.getcwd()}\\{status}\\{file_name}')
    else:
        file_name = CSV_PATH.split('/')[-1]
        os.replace(CSV_PATH, f'{os.getcwd()}/{status}/{file_name}')


async def get_csv():
    try:
        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.reader(csvfile)
            counter = 1
            for row in reader:
                try:
                    date_record = datetime.strptime(row[0], "%Y-%m-%d") if row[0] != '' else date(year=2001, month=1,
                                                                                                  day=1)
                    date_time_record = datetime.strptime(row[1], "%H:%M:%S") if row[1] != '' else time(hour=0, minute=0,
                                                                                                       second=0)
                    type_record = row[2]
                    comment_record = row[3]
                    symbol_name_record = row[4]
                    symbol_record = row[5]
                    account_record = row[6]
                    sum_record = float(row[7]) if row[7] != '' else 0
                    await FinamReportsDAO.add(
                        date_record=date_record,
                        date_time_record=date_time_record,
                        type_record=type_record,
                        comment_record=comment_record,
                        symbol_name_record=symbol_name_record,
                        symbol_record=symbol_record,
                        account_record=account_record,
                        sum_record=sum_record
                        )
                except IntegrityError:
                    logger.warning(f'File: {CSV_PATH} || Не удалось добавить позицию № {counter}. Строка уже существует')
                except ValueError:
                    logger.warning(f'File: {CSV_PATH} || Не удалось добавить позицию № {counter}. Неверный формат данных')
                counter += 1
        change_directory('SUCCESSFUL')
    except UnicodeDecodeError:
        logger.error(f'File: {CSV_PATH} || Неверный формат файла')
        change_directory('ERRORS')
    except FileNotFoundError:
        logger.error(f'File: {CSV_PATH} || Файл не найден')
    except OSError:
        logger.error(f'File: {CSV_PATH} || Отсутствует соединение с интернетом')
        change_directory('ERRORS')


if __name__ == '__main__':
    asyncio.run(get_csv())
