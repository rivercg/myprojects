from django.db import models
from jobs.models import Position
from candidates.models import Candidate
from accounts.models import VirtualUser

MSG_MAX_LEN = 500

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
    
