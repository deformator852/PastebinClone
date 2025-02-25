import uuid
from django.db import models
from django.contrib.auth.models import User


class PasteSettings(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"
    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
        (UNLISTED, "Unlisted"),
    ]
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default=PRIVATE
    )
    is_password_protected = models.BooleanField()
    password = models.CharField(max_length=255)


class Paste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=155)
    content = models.TextField(max_length=10000)
    author = models.ForeignKey(User, models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    settings = models.ForeignKey("PasteSettings", models.CASCADE, editable=False)


class PasteHistory(models.Model):
    paste = models.ForeignKey("Paste", models.CASCADE)
    previouse = models.TextField(max_length=10000)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.CASCADE)


class Comment(models.Model):
    paste = models.ForeignKey("Paste", models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=150)
    pastes = models.ManyToManyField("Paste")


class Category(models.Model):
    name = models.CharField(max_length=120)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paste = models.ForeignKey("Paste", on_delete=models.CASCADE)
