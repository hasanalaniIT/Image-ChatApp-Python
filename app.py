import sqlite3
import datetime

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

    @abstractmethod
    def start(self) -> None:
        pass


class Register(UserSession):

    def __int__(self):
        self.username = None
        self.password = None

    def _check_username(self, username) -> bool:
        with DatabaseHandler().database_connected() as db_cursor:
            username_query = db_cursor.execute('SELECT username FROM users ')
            usernames = [user[0] for user in username_query]
        return not (username in usernames)

    def _set_username(self):
        username_input = str(input("Enter your Username: "))
        if self._check_username(username_input):
            self.username = username_input
        else:
            print("this user exists!!!")
            self._set_username()

    def _set_password(self):
        self.password = str(input("Enter your Password: "))

    def _set_credentials(self):
        self._set_username()
        self._set_password()

    def store_data(self):
        with DatabaseHandler().database_connected() as db_cursor:
            db_cursor.execute('INSERT INTO users VALUES(?,?,?,?)',
                              (None, self.username, self.password, str(datetime.date.today())))
        print("Welcome yl 7beeb")

    def start(self):
        self._set_credentials()
        self.store_data()


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


Register().start()
