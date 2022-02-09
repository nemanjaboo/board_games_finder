from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'link', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'body')
    ordering = ('name', 'status')