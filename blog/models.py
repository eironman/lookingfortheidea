import datetime
import os
from PIL import Image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatewords


def get_thumbnail_path(original_image_full_path, suffix):
    """Returns the path to a thumbnail"""
    original_image_path = os.path.split(original_image_full_path)[0] + '/'
    original_image_name = os.path.split(original_image_full_path)[1].split('.')[0]
    original_image_extension = os.path.split(original_image_full_path)[1].split('.')[1]
    return original_image_path + original_image_name + suffix + '.' + original_image_extension


def create_thumbnail(original_image_full_path, size, suffix):
    """Creates a resized version of an image"""

    # Get original image
    original_image = Image.open(original_image_full_path)

    # Create a copy
    image_copy = original_image.copy()

    # Resize
    image_copy.thumbnail(size, Image.ANTIALIAS)

    # Save
    image_copy.save(get_thumbnail_path(original_image_full_path, suffix))
    return


class Post(models.Model):
    """User posts"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)
    main_image = models.ImageField(upload_to=settings.BLOG_IMAGES_STORAGE_DIRECTORY, null=True)

    def save(self):
        """Overwrite save method to create different image size"""
        super(Post, self).save()
        if self.main_image:
            create_thumbnail(self.main_image.path, settings.THUMBNAIL_BIG, '_big')
            create_thumbnail(self.main_image.path, settings.THUMBNAIL_MEDIUM, '_medium')
            create_thumbnail(self.main_image.path, settings.THUMBNAIL_SMALL, '_small')

    def __str__(self):
        """String representation of the class"""
        return self.title + ' - ' + self.content

    def image_tag(self, size=None):
        if self.main_image:
            if size:
                return u'<img src="%s" />' % get_thumbnail_path(self.main_image.url, size)
            else:
                return u'<img src="%s%s" />' % (settings.MEDIA_URL, self.main_image)
        else:
            return '-'

    def image_big(self):
        return self.image_tag('_big')
    image_big.allow_tags = True

    def image_medium(self):
        return self.image_tag('_medium')
    image_medium.allow_tags = True

    def image_small(self):
        return self.image_tag('_small')
    image_small.allow_tags = True

    def short_content(self):
        """Returns a short version of the post content"""
        return truncatewords(self.content, 15)
    short_content.allow_tags = True

    def was_published_recently(self):
        """Checks if a post was created one day ago"""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class PostComment(models.Model):
    """Comments for posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return '%s - %s - %s' % (self.owner, self.pub_date, self.content)

    class Meta:
        ordering = ('-pub_date',)


class PostMedia(models.Model):
    """Media (images, videos) for posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.ImageField(upload_to=settings.BLOG_IMAGES_STORAGE_DIRECTORY, blank=True, null=True)
    video_id = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)

    def save(self):
        """Overwrite save method to resize image"""
        super(PostMedia, self).save()
        if self.url:
            create_thumbnail(self.url.path, settings.THUMBNAIL_BIG, '_big')
            create_thumbnail(self.url.path, settings.THUMBNAIL_MEDIUM, '_medium')
            create_thumbnail(self.url.path, settings.THUMBNAIL_SMALL, '_small')

    def image_tag(self, size=None):
        if self.url:
            if size:
                return u'<img src="%s" />' % get_thumbnail_path(self.url.url, size)
            else:
                return u'<img src="%s%s" />' % (settings.MEDIA_URL, self.url)
        else:
            return '-'

    def image_big(self):
        return self.image_tag('_big')
    image_big.allow_tags = True

    def image_medium(self):
        return self.image_tag('_medium')
    image_medium.allow_tags = True

    def image_small(self):
        return self.image_tag('_small')
    image_small.allow_tags = True

    def image_url_big(self):
        return get_thumbnail_path(self.url.url, '_big')

    def image_url_medium(self):
        return get_thumbnail_path(self.url.url, '_medium')

    def image_url_small(self):
        return get_thumbnail_path(self.url.url, '_small')

    class Meta:
        ordering = ('order',)
