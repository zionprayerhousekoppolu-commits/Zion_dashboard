from django.contrib import admin
from . import models

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id','languageCode', 'languages', 'is_active', 'created_at', 'updated_at')
    search_fields = ('languageCode', 'languages')
    list_filter = ('is_active', 'created_at', 'updated_at')
    ordering = ('id','languages',)

admin.site.register(models.languageList, LanguageAdmin)