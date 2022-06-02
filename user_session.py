import datetime

from abc import ABC, abstractmethod

from database_connection import DatabaseHandler
from message_session import MessageSession


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

    def _set_username(self) -> None:
        username_input = str(input("To Register\nEnter your Username: "))
        if self._check_username(username_input):
            self.username = username_input
        else:
            print("this user exists!!!")
            self._set_username()

    def _set_password(self) -> None:
        self.password = str(input("Enter your Password: "))

    def _set_credentials(self) -> None:
        self._set_username()
        self._set_password()

    def store_data(self) -> None:
        with DatabaseHandler().database_connected() as db_cursor:
            db_cursor.execute('INSERT INTO users VALUES(?,?,?,?)',
                              (None, self.username, self.password, str(datetime.date.today())))
        print("Welcome yl 7beeb")

    def start(self) -> None:
        self._set_credentials()
        self.store_data()
        # After Registration the user will be Logged in to the application automatically
        Login().authenticate(self.username, self.password)


class Login(UserSession):
    def _check_username(self, username) -> None:
        pass

    def __int__(self):
        self.username = None
        self.password = None

    def login(self) -> None:
        self.authenticate(self.username, self.password)

    def _set_username(self) -> None:
        self.username = str(input("Enter your Username: "))

    def get_username(self) -> str:
        return self.username

    def _set_password(self) -> None:
        self.password = str(input("Enter your Password: "))

    def _set_credentials(self) -> None:
        self._set_username()
        self._set_password()

    def authenticate(self, username, password) -> None:
        with DatabaseHandler().database_connected() as db_cursor:
            db_password = str(
                db_cursor.execute('SELECT password FROM users WHERE username= ?', (username,)).fetchone()).strip(
                "('',)'")
        if password == db_password:
            print("Login successfully")
            MessageSession(username).start()

        else:
            user_option = input(
                "user or password does not match\n to try again type anything\n to register a new account type (2)\n: ")
            options = {"1": self.start, "2": Register().start}
            if user_option in options.keys():
                options.get(user_option)()
            else:
                self.start()

    def start(self) -> None:
        self._set_credentials()
        self.login()
