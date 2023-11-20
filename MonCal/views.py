
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django import forms
from .models import Suresubject, Schedule,Person,Cycle
from .forms import ProductMultiForm
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
        context=myschedule(context,self.request.user.pk)
        return context
#管理者用利用者のマイページ
class MyPageWithPk(OnlyUserMixin, generic.TemplateView):
    template_name = 'MonCal/my_page.html'
    #直近の予定を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        context=myschedule(context,self.kwargs['pk'])
        return context
#予約カレンダーページ
class SureCalendar(LoginRequiredMixin,generic.CreateView):
    model = Schedule
    form_class=ProductMultiForm
    template_name = 'MonCal/calendar.html'
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        # どの日を基準にカレンダーを表示するかの処理。年月日の指定がなければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date =  datetime.date.today()
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        context=makecalendar(subject,base_date,context)
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        ls=[('week','週'),('month','月')]
        kwgs["categories"] = choicetime(subject),ls
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        end=datetime.datetime.combine(schedule.date, schedule.endtime) - datetime.timedelta(minutes=1)
        schedule.endtime=end.time()
        cyboolen=False
        for cysche in cyclejudge(subject,schedule.date):
            if cysche.starttime <= schedule.endtime or cysche.endtime <= schedule.starttime:
                cyboolen=True
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
        elif  Schedule.objects.filter(date=schedule.date,subject_name=subject)\
                        .exclude(Q(starttime__gt= schedule.endtime) | \
                                 Q(endtime__lt=schedule.starttime)| Q(pk=schedule.pk)).exists()\
                or cyboolen:
            messages.error(self.request, 'すでに予約がありました。')
        else:
            schedule.subject_name = subject
            schedule.user= self.request.user
            schedule.save()                
            form.save_m2m() 
            
        return redirect('MonCal:calendar', pk=subject.pk,year=schedule.date.year,month=schedule.date.month,day=schedule.date.day)
#スケジュールの編集
class EventEdit(LoginRequiredMixin,generic.UpdateView):
    model = Schedule
    form_class=ProductMultiForm
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
        ls=[('week','週'),('month','月')]
        kwgs["categories"] = choicetime(subject),ls
    #フォームの保存
    def form_valid(self, form):
        schedule = form.save(commit=False)
        subject=schedule.subject_name 
        end=datetime.datetime.combine(schedule.date, schedule.endtime) - datetime.timedelta(minutes=1)
        schedule.endtime=end.time()
        cyboolen=False
        for cysche in cyclejudge(subject,schedule.date):
            if cysche.starttime <= schedule.endtime or cysche.endtime <= schedule.starttime:
                cyboolen=True
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            return redirect('MonCal:Event_edit', pk=schedule.pk)
        elif Schedule.objects.filter(date=schedule.date,subject_name=subject)\
                .exclude(Q(starttime__gt= schedule.endtime)| Q(endtime__lt=schedule.starttime)| Q(pk=schedule.pk)).exists() or cyboolen:
            messages.error(self.request, 'すでに予約がありました。')
            return redirect('MonCal:Event_edit', pk=schedule.pk)
        else:
            schedule.user= self.request.user
            schedule.save()                
            form.save_m2m() 
            return redirect('MonCal:Event_detail', pk=schedule.pk)
#スケジュールの詳細ページ
class EventDetail(LoginRequiredMixin,generic.TemplateView):
    template_name = 'MonCal/Event_detail.html'
    #スケジュールの情報を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        host=Person.objects.get(user=event.user)
        context['Boolen']=Cycle.objects.filter(schedule=event)
        context['event']=event
        context['host']=host
        context['user']=self.request.user
        return context
#スケジュールの削除
class EventDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    success_url = reverse_lazy('MonCal:my_page')
#繰り返しの削除
class CycleDelete(LoginRequiredMixin, generic.DeleteView):
    model = Cycle
    success_url = reverse_lazy('MonCal:my_page')

#予定一覧
def myschedule(context,usrpk):
    #単発予定リスト
    dt_today =datetime.date.today()
    dt_nextmon=dt_today  + datetime.timedelta(days=30)  
    schedule= Schedule.objects.filter(user__pk=usrpk,\
                                      date__gte=dt_today,date__lte=dt_nextmon).order_by('date','starttime')
    context['schedule_list'] = schedule.distinct()
    #定期予定リスト
    #cydic={}
    #for cycle in Cycle.objects.filter(Q(schedule__user__pk=usrpk))\
                                #.exclude(schedule__date__gte=dt_today,schedule__date__lte=dt_nextmon):
        #cyshce=cycle.schedule
        #cy_dt=datetime.datetime.combine(cyshce.date, cyshce.starttime)
        #cydic[cy_dt]=cyshce
        #context['cycle_list']
    return context
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
#繰り返し予定の判定
def cyclejudge(subject,date):
    rt=[]
    for cycle in Cycle.objects.filter(schedule__subject_name=subject,\
                                      schedule__date__lte=date):
            if cycle.unit == 'week':
                step=7 * cycle.step
                unit='day'
            elif cycle.unit == 'year':
                step=12 * cycle.step
                unit='month'
            else:
                step=1 * cycle.step
                unit=cycle.unit
            cysche_date=cycle.schedule.date
            
            if unit =='day' :
                daysdiff=(date-cysche_date).days
                if (daysdiff % step) == 0:
                    rt.append(cycle.schedule)

    return(rt)
#カレンダー作成
def makecalendar(subject,base_date,context):
    head_time=subject.head_time
    tail_time=subject.tail_time
    display_period=subject.display_period
    timestep=subject.Step
    days = [base_date + datetime.timedelta(days=day) for day in range(display_period)]
    start_day = days[0]
    end_day = days[-1]
    # head_timeからtail_timeまでtimestep分刻み、display_period分の、値がNothingなカレンダーを作る
    calendar = {}
    loop_time= datetime.datetime.combine(start_day, head_time)
    loop_tail= datetime.datetime.combine(start_day,tail_time)
    while loop_time < loop_tail:
        row = {}
        for day in days:
            row[day] = 'Nothing'
        calendar[loop_time.time()] = row
        loop_time = loop_time + datetime.timedelta(minutes=timestep) 
    for day in days: 
        for cycle_sche in cyclejudge(subject,day):
            calendar=scheincal(calendar,cycle_sche,day)
                
    # カレンダー表示する最初と最後の日時の間にある予約を取得する
    for schedule in Schedule.objects.filter(subject_name=subject)\
                        .exclude(Q(date__gt=end_day) | Q(date__lt=start_day)):
        if schedule.starttime in calendar and schedule.date in calendar[schedule.starttime]: 
            calendar=scheincal(calendar,schedule,schedule.date)  
    context['subject'] =subject
    context['calendar'] =calendar
    context['days'] = days
    context['start_day'] =start_day
    context['end_day'] = end_day
    context['before'] = context['days'][0] - datetime.timedelta(days=subject.display_period)
    context['next'] = context['days'][-1] + datetime.timedelta(days=1)
    context['today'] = datetime.date.today()
    return(context)
#カレンダーに予定を入力
def scheincal(calendar,schedule,date):
    booking_date = date
    booking_time = schedule.starttime
    subject=schedule.subject_name
    timestep=subject.Step
    calendar[booking_time][booking_date] = schedule
    int_time=datetime.datetime.combine(booking_date, schedule.starttime)
    whileboolen=True
    while whileboolen:
        int_time=int_time + datetime.timedelta(minutes=timestep)
        if int_time.time() < schedule.endtime:
            booking_time=int_time.time()
            calendar[booking_time][booking_date] = 'same'
        else:
            whileboolen=False
    return(calendar)