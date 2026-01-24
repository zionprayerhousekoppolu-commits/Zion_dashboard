from django.urls import path
from . import views

app_name = 'languages'

urlpatterns = [
    path('songslist/', 
         views.SongListView.as_view(), 
         name='song-list-by-language'),
    
    path('<int:id>/', 
         views.SongDetailView.as_view(), 
         name='song-detail'),
    
    path('search/', 
         views.SongSearchView.as_view(), 
         name='song-search'),]
