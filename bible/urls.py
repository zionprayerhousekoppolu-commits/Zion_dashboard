# urls.py
from django.urls import path
from . import views

app_name = 'bible'

urlpatterns = [
    path('<str:language_code>/biblelist/', views.BibleListByLanguageView.as_view(), name='bible-list-by-language'),
    path('books/<int:book_id>/verses/', views.BibleVersesByBookView.as_view(), name='verses-by-book'),
    path('search/', views.VerseSearchView.as_view(), name='verse-search'),
    path('verseoftheday/today', 
     views.VerseOfTheDayView.as_view(), 
     name='verse-of-the-day'),
]