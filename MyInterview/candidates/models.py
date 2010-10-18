from django.db import models

class Candidate(models.Model):
    last_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(null=True)
    married = models.NullBooleanField(null=True)
    hukou = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    email = models.CharField('Email', max_length=100, null=True)
    phone = models.CharField('Phone', max_length=20, null=True)
    cell_phone = models.CharField('Cell phone', max_length=20, null=True)
    create_date = models.DateTimeField('Date created')

    def name(self):
        return self.last_name + ' ' + self.first_name
    
    def __unicode__(self):
        return self.name()
