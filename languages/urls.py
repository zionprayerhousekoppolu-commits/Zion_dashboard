from django.urls import path
from . import views

app_name = 'languages'

urlpatterns = [
    path('languageslist/', views.LanguageListView.as_view(), name='languageslist'),
]
