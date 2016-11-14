from django import forms
from django.contrib import admin
from .models import Post, PostComment


class ContentForm(forms.ModelForm):
    """Convert content field as a textarea"""
    content = forms.CharField(widget=forms.Textarea)


class PostCommentInline(admin.TabularInline):
    """Comments inside Post admin"""
    extra = 0
    form = ContentForm
    model = PostComment
    ordering = ['-pub_date']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Blog post"""
    date_hierarchy = 'pub_date'
    form = ContentForm
    fields = ('title', 'content', 'pub_date', 'main_image', 'image_tag',)
    inlines = [PostCommentInline]
    list_display = ('title', 'short_content', 'pub_date', 'num_comments')
    list_filter = ('pub_date',)
    readonly_fields = ('image_tag',) # image_tag has to be in fields and readonly_fields to avoid django error
    search_fields = ('title',)

    def num_comments(self, obj):
        return obj.postcomment_set.count()
    num_comments.short_description = 'Comments'
