import pyodbc


class SQLWrapper(object):
    def __init__(self, server, database):
        # Подключаемся к базе
        self.connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server}; SERVER=%s; "
            "DATABASE=%s; TRUSTED_CONNECTION=yes" % (server, database))
        self.cursor = self.connection.cursor()

    def get_info(self, table, columns, where):
        if where != 'None':
            self.cursor.execute("SELECT %s FROM %s WHERE %s" % (columns, table, where))
        else:
            self.cursor.execute("SELECT %s FROM %s" % (columns, table))
        info = self.cursor.fetchall()
        return info
