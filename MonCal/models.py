
from django.db import models


class Schedule(models.Model):
    subject_name=models.CharField(max_length=30)
    date=models.DateField()
    usetime=models.DurationField(blank=True, null=True)
    user=models.CharField(max_length=30)

class Suresubject(models.Model):
    name=models.CharField(max_length=30)
    cal_url=models.TextField()
    def __str__(self):
        return self.name