from rest_framework import serializers

from pastebin.services import hash_password
from .models import Category, Comment, Paste, Tag
from rest_framework import serializers
from .models import PasteSettings
import hashlib


class PasteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasteSettings
        fields = ["visibility", "is_password_protected", "password"]


class CreatePasteSerializer(serializers.ModelSerializer):
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("user", "comment", "created_at")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class PasteDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Paste
        fields = (
            "title",
            "content",
            "comments",
            "tags",
        )
