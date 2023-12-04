
from django.conf import settings
from django.db import models


class Schedule(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    subject_name = models.ForeignKey('Suresubject',  verbose_name='予約対象', 
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',
                             on_delete=models.SET_NULL, null=True,blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    cycle_type=models.ForeignKey('Cycle_type', verbose_name='繰り返し区分',
                                on_delete=models.SET_DEFAULT, default=1,)
    detail=models.TextField('詳細',null=True,blank=True)
    def __str__(self):
        start=self.starttime.strftime('%H:%M')
        end=self.endtime.strftime('%H:%M')
        return f'{self.date} {start} ~ {end}：{self.title}'

class EventSchedule(models.Model):
    date=models.DateField('日付',null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    updateuser = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',
                                    on_delete=models.SET_NULL, null=True,blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)    
    cycle_type=models.ForeignKey('Cycle_type', verbose_name='繰り返し区分',
                                on_delete=models.SET_DEFAULT, default=1,)
    cycle_stopday=models.DateField('繰り返し停止日', blank=True,null=True)
    place=models.ManyToManyField('Event', verbose_name='場所')
    room=models.ManyToManyField('Suresubject', verbose_name='設備',blank=True)
    detail=models.TextField('詳細',null=True,blank=True)
    def __str__(self):
        start=self.starttime.strftime('%H:%M')
        end=self.endtime.strftime('%H:%M')
        return f'{self.date} {start} ~ {end}：{self.title}'

class Cycle_pause(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    schedule=models.ForeignKey('EventSchedule', verbose_name='行事予定',
                               on_delete=models.CASCADE)
    pause_type=models.ForeignKey('Pause_type', verbose_name='定期的な予定の削除'
                                 ,on_delete=models.SET_DEFAULT, default=1,)
    updateuser = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',
                                    on_delete=models.SET_NULL, null=True,blank=True)
    
    def __str__(self):
        return f'{self.date} {self.schedule.title}'

class Pause_type(models.Model):
    code=models.CharField('コード',max_length=31)
    name=models.CharField('名前',max_length=31)
    def __str__(self):
        return self.name

class Cycle_type(models.Model):
    code=models.CharField('コード',max_length=31)
    name=models.CharField('名前',max_length=31)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    name=models.CharField('行事区分',max_length=31)
    #pk=2:本社
    #pk=3:岡崎
    def __str__(self):
        return self.name

class Suresubject(models.Model):
    name=models.CharField('対象名',max_length=31)
    subject_type= models.ForeignKey('Subject_type', verbose_name='設備区分',
                                   on_delete=models.SET_NULL, null=True,blank=True)
    def __str__(self):
        return self.name

class Subject_type(models.Model):
    name =models.CharField('区分名',max_length=31)
    #pk=1:本社工場
    #pk=2:岡崎工場
    #pk=3:社用車
    def __str__(self):
        return self.name

class Booking_time(models.Model):
    name=models.CharField('時間名',max_length=31)
    time=models.TimeField('時刻', null=True,blank=True)
    #pk=1:開始時刻
    #pk=2:終了時刻
    def __str__(self):
        return self.name
    
class Working_day(models.Model):
    date=models.DateField('日付')
    weekend_f=models.BooleanField('土日判定',null=True)
    #Trueの時、土日
    def __str__(self):
        return str(self.date)