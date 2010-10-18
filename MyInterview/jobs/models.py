from django.db import models
import datetime

class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    closed = models.BooleanField('Job closed') 
    responsibility = models.CharField(max_length=2000)
    requirement = models.CharField(max_length=2000)
    preference = models.CharField(max_length=1000, null=True)
    pub_date = models.DateTimeField('Date published')
    close_date = models.DateTimeField('Date closed', blank=True, null=True)

    def __unicode__(self):
        return self.title

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'

