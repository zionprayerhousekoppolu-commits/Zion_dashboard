from rest_framework import serializers
from .models import AppUser, UserToken
from languages.models import languageList


class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = languageList
        fields = "__all__"


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
        
    profile = serializers.SerializerMethodField()


    def create(self, validated_data):
        # Get Telugu default
        try:
            telugu = languageList.objects.get(languageCode="te")
        except languageList.DoesNotExist:
            telugu = None

        # Set default languages only if not supplied
        if "prefered_language_for_dailyWord" not in validated_data:
            validated_data["prefered_language_for_dailyWord"] = telugu

        return super().create(validated_data)
    
    def get_profile(self, obj):
        request = self.context.get("request")
        if obj.profile and request:
            return request.build_absolute_uri(obj.profile.url)
        return obj.profile.url if obj.profile else ""


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]