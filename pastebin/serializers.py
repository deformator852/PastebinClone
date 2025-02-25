from rest_framework import serializers

from pastebin.services import hash_password
from .models import Paste
from rest_framework import serializers
from .models import PasteSettings
import hashlib


class PasteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasteSettings
        fields = ["visibility", "is_password_protected", "password"]


class CreatePastSerializer(serializers.ModelSerializer):
    settings = PasteSettingsSerializer()

    class Meta:
        model = Paste
        fields = ("title", "content", "settings", "author")

    def create(self, validated_data):
        settings_data = validated_data.pop("settings")
        hashed_password = hash_password(settings_data["password"])
        settings_data["password"] = hashed_password
        settings = PasteSettings.objects.create(**settings_data)
        author = self.context.get("user")
        paste = Paste.objects.create(author=author, settings=settings, **validated_data)
        return paste


class PasteDetailSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, required=False, default=None)
