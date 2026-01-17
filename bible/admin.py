from django.contrib import admin
from . import models


class BibleBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'bibleLanguage', 'testament', 'bookName', 'chapters', 'created_at', 'updated_at')
    search_fields = ('bookName', 'chapters')
    list_filter = ('bibleLanguage', 'testament')
    
class VersesAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'no_of_chapter', 'no_of_verses', 'verses', 'created_at', 'updated_at')


# registrations
admin.site.register(models.BibleBook, BibleBookAdmin)
admin.site.register(models.Verse, VersesAdmin)