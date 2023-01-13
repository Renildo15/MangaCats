from django.contrib import admin
from .models import CommentChapter, CommentManga, ReplyCommentChapter, ReplyCommentManga
# Register your models here.
admin.site.register(CommentChapter)
admin.site.register(CommentManga)
admin.site.register(ReplyCommentChapter)
admin.site.register(ReplyCommentManga)