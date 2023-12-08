
from .models import Schedule,EventSchedule,Suresubject
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class Scheduleform(forms.ModelForm):
    starttime = forms.ChoiceField(label='開始時間')
    endtime = forms.ChoiceField(label='終了時間')
    class Meta:
        model =Schedule
        fields = ('date','starttime','endtime','title','detail')
        widgets = {'date': AdminDateWidget()}
    
    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["starttime"].choices = categories
        self.base_fields["endtime"].choices = categories
        super().__init__(*args, **kwargs)

class AllScheduleform(forms.ModelForm):
    starttime = forms.ChoiceField(label='開始時間')
    endtime = forms.ChoiceField(label='終了時間')
    subject = forms.ChoiceField(label='社用車名')
    class Meta:
        model =Schedule
        fields = ('date','starttime','endtime','subject','title','detail')
        widgets = {'date': AdminDateWidget()}
    
    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["starttime"].choices =  categories['time']
        self.base_fields["endtime"].choices =  categories['time']
        self.base_fields["subject"].choices = categories['subject']
        super().__init__(*args, **kwargs)


class EventScheduleform(forms.ModelForm):
    starttime = forms.ChoiceField(label='開始時間')
    endtime = forms.ChoiceField(label='終了時間')
    
    room= forms.MultipleChoiceField(label='設備',widget=forms.CheckboxSelectMultiple,required=False,)
    place= forms.MultipleChoiceField(label='場所',widget=forms.CheckboxSelectMultiple,required=True)
    class Meta:
        model =EventSchedule
        fields = ('date','starttime','endtime','cycle_type' ,'place','room','title','detail')
        widgets = {'date': AdminDateWidget()}
    
    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["starttime"].choices = categories['time']
        self.base_fields["endtime"].choices = categories['time']
        self.base_fields["room"].choices = categories['room']
        self.base_fields["place"].choices = categories['place']
        super().__init__(*args, **kwargs)

