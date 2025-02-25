from django.urls import path
from .views import CreatePaste, PasteDetail

urlpatterns = [
    path("paste/", CreatePaste.as_view()),
    path("paste-detail/<uuid:id>/", PasteDetail.as_view()),
]
