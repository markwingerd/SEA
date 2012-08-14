from django.db import models

from cStringIO import StringIO
from django.core.files.base import ContentFile
import os
from PIL import Image
from datetime import datetime

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

    # Find any other pictures with Master and switch them to Common.
    #  Note: Currently this will magically skip the currently
    #  added/changed picture.
    def switch_common(self):
        picture_list = Picture.objects.filter(project=self.project)
        for p in picture_list:
            if p.picture_type == 'M':
                p.picture_type = 'C'
                p.save()

    def resize_image(self, field, size, source):
        original = Image.open(source.path)
        fmt = original.format
        img = original.copy()
        img.thumbnail(size, Image.ANTIALIAS)
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


    def save(self):
        self.image.save(self.image.name, self.image, save=False)
        self.thumb.save(self.image.name, self.image, save=False)
        if self.picture_type == 'M':
            self.crop_image(self.project.banner, self.image, BANNER_WIDTH, BANNER_CROP)
            self.switch_common()
        self.resize_image(self.image, MAX_PHOTO_SIZE, self.image)
        self.resize_image(self.thumb, THUMBNAIL_SIZE, self.image)

        super(Picture, self).save()