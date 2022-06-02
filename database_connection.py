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

    @classmethod
    def get_users(cls) -> list:
        with DatabaseHandler().database_connected() as db_cursor:
            username_query = db_cursor.execute('SELECT username FROM users')
            return [user[0] for user in username_query]

