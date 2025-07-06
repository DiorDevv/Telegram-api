from django.contrib import admin

# Register your models here.

from .models import User, Chat, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-last_login',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_group', 'created_at')
    search_fields = ('id',)
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'is_read', 'created_at')
    search_fields = ('chat__id', 'sender__username', 'text')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)
