from django.urls import path
from . import views

urlpatterns = [
    # Create or Update (auto) User
    path("saveuser/", views.SaveUser.as_view(), name="save_user"),

    # Get all users
    path("users/", views.GetUsers.as_view(), name="get_users"),

    # Get single user
    path("currentuser/", views.GetUser.as_view(), name="get_user"),

    # Update user
    path("users/<int:id>/update/", views.UserUpdate.as_view(), name="update_user"),

    # Delete user
    path("users/<int:id>/delete/", views.UserDeleteAccount.as_view(), name="delete_user"),

    # Logout user
    path("users/<int:id>/logout/", views.UserLogout.as_view(), name="logout_user"),
    
    # Save User Token
    path('savetoken/', views.SaveUserToken.as_view(), name='save_user_token'),
]
