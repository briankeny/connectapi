from django.contrib import admin
from .models import Post,Comment,CommentReply

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(CommentReply)
class PostAdmin(admin.ModelAdmin):
    pass
