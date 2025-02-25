from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Paste
from .serializers import CreatePastSerializer, PasteDetailSerializer


class CreatePaste(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data.copy()
        seriazlier = CreatePastSerializer(data=data, context={"user": request.user})
        if seriazlier.is_valid(raise_exception=True):
            seriazlier.save()
            return Response({"msg": "paste successfully created"})
        return Response(seriazlier.error_messages, status=400)


class PasteDetail(APIView):
    def post(self, request, id):
        password = request.data.get("password")
        paste = (
            Paste.objects.select_related("author", "settings")
            .filter(id=id)
            .values(
                "title",
                "content",
                "author",
                "updated_at",
                "settings__is_password_protected",
                "settings__password",
            )
        )
        return Response({})
