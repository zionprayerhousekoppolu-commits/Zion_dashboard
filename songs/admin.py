from django.contrib import admin
from . import models

    
class SongLyricsAdmin(admin.ModelAdmin):
    list_display = ('id','song_no', 'song_name', 'song_title', 'priseWord', 'created_at', 'updated_at')
    search_fields = ('song_no', 'song_name', 'song_title', 'priseWord')
    list_filter = ('song_no',)


# Register your models here.
admin.site.register(models.SongLyric, SongLyricsAdmin)