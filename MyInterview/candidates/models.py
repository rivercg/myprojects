from django.db import models
from random import choice
import datetime

CANDIDATE_FEATURE_NA = 0;
CANDIDATE_FEATURE_ACC = 1;
CANDIDATE_FEATURE_ASC = 2;
CANDIDATE_FEATURE_UR = 3;

CF_LINK_DIGEST_LEN = 8; 

class FeatureDoesNotExist(Exception):
    pass

class FeatureStatusDoesNotExist(Exception):
    pass

class FeatureLinkExpired(Exception):
    pass

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

CFL_STATUS_CHOICES = (
    ('W', 'Wait'),
    ('C', 'Closed'),
    ('T', 'True'),
    ('F', 'False'),
    ('U', 'Updated'),
)

CFL_STATUS_CHOICESET = 'WCTFU'
CFL_STATUS_PUBLIC_CHOICESET = 'TFU'

def is_public_cfl_status(st):
    return (st in CFL_STATUS_PUBLIC_CHOICESET)

class CandidateFeatureLink(models.Model):
    candidate = models.OneToOneField(Candidate)
    link_digest = models.CharField(unique=True,max_length=16)
    status = models.CharField(max_length=1, choices=CFL_STATUS_CHOICES)
    mod_date = models.DateTimeField('last modify date')
    
    class Meta:
        abstract = True 
        
    def feature_index(self):
        return CANDIDATE_FEATURE_NA
    
    def is_waiting(self):
        return self.status == 'W'

    def is_closed(self):
        return self.status == 'C'
    
    def can_update_status(self, st):
        return self.is_waiting() and (st in ['', 'T', 'F'])
    
    def update_status(self, st):
        if not (st in CFL_STATUS_CHOICESET):
            raise FeatureStatusDoesNotExist
        self.status = st
        self.mod_date = datetime.datetime.now()
        self.save()
        
    def close_it(self):
        self.update_status('C')
        
    def reset_it(self):
        self.update_status('W')

class CandidateAckContactLink(CandidateFeatureLink):
    class Meta(CandidateFeatureLink.Meta):
        db_table = 'candidates_ackcontact_link'

    def feature_index(self):
        return CANDIDATE_FEATURE_ACC
        
class CandidateAckSchduleLink(CandidateFeatureLink):
    class Meta(CandidateFeatureLink.Meta):
        db_table = 'candidates_ackscedule_link'

    def feature_index(self):
        return CANDIDATE_FEATURE_ASC
        
class CandidateUpdateResumeLink(CandidateFeatureLink):
    class Meta(CandidateFeatureLink.Meta):
        db_table = 'candidates_updateresume_link'

    def feature_index(self):
        return CANDIDATE_FEATURE_UR

    def can_update_status(self, st):
        return (not self.is_closed()) and (st in ['', 'U'])
   
def random_digest(fea_class, len=CF_LINK_DIGEST_LEN):
    while True:
        digest = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(len)])
        try:
            fea_class.objects.all().get(link_digest=digest)
        except fea_class.DoesNotExist:
            return  digest
   
CANDIDATE_FEATURE_DEFNITIONS_NAMES = ('fea_index', 'fea_key', 'fea_desc', 'fea_class')               
               
CANDIDATE_FEATURE_DEFNITIONS = (
    (CANDIDATE_FEATURE_ACC, 'ACC', 'Acknowledge contact continue', CandidateAckContactLink),
    (CANDIDATE_FEATURE_ASC, 'ASC', 'Acknowledge schedule continue', CandidateAckSchduleLink),
    (CANDIDATE_FEATURE_UR, 'UR', 'Update resume', CandidateUpdateResumeLink),
)
 
def get_feature_defset(feature_id):
    for defset in CANDIDATE_FEATURE_DEFNITIONS:
        if (defset[1] == feature_id):
            d = {}
            for i, key in enumerate(CANDIDATE_FEATURE_DEFNITIONS_NAMES):
                d[key] = defset[i]
            return d
    raise FeatureDoesNotExist

def get_feature_defset_byindex(feature_index):
    for defset in CANDIDATE_FEATURE_DEFNITIONS:
        if (defset[0] == feature_index):
            d = {}
            for i, key in enumerate(CANDIDATE_FEATURE_DEFNITIONS_NAMES):
                d[key] = defset[i]
            return d
    raise FeatureDoesNotExist
