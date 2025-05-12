from django.contrib import admin
from .models import Thread, ThreadCategory, Comment

class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    
    list_display = ('title', 'category', 'created_on', 'updated_on')

class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory

    list_display = ('name',)

class CommentAdmin(admin.ModelAdmin):
    model = Comment

    list_display = ('author', 'thread', 'created_on', 'updated_on')

admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Comment, CommentAdmin)

