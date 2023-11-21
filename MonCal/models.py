
from django.conf import settings
from django.db import models

class Schedule(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    subject_name = models.ForeignKey('Suresubject', verbose_name='予約対象', \
                                     on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',\
                             on_delete=models.CASCADE, null=True,blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    cycle=models.CharField('繰り返し',max_length=15,default='nocycle')
    detail=models.TextField('詳細',null=True,blank=True)
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
    Event = models.ForeignKey('Event', verbose_name='予約対象', \
                                     on_delete=models.CASCADE)
    updateuser = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',\
                             on_delete=models.CASCADE, null=True,blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    detail=models.TextField('詳細',null=True,blank=True)
    subject=models.ForeignKey('Suresubject', verbose_name='利用設備', \
                                     on_delete=models.CASCADE, null=True,blank=True)
    
    def __str__(self):
        start=self.starttime.strftime('%H:%M')
        end=self.endtime.strftime('%H:%M')
        return f'{self.title}：{self.date} {start} ~ {end}'
        
class Event(models.Model):
    name=models.CharField('行事区分',max_length=31)
    head_time=models.TimeField('受付開始時間', null=True)
    tail_time=models.TimeField('受付終了時間', null=True)
    def __str__(self):
        return self.name

class Suresubject(models.Model):
    name=models.CharField('対象名',max_length=31)
    subjectclass=models.CharField('区分',max_length=31, null=True)
    head_time=models.TimeField('受付開始時間', null=True)
    tail_time=models.TimeField('受付終了時間', null=True)
    def __str__(self):
        return self.name

class Person(models.Model):
    name=models.CharField('名前',max_length=31, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='ユーザー',\
                             on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    
class weekday(models.Model):
    ja_name=models.CharField('名前',max_length=31, null=True)
    weeklynum=models.SmallIntegerField('コード上の数値',default=0)

