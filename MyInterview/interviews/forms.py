from django.forms import ModelForm
from models import IvRecord

class NewInterviewForm(ModelForm):
    class Meta:
        model = IvRecord

