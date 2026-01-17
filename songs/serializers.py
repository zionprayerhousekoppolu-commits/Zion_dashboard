from rest_framework import serializers
from .models import SongLyric

class SongLyricSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongLyric
        fields = [
            'id',
            'song_no',
            'song_name',
            'song_title',
            'priseWord',
            'song_lyric',
            'song_audio',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
