from django.db import models
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings

import os
from cStringIO import StringIO
from PIL import Image
from datetime import datetime

from watermark import watermark

PICTURE_TYPE_CHOICES = (
    ('M', 'Master'),
    ('C', 'Common'),
)
THUMBNAIL_SIZE = (128, 128)
MAX_PHOTO_SIZE = (512, 512)
BANNER_WIDTH = float(978)
BANNER_CROP = (0,256,978,384) # BANNER_CROP is left, upper, right, lower


def updateContent(field, name, img, fmt="JPEG"):
    fp = StringIO()
    img.save(fp, fmt, quality=128)
    cf = ContentFile(fp.getvalue())
    if field:
        os.remove(field.path)
        field.save(name=name, content=cf, save=False)


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and obj.id != model.objects.get().id):
        raise ValidationError('Can only create 1 %s instance' % model.__name__)


# Create your models here.
class Project(models.Model):
    def __unicode__(self):
        return self.project
    project = models.CharField(max_length=200)
    banner = models.ImageField(upload_to='images/banner', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    # Used to add a banner image if a picture is uploaded as a Master.
    def upload_banner(self, name, img, fmt):
        updateContent(self.banner, name, img, fmt)
        super(Project, self).save()

class Picture(models.Model):
    def __unicode__(self):
        return self.title
    project = models.ForeignKey(Project)
    picture_type = models.CharField(max_length=3, choices=PICTURE_TYPE_CHOICES, default='C')
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.ImageField(upload_to='images')
    thumb = models.ImageField(upload_to='images/thumb')
    pub_date = models.DateTimeField(auto_now_add=True)

    def resize_image(self, field, size, source, add_watermark=False):
        original = Image.open(source.path)
        fmt = original.format
        img = original.copy()
        img.thumbnail(size, Image.ANTIALIAS)
        if add_watermark:
            img = watermark(img, settings.MEDIA_ROOT + 'resources/small_watermark.png')
            img = watermark(img, settings.MEDIA_ROOT + 'resources/large_watermark.png',position='center',opacity=0.1)
        updateContent(field, source.name, img, fmt)

    def crop_image(self, field, source, required_width, crop_size):
        """ Suitable for only this one application """
        # These saves will add the image files.
        field.save(source.name, source, save=False)

        # Get dimentions needed for the eventual crop.
        img = Image.open(source.path)
        fmt = img.format
        width, height = img.size
        multiplier = required_width / width
        width = int(width * multiplier)
        height = int(height * multiplier)

        # Resize the image, crop, load the crop, upload
        img = img.resize((width, height), Image.ANTIALIAS)
        img = img.crop(crop_size)
        img.load()
        self.project.upload_banner(source.name, img, fmt)


    def save(self, *args, **kwargs):
        try: # Detect if picture object exists.
            this = Picture.objects.get(id=self.id)
            if this.image != self.image: # Uploaded image is new.
                # Delete previous image and thumb.
                this.image.delete(save=False)
                this.thumb.delete(save=False)
                # Save self.image as it is used for banner and thumb.
                self.image.save(self.image.name, self.image, save=False)
                if self.picture_type == 'M': # Add a banner if this is a master.
                    this.project.banner.delete(save=False)
                    self.crop_image(self.project.banner, self.image, BANNER_WIDTH, BANNER_CROP)
                # Add replacement image and thumb. Image gets watermark so it comes last.
                self.resize_image(self.thumb, THUMBNAIL_SIZE, self.image)
                self.resize_image(self.image, MAX_PHOTO_SIZE, self.image, add_watermark=True)
            elif this.picture_type != self.picture_type: # Image did not change but picture_type did.
                if self.picture_type == 'M': # This is now a master. Add Banner.
                    self.crop_image(self.project.banner, self.image, BANNER_WIDTH, BANNER_CROP)
                else: # This is no longer a master. Delete Banner.
                    self.project.banner.delete(save=False)
        except: # Picture object does not exist.
            # This save comes first because thumb and banner require image.
            self.image.save(self.image.name, self.image, save=False)
            # If this is a master image.
            if self.picture_type == 'M': # Add the banner to the project.
                self.crop_image(self.project.banner, self.image, BANNER_WIDTH, BANNER_CROP)
            # Add the image and thumb.
            self.thumb.save(self.image.name, self.image, save=False)
            self.resize_image(self.thumb, THUMBNAIL_SIZE, self.image)
            self.resize_image(self.image, MAX_PHOTO_SIZE, self.image, add_watermark=True)

        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        self.thumb.delete(save=False)
        #self.project.banner.delete(save=False)
        super(Picture, self).delete(*args, **kwargs)





















# Not working at the moment. Saving for later.
class Style(models.Model):
    bg_color = models.CharField(max_length=6, default='b0c4de')
    banner_width = models.IntegerField(help_text='This is also the page width', default=978)
    banner_height = models.IntegerField(default=128)
    navigation_bar_width = models.IntegerField(default=150)
    thumbs_per_row = models.IntegerField(default=5)
    thumbs_per_page = models.IntegerField(default=20)
    image_width = models.IntegerField(help_text='Maximum width of an image.', default=640)
    image_height = models.IntegerField(help_text='Maximum height of an image.', default=640)

    thumb_width = models.IntegerField(default=128)
    thumb_height = models.IntegerField(default=128)

    def clean(self):
        validate_only_one_instance(self)

    # On save, apply all nessessary changes to Project and Picture