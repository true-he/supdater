from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from urllib.request import urlopen


class SUpdater(object):
    def __init__(self, file_id, sheet_id, sheet_name):
        # Скачиваем файл с api-key
        self.json_key_filename = self.download_key(file_id)
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        # Указываем куда авторизуемся
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        # Авторизуемся в сервисах, указанных в SCOPES
        self.credentials = Credentials.from_service_account_file(self.json_key_filename, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.credentials)

    # Функция принимает список списков, затем добавляет построчно в конец таблицы sheet_id
    # Пример входного списка: [['Ячейка A1', 'Ячейка B1', 'Ячейка C1', 'Ячейка D1'],
    #                          ['Ячейка A2', 'Ячейка B2', 'Ячейка C2', 'Ячейка D2']]
    def add_info(self, rows):
        # Формируем запрос
        request = self.service.spreadsheets().values().append(spreadsheetId=self.sheet_id,
                                                              range=self.sheet_name,
                                                              valueInputOption='USER_ENTERED',
                                                              insertDataOption='OVERWRITE',
                                                              body={"values": rows})
        # Отправляем запрос
        response = request.execute()
        # Возвращаем ответ от Spreadsheets
        return response

    # Скачивает файл по id в Google Drive
    # Сохраняет под именем 'key.json' в родительской директории
    # (Прим.: Не работает для больших файлов, т.к. нужно подтверждение)
    @staticmethod
    def download_key(file_id):
        # Открывает ссылку на скачивание
        key = urlopen('https://drive.google.com/uc?export=download&id={}'.format(file_id))
        # Сохраняет с именем 'key.json'
        with open('key.json', 'wb') as file:
            file.write(key.read())
        return 'key.json'
