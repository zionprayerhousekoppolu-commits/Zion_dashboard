from rest_framework import serializers
from .models import languageList

class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = languageList
        fields = [
            'id',
            'languageCode',
            'languages',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']