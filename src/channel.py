import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel)
        return

    def to_json(self, name_file):
        chanel_info = {"id": self.id,
                       "title": self.title,
                       "description": self.description,
                       "url": self.url,
                       "subscriber_count": self.subscriber_count,
                       "video_count": self.video_count,
                       "view_count": self.view_count
                       }
        with open(f'../src/{name_file}', 'w', encoding="UTF-8") as file:
            json.dump(chanel_info, file)

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv("YT_API_KEY")
        object_api = build('youtube', 'v3', developerKey=api_key)
        return object_api

    @property
    def channel_id(self):
        return self.__channel_id
