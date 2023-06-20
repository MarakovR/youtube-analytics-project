from datetime import timedelta
from src.channel import Channel
import isodate


class PlayList(Channel):

    def __init__(self, playlist_id, channel_id: str = 'UC-OVMPlMA3-YCIeg4z5z23A'):
        super().__init__(channel_id)
        self.playlist_id = playlist_id
        self.playlists = self.youtube.playlists().list(channelId=channel_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    @property
    def total_duration(self):
        __time_video = timedelta(0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            __time_video += duration
        return __time_video

    def show_best_video(self):
        max_like = 0
        id_video_max_like = ''
        for like in self.video_response['items']:
            if int(like['statistics']['likeCount']) > max_like:
                max_like = int(like['statistics']['likeCount'])
        for like in self.video_response['items']:
            if int(like['statistics']['likeCount']) == max_like:
                id_video_max_like = like['id']
        return f'https://youtu.be/{id_video_max_like}'
