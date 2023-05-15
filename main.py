import asyncio
import os
from sys import platform, argv
import glob

from parser import Parser
from settings import logger


class Script:

    @staticmethod
    def replacer(status: str, file_path: str, directory_path: str):
        """Метод перемещения файла в категорию"""
        separator = '\\' if platform == 'win32' else '/'
        if not os.path.exists(f'{directory_path}{separator}{status}'):
            os.makedirs(f'{directory_path}{separator}{status}')
        file_name = file_path.split(separator)[-1]
        os.replace(file_path, f'{directory_path}{separator}{status}{separator}{file_name}')

    @classmethod
    async def directory_parser(cls, import_type: str, path: str, account_id: int):
        file_list = []
        for file_type in ['csv', 'xml', 'xls', 'xlsx']:
            if platform == 'win32':
                file_list.extend(glob.glob(f"{path}\\*.{file_type}"))
            else:
                file_list.extend(glob.glob(f"{path}/*.{file_type}"))

        for file in file_list:
            file_type = file.split('.')[-1]
            try:
                if file_type == 'csv':
                    data = Parser.import_type_detector(import_type)
                    await Parser.csv_parser(file=file, indexes=data, account_id=account_id)
                elif file_type == 'xml':
                    await Parser.xml_parser(file=file, import_type=import_type, account_id=account_id)
                elif file_type == 'xlsx':
                    await Parser.xlsx_parser(file=file, account_id=account_id, import_type=import_type)
                else:
                    await Parser.xls_parser(file=file, account_id=account_id, import_type=import_type)
                cls.replacer('SUCCESSFUL', file, path)
                continue
            # except UnicodeDecodeError:
            #     logger.error(f'File: {file} || {import_type} || Неверный формат файла')
            # except FileNotFoundError:
            #     logger.error(f'File: {file} || {import_type} || Файл не найден')
            # except OSError:
            #     logger.error(f'File: {file} || {import_type} || Отсутствует соединение с интернетом')
            except asyncio.exceptions.TimeoutError:
                logger.error(f'File: {file} || {import_type} || Ошибка подключения к БД')
            except KeyError:
                logger.error(f'File: {file} || {import_type} || Проверьте тип импорта')
            cls.replacer('ERRORS', file, path)


if __name__ == '__main__':
    """ВНИМАНИЕ! Путь прописывается без замыкающего слэша"""
    try:
        import_type = argv[1]
        path = argv[2]
        account_id = int(argv[3])
        asyncio.run(Script.directory_parser(import_type=import_type, path=path, account_id=account_id))
    except IndexError:
        logger.critical('Недостаточно параметров для запуска')
    except ValueError as ex:
        logger.error(f'Неверный тип данных || {ex}')
