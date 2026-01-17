from django.db import models
from languages.models import languageList


# Book creating
class BibleBook(models.Model):
    bibleLanguage = models.ForeignKey(languageList, on_delete=models.CASCADE, related_name='bible_books', default=1)
    TESTAMENT_CHOCIES = [
        ('OT', 'Old Testament - 39'),
        ('NT', 'New Testment - 27')
    ]
    testament = models.CharField(max_length=2, choices=TESTAMENT_CHOCIES, default='OT')
    booknumber = models.PositiveIntegerField()
    bookName = models.CharField(max_length=100)
    chapters = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bookName} ({self.bibleLanguage.languages})"


# creating verses
class Verse(models.Model):
    book = models.ForeignKey(BibleBook, on_delete=models.CASCADE, related_name='bible_verses')
    no_of_chapter = models.PositiveIntegerField()
    no_of_verses = models.PositiveIntegerField()
    verses = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.book}"