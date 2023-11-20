
from .models import Schedule,Cycle
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from betterforms.multiform import MultiModelForm

class MultiScheduleform(forms.ModelForm):
    starttime = forms.ChoiceField(label='開始時間')
    endtime = forms.ChoiceField(label='終了時間')
    
    class Meta:
        model =Schedule
        fields = ('title','date','starttime','endtime','detail')
        
        widgets = {'date': AdminDateWidget()}
    
    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["starttime"].choices = categories[0]
        self.base_fields["endtime"].choices = categories[0]
        super().__init__(*args, **kwargs)

class MultiCycleform(forms.ModelForm):
    unit= forms.ChoiceField(choices=(('week', 'week')),label='単位')
    
    class Meta:
        model = Cycle
        fields=('step','unit')

    def __init__(self, categories=None, *args, **kwargs):
        self.base_fields["unit"].choices = categories[1]
        super().__init__(*args, **kwargs)

class ProductMultiForm(MultiModelForm):

    form_classes = {
        "schedule_form": MultiScheduleform,
        "cycle_form": MultiCycleform,
    }
