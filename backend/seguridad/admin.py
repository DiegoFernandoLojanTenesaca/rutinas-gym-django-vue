from django.contrib import admin
from .models import UsersMetadata

@admin.register(UsersMetadata)
class UsersMetadataAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token")
    search_fields = ("user__email",)
