from django.contrib import admin
from .models import SaunaUser, AufgussSession, ChatMessage

@admin.register(SaunaUser)
class SaunaUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'color', 'is_active', 'is_permanent_admin', 'created_at')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('is_active', 'is_permanent_admin')

@admin.register(AufgussSession)
class AufgussSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'created_by')
    search_fields = ('title', 'description', 'created_by__full_name')
    list_filter = ('start_time',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'timestamp', 'content')
    search_fields = ('sender__full_name', 'content')
    list_filter = ('timestamp',)
