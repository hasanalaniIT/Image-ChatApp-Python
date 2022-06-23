import json
import time

import redis

from typing import Tuple
from threading import Thread

from database_connection import DatabaseHandler
from image_utilty import *


# from user_session import *


class MessageHandler:
    redis_client = None
    channels = None

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, password='hasan99')
        self.channels = {
            'private': DatabaseHandler().get_users(),
            'public': ['group1'],
        }

    @classmethod
    def get_private_channels(cls):
        return cls.channels['private']

    @classmethod
    def update_channels(cls):
        cls.channels = {
            'private': DatabaseHandler().get_users(),
            'public': ['group1'],
        }

    @classmethod
    def get_public_channels(cls):
        return cls.channels['public']

    @classmethod
    def get_channels(cls) -> Tuple[list, list]:
        """ Returns private and public channels names in order.
        """
        return cls.channels['private'], cls.channels['public']

    @classmethod
    def get_all_channels(cls) -> list:
        """ Returns all channels names in one list.
        """
        private_channels, public_channels = cls.get_channels()
        # unpack the list using *
        return [*private_channels, *public_channels]


class PrivateMessageSubscriber(Thread, MessageHandler):
    def __init__(self, user_channel: str, recipient: str):
        super().__init__()
        self.user_channel = user_channel
        self.recipient = recipient
        self.start()

    def run(self) -> None:
        redis_pubsub = MessageHandler().redis_client.pubsub()
        redis_pubsub.subscribe(self.user_channel)
        while True:
            redis_message = redis_pubsub.get_message()
            if redis_message:
                data = redis_message["data"]

                if data and isinstance(data, bytes):
                    data = json.loads(data)
                    username = data['username']
                    image = data['image']
                    if image:
                        ImageHandler().open_decoded(image)
                    if self.__check_user_accessibility(username):
                        message = data['message']
                        print(f"\n{username}: {message}\n")
                        time.sleep(0.01)

    def __check_user_accessibility(self, user) -> bool:
        user_exist = True
        if self.recipient != user:
            user_exist = False
        return user_exist


class PublicMessageSubscriber(Thread, MessageHandler):
    def __init__(self, user_channel: str, recipient: str):
        super().__init__()
        self.user_channel = user_channel
        self.recipient = recipient
        self.start()

    def run(self) -> None:
        redis_pubsub = MessageHandler().redis_client.pubsub()
        redis_pubsub.subscribe(self.recipient)
        image_handler = ImageHandler()
        while True:
            redis_message = redis_pubsub.get_message()
            if redis_message:
                data = redis_message["data"]
                if data and isinstance(data, bytes):
                    data = json.loads(data)
                    username = data['username']
                    message = data['message']
                    image = data['image']
                    if image:
                        image_handler.open_decoded(image)
                    print(f"\n{username}: {message}\n")
                    time.sleep(0.01)


class MessagePublisher:
    def __init__(self, username: str, recipient: str):

        self.username = username
        self.recipient = recipient

        self.start()

    def send_message(self, data: dict, recipient: str) -> None:
        """ Prepares and publishes the message to the redis client

        Args:
            data: message to sent to redis channel.
            recipient: the message recipient.
        """
        json_data = json.dumps(data)
        MessageHandler().redis_client.publish(recipient, json_data)

    def start(self) -> None:
        """ Listens continuously to user messages and send them them to the desired destination.
        """
        print("Message session has been started.")
        image_handler = ImageHandler()
        while True:
            message: str = str(input(f"{self.username}: "))
            image = None
            if message == "pic":
                print("select picture")
                image = image_handler.select()
                image_handler.decode(image)
            data: dict = {
                'username': self.username,
                'message': message,
                'image': image
            }
            self.send_message(data, self.recipient)


class MessageSession:
    def __init__(self, username):
        self.username = username
        self.recipient = None
        MessageHandler.update_channels()

    def get_user_info(self) -> None:
        self.recipient: str = str(input("Enter your Recipient: "))

    def start_messaging_session(self):
        """ Starts the messaging session.
        """
        public_channels = MessageHandler.get_public_channels()
        private_channels = MessageHandler.get_private_channels()
        if self.recipient in public_channels:
            PublicMessageSubscriber(self.username, self.recipient)
        elif self.recipient in private_channels:
            PrivateMessageSubscriber(self.username, self.recipient)
        MessagePublisher(self.username, self.recipient)

    def __check_if_channel_exist(self) -> bool:
        print(MessageHandler().get_private_channels())
        channel_exist = True
        all_channels = MessageHandler().get_all_channels()
        private_channels = MessageHandler().get_private_channels()

        if self.username not in private_channels:
            print(f"User '{self.username}' does not exist!")
            channel_exist = False
        if self.recipient not in all_channels:
            print(f"Recipient '{self.recipient}' does not exist!")
            channel_exist = False
        return channel_exist

    def start(self) -> None:
        self.get_user_info()
        if self.__check_if_channel_exist():
            self.start_messaging_session()


TODO: "UPDATE PROJECT structure for update channels method"
