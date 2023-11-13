
from django.conf import settings
from django.db import models
from django.utils import timezone

class Schedule(models.Model):
    date=models.DateField('日付', blank=True,null=True)
    starttime=models.TimeField('開始時刻', blank=True,null=True)
    endtime=models.TimeField('終了時刻', blank=True,null=True)
    start = models.DateTimeField( null=True)
    end = models.DateTimeField( null=True)
    frame=models.PositiveSmallIntegerField('コマ数', default=1)
    subject_name = models.ForeignKey('Suresubject', verbose_name='予約対象', \
                                     on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー',\
                             on_delete=models.CASCADE, null=True)
    member = models.ManyToManyField('Person', verbose_name='メンバー', blank=True)
    title=models.CharField('タイトル',max_length=31, null=True)
    detail=models.TextField('詳細',null=True,blank=True)
    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.title}:{start} ~ {end} {self.subject_name}'

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
    
