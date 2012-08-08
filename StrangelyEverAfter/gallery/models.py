from django.db import models
###
import urllib2, urlparse
from django.core.files.base import ContentFile
###

PICTURE_TYPE_CHOICES = (
    ('IMG', 'Image'),
    ('ICN', 'Icon'),
    ('BNR', 'Banner'),
)

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
    thumb = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        """
        Retrieve an image from some url and save it to the image field,
        before saving the model to the database
        """
        image_url = "http://www.strangelyeverafter.com/image/boarder.png" # get this url from somewhere
        image_data = urllib2.urlopen(image_url, timeout=5)
        filename = urlparse.urlparse(image_data.geturl()).path.split('/')[-1]
        self.thumb = filename
        self.thumb.save(
            filename,
            ContentFile(image_data.read()),
            save=False
        )
        super(Picture, self).save(*args, **kwargs)