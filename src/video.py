import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=self.video_id).execute()
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

        except IndexError:
            self.title = None
            self.like_count = None
            print('Данного ID не существует')

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, playlists_id):
        super().__init__(video_id)
        self.playlist_id = playlists_id
        self.youtube = super().youtube
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
