from SheeetsUpdate import SUpdater
from SQLWrapper import SQLWrapper
from sys import argv
from platform import node
from datetime import date

import argparse


# Функция для парсинга аргументов
def create_parser():
    arg_parser = argparse.ArgumentParser()
    # Указываем ID файла ключа на Google Drive
    arg_parser.add_argument('-F', '--fileId', default='download id of key at GDrive')
    # Указываем имя базы
    arg_parser.add_argument('-B', '--database', default='base name')
    # Указываем сервер, default - имя компьютера\SQLEXPRESS
    arg_parser.add_argument('-S', '--server', default='{}\SQLEXPRESS'.format(node()))
    # Указываем ID таблицы в Google Spreadsheets
    arg_parser.add_argument('-D', '--spreadsheetId', default='Goole Spreadsheet id')
    # Указываем имя таблиы в SQL
    arg_parser.add_argument('-T', '--sqlTableName', default='table name in sql base')
    # Указываем колонки, которые нужно выгрузить
    arg_parser.add_argument('-C', '--columns', default='*')
    # Указываем имя листа в таблице, куда будут добавляться данные
    arg_parser.add_argument('-N', '--sheetName', required=True)
    # Указываем парамметр SQL запроса WHERE, либо 'None' если не требуется
    arg_parser.add_argument('-W', '--where', default='DATA_START=\'{}\''.format(
        date.today().__str__().replace('-', '.')))

    return arg_parser


if __name__ == '__main__':
    # Создаем парсер
    parser = create_parser()
    # Парсим параметры командной строки
    params = parser.parse_args(argv[1:])
    # Создаем объект парсера SQL
    SW = SQLWrapper(server=params.server, database=params.database)
    # Получем данные из базы по заданным параметрам
    info = SW.get_info(table=params.sqlTableName, columns=params.columns, where=params.where)
    # Преобразуем список множеств в список списков
    # Т.к. Spreadsheets API не работает с множествами
    info = [[i[0], i[1], i[2], i[3]] for i in info]

    # Создаем объект обнавления таблицы
    su = SUpdater(file_id=params.fileId, sheet_id=params.spreadsheetId, sheet_name=params.sheetName)
    # Добавляем в конец таблицы информацию из базы
    su.add_info(info)
