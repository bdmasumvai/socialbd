from django.contrib import admin
from .models import Post, Like, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'privacy', 'created_at')

admin.site.register(Like)
admin.site.register(Comment)
