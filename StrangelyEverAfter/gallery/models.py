from django.db import models

# Create your models here.
class Project(models.Model):
    def __unicode__(self):
        return self.project
    project = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date uploaded')

class GalleryImage(models.Model):
    def __unicode__(self):
        return self.title
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date uploaded')