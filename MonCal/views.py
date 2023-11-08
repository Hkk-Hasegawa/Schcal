import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views import generic
from .models import Suresubject, Schedule,Calsetting

class Surelist(generic.ListView):
    model = Suresubject
    ordering = 'name'

class Booking(generic.CreateView):
    model = Schedule
    fields = ('user',)
    template_name = 'MonCal/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        time = self.kwargs.get('time')
        hour=int(time[0:2])
        minute=int(time[3:5])
        print('time:' + time)
        print('hour:' + str(hour))
        print('minute:' + str(minute))
        for calitem in Calsetting.objects.all():
            if str(calitem.subject_name) == str(subject.name):
                timestep=calitem.Step
        start = datetime.datetime(year=year, month=month, day=day, hour=hour,minute= minute)
        if minute + timestep < 59:
            end = datetime.datetime(year=year, month=month , day=day, hour=hour,minute= minute + timestep)
        else:
            end = datetime.datetime(year=year, month=month , day=day, hour=hour+1,minute= minute + timestep - 60)
        print('start:' + str(start))
        print('end:' + str(end))
        if Schedule.objects.filter(subject_name=subject).exclude(Q(start__gt=end) | Q(end__lt=start)).exists():
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
        else:
            schedule = form.save(commit=False)
            schedule.subject_name = subject
            schedule.start = start
            schedule.end = end
            schedule.save()
        return redirect('MonCal:calendar', pk=subject.pk, year=year, month=month, day=day)

class SureCalendar(generic.TemplateView):
    template_name = 'MonCal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        today = datetime.date.today()
        
        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today
        
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        calall=Calsetting.objects.all()
        for calitem in calall:
            if str(calitem.subject_name) == str(subject.name):
                head_time=calitem.head_time
                tail_time=calitem.tail_time
                display_period=calitem.display_period
                timestep=calitem.Step
            
        days = [base_date + datetime.timedelta(days=day) for day in range(display_period)]
        start_day = days[0]
        end_day = days[-1]

        # head_timeからtail_timeまでtimestep分刻み、display_period分の、値がTrueなカレンダーを作る
        calendar = {}
        loop_time= datetime.datetime.combine(start_day, head_time)
        loop_tail= datetime.datetime.combine(start_day,tail_time)
        while loop_time <= loop_tail:
            row = {}
            for day in days:
                row[day] = 'Nothing'
            calkey=str(loop_time.time())
            calkey=calkey[0:5]
            calendar[calkey] = row
            loop_time = loop_time + datetime.timedelta(minutes=timestep)
            
        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day,head_time)
        end_time = datetime.datetime.combine(end_day, tail_time)
        
        for schedule in Schedule.objects.filter(subject_name=subject).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_time = str(local_dt.time())
            booking_time=booking_time[0:5]
            if booking_time in calendar and booking_date in calendar[booking_time]:
                calendar[booking_time][booking_date] = schedule.user
        
        context['subject'] = subject
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=display_period)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        return context