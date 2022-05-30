from user_session import Login, Register


class App:
    def __init__(self):
        self.option = None

    def start(self) -> None:
        self.option = input("Welcome to Image Chat\nTo Continue Please Type\n(1) for Login\n(2) for Signup\n: ")
        options = {"1": Login().start, "2": Register().start}
        if self.option in options.keys():
            options.get(self.option)()
        else:
            self.start()

    def exit_menu(self):
        return self.start()


if __name__ == '__main__':
    App().start()
