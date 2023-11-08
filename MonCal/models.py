
from django.db import models
from django.utils import timezone

class Schedule(models.Model):
    start = models.DateTimeField('開始時間', null=True)
    end = models.DateTimeField('終了時間', null=True)
    user=models.CharField('予約者名',max_length=31)
    subject_name = models.ForeignKey('Suresubject', verbose_name='予約対象', \
                                     on_delete=models.CASCADE)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.user} {start} ~ {end} {self.subject_name}'

class Suresubject(models.Model):
    name=models.CharField('対象名',max_length=31)
    cal_url=models.TextField()
    def __str__(self):
        return self.name

class Calsetting(models.Model):
    subject_name = models.ForeignKey('Suresubject', verbose_name='予約対象', \
                                     on_delete=models.CASCADE,unique=True)
    head_time=models.TimeField('受付開始時間')
    tail_time=models.TimeField('受付終了時間')
    display_period=models.PositiveSmallIntegerField('表示期間')
    Step=models.PositiveSmallIntegerField('刻み幅（分）')
    def __str__(self):
        return str(self.subject_name)