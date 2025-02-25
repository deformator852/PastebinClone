from django.contrib import admin
from pastebin.models import Paste, PasteSettings

admin.site.register(Paste)
admin.site.register(PasteSettings)
