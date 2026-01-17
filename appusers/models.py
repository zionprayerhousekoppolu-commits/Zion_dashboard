from django.db import models
from languages.models import languageList

# Create your models here.
# class AppUser(models.Model):
#     ROLE_CHOCIES = [
#         ('SUP', 'SuperAdmin'),
#         ('ADM', 'Admin'),
#         ('User', 'User')
#     ]
#     role = models.CharField(max_length=4, choices=ROLE_CHOCIES)
#     userName = models.CharField()
#     name = models.CharField()
#     mobileNumber = models.CharField()
#     gmail = models.CharField()
#     age = models.PositiveIntegerField()
#     profile = models.FileField(upload_to='users/profile/', null=True, blank=True)
#     prefered_language_for_dailyWord = models.ForeignKey(languageList, on_delete=models.CASCADE, related_name='AdminUsers', null=True, blank=True)
#     is_login = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     is_logout = models.BooleanField(default=False)
#     created_at =models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
class AppUser(models.Model):
    ROLE_CHOCIES = [
        ('SUP', 'SuperAdmin'),
        ('ADM', 'Admin'),
        ('User', 'User')
    ]
    role = models.CharField(max_length=4, choices=ROLE_CHOCIES)
    name = models.CharField()
    mobileNumber = models.CharField(null=True, blank=True)
    gmail = models.CharField()
    age = models.PositiveIntegerField(null=True, blank=True, default=0)
    profile = models.FileField(upload_to='users/profile/', null=True, blank=True)
    prefered_language_for_dailyWord = models.ForeignKey(languageList, on_delete=models.CASCADE, related_name='dailyword_users', null=True, blank=True)
    is_login = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_logout = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class UserToken(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="tokens")
    access_token = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def user_name(self):   
        return self.user.name
        
