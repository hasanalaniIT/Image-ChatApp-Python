import sqlite3

from contextlib import contextmanager


class DatabaseHandler:
    @contextmanager
    def database_connected(self):
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        try:
            yield cursor
        except Exception as e:
            print(e)
        finally:
            sqliteConnection.commit()
            cursor.close()