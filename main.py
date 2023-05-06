import asyncio
import csv
import logging
import os
from datetime import datetime, date, time
from sys import platform
import glob

from sqlalchemy.exc import IntegrityError

from database import FinamReportsDAO

logger = logging.getLogger(__name__)
file_log = logging.FileHandler("logger.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.WARNING,
                    format="%(asctime)s %(levelname)s %(message)s")


class CSVParser:

    @staticmethod
    def import_type_detector(import_type: str) -> dict:
        """При добавлении импортов заполнить индексами столбцов начиная с нуля"""
        if import_type == 'finam':
            data = dict(
                import_type=import_type,
                date_index=0,
                date_time_index=1,
                type_index=2,
                comment_index=3,
                symbol_name_index=4,
                symbol_index=5,
                account_index=6,
                sum_index=7,
                date_format="%Y-%m-%d",
                date_time_format="%H:%M:%S"
                )
        else:
            data = dict()
        return data

    @staticmethod
    async def file_parser(file: str, data: dict):
        """Метод парсинга файла и добавления в БД"""
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            counter = 1
            for row in reader:
                try:
                    if row[data['date_index']] != '':
                        date_record = datetime.strptime(row[data['date_index']], data['date_format'])
                    else:
                        date_record = date(year=2001, month=1, day=1)

                    if row[data['date_time_index']] != '':
                        date_time_record = datetime.strptime(row[data['date_time_index']], data['date_time_format'])
                    else:
                        date_time_record = time(hour=0, minute=0, second=0)

                    type_record = row[data['type_index']]
                    comment_record = row[data['comment_index']]
                    symbol_name_record = row[data['symbol_name_index']]
                    symbol_record = row[data['symbol_index']]
                    account_record = row[data['account_index']]
                    sum_record = float(row[data['sum_index']]) if row[data['sum_index']] != '' else 0
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
                    logger.warning(
                        f'File: {file} || {data["import_type"]} || Не удалось добавить позицию № {counter}. Строка '
                        f'уже существует')
                except ValueError:
                    logger.warning(
                        f'File: {file} || {data["import_type"]} || Не удалось добавить позицию № {counter}. Неверный '
                        f'формат данных')
                counter += 1

    @staticmethod
    def replacer(status: str, file_path: str, directory_path: str):
        separator = '\\' if platform == 'win32' else '/'
        if not os.path.exists(f'{directory_path}{separator}{status}'):
            os.makedirs(f'{directory_path}{separator}{status}')
        file_name = file_path.split(separator)[-1]
        os.replace(file_path, f'{directory_path}{separator}{status}{separator}{file_name}')

    @classmethod
    async def directory_parser(cls, import_type: str, path: str):
        if platform == 'win32':
            file_list = glob.glob(f"{path}\\*.csv")
        else:
            file_list = glob.glob(f"{path}/*.csv")

        for file in file_list:
            try:
                data = cls.import_type_detector(import_type)
                await cls.file_parser(file, data)
                cls.replacer('SUCCESSFUL', file, path)
                continue
            except UnicodeDecodeError:
                logger.error(f'File: {file} || {import_type} || Неверный формат файла')
            except FileNotFoundError:
                logger.error(f'File: {file} || {import_type} || Файл не найден')
            except OSError:
                logger.error(f'File: {file} || {import_type} || Отсутствует соединение с интернетом')
            except asyncio.exceptions.TimeoutError:
                logger.error(f'File: {file} || {import_type} || Ошибка подключения к БД')
            except KeyError:
                logger.error(f'File: {file} || {import_type} || Проверьте тип импорта')
            cls.replacer('ERRORS', file, path)


if __name__ == '__main__':
    """ВНИМАНИЕ! Путь прописывается без замыкающего слэша"""
    import_type = 'finam'
    csv_path = ''
    asyncio.run(CSVParser.directory_parser(import_type, csv_path))
