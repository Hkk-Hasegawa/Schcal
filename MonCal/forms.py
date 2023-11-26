
from .models import Schedule,EventSchedule,Suresubject
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class Scheduleform(forms.ModelForm):
    starttime = forms.ChoiceField(label='開始時間')
    endtime = forms.ChoiceField(label='終了時間')
    cycle= forms.ChoiceField(label='繰り返し')
    class Meta:
        model =Schedule
        fields = ('title','date','starttime','endtime','cycle','detail')
        widgets = {'date': AdminDateWidget()}
    
    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["starttime"].choices = categories
        self.base_fields["endtime"].choices = categories
        self.base_fields["cycle"].choices = [('nocycle','繰り返さない'),('week','毎週')]
        super().__init__(*args, **kwargs)




class EventScheduleform(forms.ModelForm):
    starttime = forms.ChoiceField(label='開始時間')
    endtime = forms.ChoiceField(label='終了時間')
    cycle= forms.ChoiceField(label='繰り返し')
    subject_pk= forms.ChoiceField(label='設備利用')
    class Meta:
        model =EventSchedule
        fields = ('title','date','starttime','endtime','subject_pk','cycle','detail')
        widgets = {'date': AdminDateWidget()}
    
    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["starttime"].choices = categories['time']
        self.base_fields["endtime"].choices = categories['time']
        self.base_fields["cycle"].choices =categories['cycle']
        self.base_fields["subject_pk"].choices = categories['room']
        super().__init__(*args, **kwargs)

