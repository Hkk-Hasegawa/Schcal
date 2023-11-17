
from django.conf import settings
from django.db import models

class Schedule(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    frame=models.PositiveSmallIntegerField('コマ数', default=1)
    subject_name = models.ForeignKey('Suresubject', verbose_name='予約対象', \
                                     on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',\
                             on_delete=models.CASCADE, null=True,blank=True)
    member = models.ManyToManyField('Person', verbose_name='メンバー', blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    detail=models.TextField('詳細',null=True,blank=True)
    
    def __str__(self):
        start=self.starttime.strftime('%H:%M')
        end=self.endtime.strftime('%H:%M')
        return f'{self.title}：{self.subject_name}：{self.date} {start} ~ {end}'

class Cycle(models.Model):
    schedule= models.OneToOneField('Schedule',on_delete=models.CASCADE,\
                                    verbose_name='スケジュール',null=True)
    step=models.PositiveSmallIntegerField('刻み幅',null=True)
    unit=models.CharField('単位',max_length=8,null=True,blank=True)
    def __str__(self):
        title=self.schedule.title
        start=self.schedule.starttime.strftime('%H:%M')
        end=self.schedule.endtime.strftime('%H:%M')
        return f'{self.step}*{self.unit}：{title} {start} ~ {end}'

class Excludeday(models.Model):
    cycle= models.ForeignKey('Cycle', on_delete=models.CASCADE,\
                             verbose_name='サイクル',null=True)
    date=models.DateField('日付', blank=True,null=True)
    def __str__(self):
        return f'{self.date}：{self.cycle}'

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
    
