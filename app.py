import datetime
import sqlite3
from abc import ABC, abstractmethod

from contextlib import contextmanager


class DatabaseHandler:
    @classmethod
    @contextmanager
    def database_connected(cls):
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        try:
            yield cursor
        except Exception as e:
            print(e)
        finally:
            sqliteConnection.commit()
            cursor.close()


class UserSession(ABC):
    @abstractmethod
    def _set_username(self) -> None:
        pass

    @abstractmethod
    def _set_password(self) -> None:
        pass

    @abstractmethod
    def _set_credentials(self) -> None:
        pass

    @abstractmethod
    def _check_username(self, username) -> None:
        pass


class Register(UserSession):
    @classmethod
    def register(cls, username, password):
        with DatabaseHandler().database_connected() as db_cursor:
            db_cursor.execute('INSERT INTO users VALUES(?,?,?,?)',
                              (None, username, password, str(datetime.date.today())))

    def __int__(self):
        self.username = None
        self.password = None

    def _check_username(self, username) -> bool:
        with DatabaseHandler().database_connected() as db_cursor:
            username_query = db_cursor.execute('SELECT username FROM users ')
            usernames = [user[0] for user in username_query]
        return not (username in usernames)

    def _set_username(self):
        self.username = str(input("Enter your Username: "))

    def _set_password(self):
        self.password = str(input("Enter your Password: "))

    def _set_credentials(self):
        self._set_username()
        self._set_password()


class Login(UserSession):
    def _check_username(self, username) -> None:
        pass

    def __int__(self):
        self.username = None
        self.password = None

    def login(self):
        self.authenticate(self.username, self.password)

    def _set_username(self):
        self.username = str(input("Enter your Username: "))

    def _set_password(self):
        self.password = str(input("Enter your Password: "))

    def _set_credentials(self):
        self._set_username()
        self._set_password()

    def authenticate(self, username, password):
        with DatabaseHandler().database_connected() as db_cursor:
            db_password = str(
                db_cursor.execute('SELECT password FROM users WHERE username= ?', (username,)).fetchone()).strip(
                "('',)'")
        if password == db_password:
            print("Login successfully")
        else:
            print("user or password does not match try again!!")
            self.start()

    def start(self):
        self._set_credentials()
        self.login()


# DatabaseHandler().register("HASAN", "1234")

