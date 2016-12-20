from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image


class VisitorBookMessage(models.Model):
    """Messages published in the visitor's book"""
    name = models.CharField(max_length=200, null=False)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=settings.VISITORS_BOOK_IMAGES_STORAGE_DIRECTORY, null=True, blank=True)
    date = models.DateTimeField('published date', default=timezone.now)

    def save(self):
        """Overwrite save method to resize image"""
        super(VisitorBookMessage, self).save()
        if self.image:
            image = Image.open(self.image.path)
            image.thumbnail(settings.VISITORS_BOOK_MESSAGE_IMAGE_SIZE, Image.ANTIALIAS)
            image.save(self.image.path)

    def image_tag(self):
        """Returns the image enclosed in html img tag"""
        if self.image:
            return u'<img src="%s%s" />' % (settings.MEDIA_URL, self.image)
        else:
            return '-'
    image_tag.allow_tags = True
    image_tag.short_description = ''

    class Meta:
        ordering = ('-date',)
