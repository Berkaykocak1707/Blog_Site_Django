from django.contrib import admin
from .models import Category, Blog, Comment
from .models import Reply

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment',)
    search_fields = ('name', 'reply', 'comment__name')

    def short_reply(self, obj):
        return obj.reply[:50] + '...' if len(obj.reply) > 50 else obj.reply
    short_reply.short_description = 'Reply'

admin.site.register(Reply, ReplyAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # 'name' alanına göre 'slug' alanını otomatik doldur

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'date',]
    list_filter = ['date', 'categories']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}  # 'title' alanına göre 'slug' alanını otomatik doldur
    date_hierarchy = 'date'  # Tarihe göre hiyerarşik görünüm

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'get_replies_count']
    search_fields = ['name', 'comment']

    def get_replies_count(self, obj):
        return obj.replies.count()
    get_replies_count.short_description = 'Number of Replies'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
