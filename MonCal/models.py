
from django.conf import settings
from django.db import models



class Schedule(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    subject_name = models.ForeignKey('Suresubject', 
                                     verbose_name='予約対象', 
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',
                             on_delete=models.SET_NULL, null=True,blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    cycle=models.CharField('繰り返し',max_length=15,default='nocycle')
    detail=models.TextField('詳細',null=True,blank=True)
    subschedule= models.ForeignKey('EventSchedule', verbose_name='行事スケジュール',
                                   on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        start=self.starttime.strftime('%H:%M')
        end=self.endtime.strftime('%H:%M')
        if self.cycle=='nocycle':
            return f'{self.title}：{self.date} {start} ~ {end}'
        elif self.cycle=='week':
            weekday=self.date.weekday()
            weekday=weekdaychinge(weekday)
            return f'{self.title}：毎週{weekday}曜日{start} ~ {end}'

def weekdaychinge(weekday):
    if weekday == 0:
        return('月')
    elif weekday==1:
        return('火')
    elif weekday==2:
        return('水')
    elif weekday==3:
        return('木')
    elif weekday==4:
        return('金')
    elif weekday==5:
        return('土')
    elif weekday==6:
        return('日')

class EventSchedule(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    event = models.ForeignKey('Event', verbose_name='予約対象',
                                     on_delete=models.CASCADE)
    updateuser = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',
                                    on_delete=models.SET_NULL, null=True,blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    cycle=models.CharField('繰り返し',max_length=15,default='nocycle')
    detail=models.TextField('詳細',null=True,blank=True)
    subject_pk=models.PositiveBigIntegerField('利用設備',default=0)
    subschedule= models.ForeignKey('Schedule', verbose_name='設備スケジュール',
                                   on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        start=self.starttime.strftime('%H:%M')
        end=self.endtime.strftime('%H:%M')
        return f'{self.title}：{self.date} {start} ~ {end}'

class Event(models.Model):
    name=models.CharField('行事区分',max_length=31)
    subject_type= models.ForeignKey('Subject_type', verbose_name='設備区分',
                                   on_delete=models.SET_NULL, null=True,blank=True)
    #pk=1:全体行事
    #pk=2:本社行事
    #pk=3:岡崎工場
    def __str__(self):
        return self.name

class Suresubject(models.Model):
    name=models.CharField('対象名',max_length=31)
    subject_type= models.ForeignKey('Subject_type', verbose_name='設備区分',
                                   on_delete=models.SET_NULL, null=True,blank=True)
    subjectclass=models.CharField('区分',max_length=31, null=True)

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