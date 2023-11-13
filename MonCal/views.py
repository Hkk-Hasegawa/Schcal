from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy
from .models import Suresubject, Schedule,Person
from .forms import Scheduleform
import datetime
User = get_user_model()

#管理者か判定
class OnlyUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.kwargs['pk'] == self.request.user.pk or self.request.user.is_superuser
#予約対象一覧ページ
class Surelist(LoginRequiredMixin,generic.ListView):
    model = Suresubject
    ordering = 'name'
#マイページ
class MyPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/my_page.html'
    #直近の予定を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.datetime.combine( datetime.date.today(),datetime.time())
        sch= Schedule.objects.filter(Q(user=self.request.user)|Q(member__user=self.request.user),start__gte=dt_today).order_by('start')
        context['schedule_list'] = sch.distinct()
        return context
#管理者用利用者のマイページ
class MyPageWithPk(OnlyUserMixin, generic.TemplateView):
    template_name = 'MonCal/my_page.html'
    #直近の予定を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        dt_today =datetime.datetime.combine( datetime.date.today(),datetime.time())
        sch=Schedule.objects.filter(Q(user__pk=self.kwargs['pk'])|Q(member__user__pk=self.kwargs['pk']), start__gte=dt_today).order_by('start')
        context['schedule_list'] =sch.distinct()
        return context
#予約カレンダーページ
class SureCalendar(LoginRequiredMixin,generic.CreateView):
    model = Schedule
    form_class=Scheduleform
    template_name = 'MonCal/calendar.html'
    #カレンダーの作成
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
        context=makecalendar(subject,base_date,context)
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        kwgs["categories"] = choicetime(subject)
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        start=datetime.datetime.combine(schedule.date, schedule.starttime)
        end=datetime.datetime.combine(schedule.date, schedule.endtime) - datetime.timedelta(minutes=1)
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
        elif Schedule.objects.filter(subject_name=subject).exclude(Q(start__gt=end) | Q(end__lt=start)).exists():
        #elif True:
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
        else:
            schedule.subject_name = subject
            schedule.user= self.request.user
            schedule.start = start
            schedule.end = end
            schedule.save()                
            form.save_m2m() 
        return redirect('MonCal:calendar', pk=subject.pk)
#スケジュールの詳細ページ
class EventDetail(LoginRequiredMixin,generic.TemplateView):
    template_name = 'MonCal/Event_detail.html'
    #スケジュールの情報を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        host=Person.objects.get(user=event.user)
        context['event']=event
        context['host']=host
        context['user']=self.request.user
        return context
#スケジュールの編集
class EventEdit(LoginRequiredMixin,generic.UpdateView):
    model = Schedule
    form_class=Scheduleform
    template_name = 'MonCal/Event_edit.html'
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject=event.subject_name
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date=event.date
        context=makecalendar(subject,base_date,context)
        context['event']=event
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject=schedule.subject_name
        kwgs["categories"] = choicetime(subject)
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        schedule = form.save(commit=False)
        subject=schedule.subject_name 
        start=datetime.datetime.combine(schedule.date, schedule.starttime)
        end=datetime.datetime.combine(schedule.date, schedule.endtime) - datetime.timedelta(minutes=1)
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            return redirect('MonCal:Event_edit', pk=schedule.pk)
        elif Schedule.objects.filter(subject_name=subject).exclude(Q(start__gt=end) | Q(end__lt=start)| Q(pk=schedule.pk)).exists():
        #elif True:
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
            return redirect('MonCal:Event_edit', pk=schedule.pk)
        else:
            schedule.user= self.request.user
            schedule.start = start
            schedule.end = end
            schedule.save()                
            form.save_m2m() 
            return redirect('MonCal:Event_detail', pk=schedule.pk)
#スケジュールの削除
class EventDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    success_url = reverse_lazy('MonCal:my_page')
#時刻の選択肢作成
def choicetime(subject):
    looptime=subject.head_time
    today = datetime.date.today()
    choicelist=[]     
    while looptime <= subject.tail_time:
        choicelist.append((looptime,looptime))
        loopdate=datetime.datetime.combine(today, looptime)
        loopdate=loopdate + datetime.timedelta(minutes=subject.Step)
        looptime=loopdate.time()
    category_choice = tuple(choicelist)
    return(category_choice)
#カレンダー作成
def makecalendar(subject,base_date,context):
    head_time=subject.head_time
    tail_time=subject.tail_time
    display_period=subject.display_period
    timestep=subject.Step
    days = [base_date + datetime.timedelta(days=day) for day in range(display_period)]
    start_day = days[0]
    end_day = days[-1]
    # head_timeからtail_timeまでtimestep分刻み、display_period分の、値がTrueなカレンダーを作る
    calendar = {}
    loop_time= datetime.datetime.combine(start_day, head_time)
    loop_tail= datetime.datetime.combine(start_day,tail_time)
    while loop_time < loop_tail:
        row = {}
        for day in days:
            row[day] = 'Nothing'
        calendar[loop_time.time()] = row
        loop_time = loop_time + datetime.timedelta(minutes=timestep)    
    # カレンダー表示する最初と最後の日時の間にある予約を取得する
    start_time = datetime.datetime.combine(start_day,head_time)
    end_time = datetime.datetime.combine(end_day, tail_time)
        
    for schedule in Schedule.objects.filter(subject_name=subject).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
        local_dt = timezone.localtime(schedule.start)
        booking_date = local_dt.date()
        int_time=local_dt.time()
        booking_time = int_time
        if booking_time in calendar and booking_date in calendar[booking_time]:   
            calendar[booking_time][booking_date] = schedule
            int_time=datetime.datetime.combine(booking_date, int_time)
            whileboolen=True
            while whileboolen:
                int_time=int_time + datetime.timedelta(minutes=timestep)
                print(int_time)
                endtime=timezone.localtime(schedule.end)
                print(endtime)
                if int_time.time() < endtime.time():
                    booking_time=int_time.time()
                    calendar[booking_time][booking_date] = 'same'
                else:
                    whileboolen=False
    caldic={'calendar':calendar,'days':days,'start_day':start_day,'end_day':end_day}
    context['subject'] =subject
    context['calendar'] =caldic['calendar'] 
    context['days'] = caldic['days']
    context['start_day'] =caldic['start_day']
    context['end_day'] = caldic['end_day']
    context['before'] = caldic['days'][0] - datetime.timedelta(days=subject.display_period)
    context['next'] = caldic['days'][-1] + datetime.timedelta(days=1)
    context['today'] = datetime.date.today()
    return(context)