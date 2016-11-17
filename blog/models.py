import datetime
from PIL import Image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatewords


# User posts
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)
    main_image = models.ImageField(upload_to='blog/%Y/%m/%d/', null=True)

    def save(self):
        """Overwrite save method to resize image"""
        super(Post, self).save()

        # Get original image
        image = Image.open(self.main_image)

        # Resize and save
        maxsize = (800, 600)
        image.thumbnail(maxsize, Image.ANTIALIAS)
        image.save(self.main_image.path)

    # String representation of the class
    def __str__(self):
        return self.title + ' - ' + self.content

    # Returns an html image tag
    def image_tag(self):
        if self.main_image:
            return u'<img style="max-width:300px" src="%s%s" />' % (settings.MEDIA_URL, self.main_image)
        else:
            return '-'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    # Returns a short version of the content
    def short_content(self):
        return truncatewords(self.content, 15)

    # Checks if a post was created one day ago
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# Comments for posts
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return '%s - %s - %s' % (self.owner, self.pub_date, self.content)

    class Meta:
        ordering = ('-pub_date',)


# Media (images, videos) for posts
class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, null=True)
    video_id = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)

    def save(self):
        """Overwrite save method to resize image"""
        super(PostMedia, self).save()

        if (self.url):
            # Get original image
            image = Image.open(self.url)

            # Resize and save
            maxsize = (800, 600)
            image.thumbnail(maxsize, Image.ANTIALIAS)
            image.save(self.url.path)

    def image_tag(self):
        if self.url:
            return u'<img style="max-width:80px" src="%s%s" />' % (settings.MEDIA_URL, self.url)
        else:
            return '-'
    image_tag.allow_tags = True

    class Meta:
        ordering = ('order',)
