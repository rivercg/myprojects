from django.db import models
from django.contrib.auth.models import User;
from jobs.models import Position
from candidates.models import Candidate

MSG_MAX_LEN = 500

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

class IvRecord(models.Model):
    position = models.ForeignKey(Position)
    candidate = models.OneToOneField(Candidate)
    STATUS_CHOICES = (
        ('Open', 'Record open'),
        ('Closed', 'Record closed'),
        ('Scheduled', 'Interview scheduled'),
        ('Check-in', 'Interview check-in'),
        ('Canceled', 'Interview canceled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    open_date = models.DateTimeField('date opened')
    close_date = models.DateTimeField('date closed', blank=True, null=True)
    
    def __unicode__(self):
        return self.candidate.name() + ' => ' + self.position.title
        #return  self.position 
    
class Message(models.Model):
    iv_record = models.ForeignKey(IvRecord)
    send_from = models.ForeignKey(VirtualUser)
    text = models.CharField(max_length=MSG_MAX_LEN)
    pub_date = models.DateTimeField('date published')
    
    def degist_text(self):
        return self.text
    
    def __unicode__(self):
        return self.degist_text()
    
    def ivrecord_pk(self):
        return self.iv_record.pk
    
    def ivrecord_position(self):
        return self.iv_record.position
    
    def ivrecord_candidate(self):
        return self.iv_record.candidate
    
    def ivrecord_status(self):
        return self.iv_record.status
    
    def sendfrom_pk(self):
        return self.send_from.pk
    
    def sendfrom_role(self):
        return self.send_from.role 

    def sendfrom_username(self):
        return self.send_from.user_name()
    
    def sendfrom_dispname(self):
        return self.send_from.disp_name()
    
    def sendfrom_email(self):
        return self.send_from.email()
    
