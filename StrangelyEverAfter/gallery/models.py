from django.db import models

from cStringIO import StringIO
from django.core.files.base import ContentFile
import os
from PIL import Image

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
    pub_date = models.DateTimeField('date uploaded')


class Picture(models.Model):
    def __unicode__(self):
        return self.title
    project = models.ForeignKey(Project)
    picture_type = models.CharField(max_length=3, choices=PICTURE_TYPE_CHOICES)
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.ImageField(upload_to='images')
    thumb = models.ImageField(upload_to='images/thumb')
    banner = models.ImageField(upload_to='images/banner')
    pub_date = models.DateTimeField(auto_now_add=True)

    def save(self):
        self.image.save(self.image.name, self.image, save=False)
        self.thumb.save(self.image.name, self.image, save=False)

        imgFile = Image.open(self.image.path)
        fmt = imgFile.format

        #Convert to RGB
        if imgFile.mode not in ('L', 'RGB'):
            imgFile = imgFile.convert('RGB')

        # make sure photo doesn't exceed our max photo size for the site
        resizeImg = imgFile.copy()
        resizeImg.thumbnail(MAX_PHOTO_SIZE, Image.ANTIALIAS)
        updateContent(self.image, self.image.name, resizeImg, fmt)

        thumbImg = imgFile.copy()
        thumbImg.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        updateContent(self.thumb, self.image.name, thumbImg, fmt)

        # Alters image size, then crops.
        if self.picture_type == 'M':
            self.banner.save(self.image.name, self.image, save=False)
            bannerImg = imgFile.copy()
            width, height = bannerImg.size
            multiplier = BANNER_WIDTH / width
            width = int(width * multiplier)
            height = int(height * multiplier)
            print width
            bannerImg = bannerImg.resize((width, height), Image.ANTIALIAS)
            bannerImg = bannerImg.crop(BANNER_CROP)
            bannerImg.load()
            updateContent(self.banner, self.image.name, bannerImg, fmt)

        super(Picture, self).save()