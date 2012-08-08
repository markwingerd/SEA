from django.db import models

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
    pub_date = models.DateTimeField(auto_now_add=True)































    """ Will be Depreciated 
class GalleryImage(models.Model):
    def __unicode__(self):
        return self.title
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date uploaded')
"""