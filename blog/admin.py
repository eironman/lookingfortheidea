from django import forms
from django.contrib import admin
from .models import Post, PostComment, PostMedia, Subscriber


class ContentForm(forms.ModelForm):
    """Convert content field as a textarea"""
    content = forms.CharField(widget=forms.Textarea)


class PostCommentInline(admin.TabularInline):
    """Comments inside Post admin"""
    extra = 0
    form = ContentForm
    model = PostComment


class PostMediaInline(admin.TabularInline):
    """Media inside Post admin"""
    extra = 10
    model = PostMedia
    fields = ('image_small', 'url', 'video_id','description', 'order')
    readonly_fields = ('image_small',) # image_small has to be in fields and readonly_fields to avoid django error
    # define the sortable
    # sortable_field_name = "order"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Blog post"""
    date_hierarchy = 'pub_date'
    form = ContentForm
    fields = ('publish', 'notification_sent', 'title', 'url', 'content', 'pub_date', 'main_image', 'image_medium',)
    inlines = [PostMediaInline, PostCommentInline]
    list_display = ('image_small', 'title', 'publish', 'notification_sent','pub_date', 'num_comments', 'num_media')
    list_filter = ('pub_date',)
    readonly_fields = ('image_medium',) # image_small has to be in fields and readonly_fields to avoid django error
    search_fields = ('title',)

    def num_comments(self, obj):
        return obj.postcomment_set.count()
    num_comments.short_description = 'Comments'

    def num_media(self, obj):
        return obj.postmedia_set.count()
    num_media.short_description = 'Media'

    class Media:
        css = {
            'all': ('/static/blog/css/admin.css',)
        }
        js = (
            '/static/blog/lib/tinymce/tinymce.min.js',
            '/static/blog/js/admin/tinymce_setup.js',
            '/static/blog/js/admin/post.js',
            '/static/blog/js/Helper.js',
        )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Blog subscriber"""
    fields = ('email', 'phone')
    list_display = ('email', 'phone', 'creation_date')