from django.db import models

    # Create your models here.
class SongLyric(models.Model):
    song_no = models.IntegerField(unique=True)
    song_name = models.CharField(max_length=200)
    song_title = models.TextField()
    priseWord = models.TextField()
    song_lyric = models.TextField()
    song_audio = models.FileField(upload_to='songs/audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.song_no)