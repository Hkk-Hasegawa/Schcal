
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
    member = models.ManyToManyField('Person', verbose_name='メンバー',  blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    detail=models.TextField('詳細',null=True,blank=True)
    cycle=models.CharField('繰り返し',max_length=15,default='nocycle')
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
class Suresubject(models.Model):
    name=models.CharField('対象名',max_length=31)
    head_time=models.TimeField('受付開始時間', null=True)
    tail_time=models.TimeField('受付終了時間', null=True)
    display_period=models.PositiveSmallIntegerField('表示期間',default=7)
    Step=models.PositiveSmallIntegerField('刻み幅（分）',default=30)
    def __str__(self):
        return self.name

class Person(models.Model):
    name=models.CharField('名前',max_length=31, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='ユーザー',\
                             on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    
