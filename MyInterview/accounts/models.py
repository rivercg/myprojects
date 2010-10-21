from django.db import models
from django.contrib.auth.models import User;

class VirtualUser(models.Model):
    real_user = models.OneToOneField(User)
    ROLE_CHOICES = (
        ('sys', 'System'),
        ('hr', 'HR'),
        ('ivr', 'Interviewer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def __unicode__(self):
        return self.user_name() 

    def user_name(self):
        return self.real_user.username 
    
    def username_pk(self):
        return self.real_user.pk  
    
    def email(self):
        return self.real_user.email
    
    def last_login(self):
        return self.real_user.last_login
    
    def first_name(self):
        return self.real_user.first_name
    
    def last_name(self):
        return self.real_user.last_name
    
    def disp_name(self):
        return self.first_name() + ' ' + self.last_name()

