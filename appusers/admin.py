from django.contrib import admin
from .models import AppUser, UserToken

# Register your models here.
class AppAdminUsersList(admin.ModelAdmin):
    list_display = ('id','name','role' ,'prefered_language_for_dailyWord','is_login','is_active','is_logout','created_at','updated_at')
    
class UserTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_name",     
        "access_token",
        "created_at",
        "updated_at",
    )

    search_fields = ("user__gmail", "access_token")
    ordering = ("-updated_at",)
    
admin.site.register(AppUser, AppAdminUsersList)
admin.site.register(UserToken, UserTokenAdmin)