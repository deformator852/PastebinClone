from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from pastebin.services import hash_password
from .models import Comment, Paste, PasteSettings
from .serializers import CommentSerializer, CreatePasteSerializer, PasteDetailSerializer


class CreatePaste(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data.copy()
        seriazlier = CreatePasteSerializer(data=data, context={"user": request.user})
        if seriazlier.is_valid(raise_exception=True):
            seriazlier.save()
            return Response({"msg": "paste successfully created"})
        return Response(seriazlier.error_messages, status=400)


class PasteDetail(APIView):
    def post(self, request, id):
        password = request.data.get("password", None)
        paste = Paste.objects.select_related("settings").get(id=id)
        visibility = paste.settings.visibility
        if visibility == PasteSettings.PRIVATE and paste.author.id != request.user.id:
            return Response({"msg": "it's private paste"}, status=403)
        if paste.settings.is_password_protected:
            if not password:
                return Response({"msg": "paste require password"}, status=400)
            hashed_password = hash_password(password)
            if not paste.settings.password == hashed_password:
                return Response({"msg": "wrong password"}, status=400)

        comments = Comment.objects.filter(paste=paste.id)[0:10]
        comment_serializer = CommentSerializer(comments, many=True)

        paste_serializer = PasteDetailSerializer(paste)

        response = {
            "paste": paste_serializer.data,
            "comments": comment_serializer.data,
        }
        return Response(response)
