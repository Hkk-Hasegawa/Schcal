
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from .models import Suresubject, Schedule,Person,Event,EventSchedule
from .forms import Scheduleform,EventScheduleform
import datetime
User = get_user_model()
#ホームページ
class HomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/home_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject_list']= Suresubject.objects.all()
        context['event_list']= Event.objects.all()
        return context

#予約対象ごとの直近の予定
class PropertyList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/Property_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        dt_nextmon=dt_today  + datetime.timedelta(days=30) 
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule=Schedule.objects.filter(subject_name=subject,date__gte=dt_today,\
                     date__lte=dt_nextmon,cycle='nocycle').order_by('date','starttime')
        cyschedule=Schedule.objects.filter(subject_name=subject,date__lte=dt_nextmon)\
                    .exclude(cycle='nocycle').order_by('date','starttime')
        context['single_list'] = schedule.distinct()
        context['cycle_list'] = cyschedule.distinct()
        context['subject']=subject
        return context
#予約カレンダーページ
class PropertyCalendar(LoginRequiredMixin,generic.CreateView):
    model = Schedule
    form_class=Scheduleform
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
        kwgs["categories"] = choicetime(subject)
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        date=schedule.date
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
        elif  Schedule.objects.filter(date=schedule.date,subject_name=subject,cycle='nocycle')\
                        .exclude(Q(starttime__gte= schedule.endtime) | \
                                 Q(endtime__lte=schedule.starttime)| Q(pk=schedule.pk)).exists()\
                or cyclebooking(schedule,subject) or newcyclecheck(schedule,subject):
            
            messages.error(self.request, 'すでに予約がありました。')
        else:
            schedule.subject_name = subject
            schedule.user= self.request.user
            schedule.save()                
            form.save_m2m() 
        return redirect('MonCal:calendar', pk=subject.pk,year=date.year,month=date.month,day=date.day)
#設備予約の詳細ページ
class PropertyDetail(LoginRequiredMixin,generic.TemplateView):
    template_name = 'MonCal/Property_detail.html'
    #スケジュールの情報を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        host=Person.objects.get(user=event.user)
        context['event']=event
        context['host']=host
        context['user']=self.request.user
        return context
    #フォームの保存
#設備予約の編集
class PropertyEdit(LoginRequiredMixin,generic.UpdateView):
    model = Schedule
    form_class=Scheduleform
    template_name = 'MonCal/Property_edit.html'
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
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            return redirect('MonCal:Property_edit', pk=schedule.pk)
        elif Schedule.objects.filter(date=schedule.date,subject_name=subject)\
                .exclude(Q(starttime__gte= schedule.endtime)| Q(endtime__lte=schedule.starttime)| Q(pk=schedule.pk)).exists() \
            or cyclebooking(schedule,subject) or newcyclecheck(schedule,subject):
            messages.error(self.request, 'すでに予約がありました。')
            return redirect('MonCal:Property_edit', pk=schedule.pk)
        else:
            schedule.user= self.request.user
            schedule.save()                
            form.save_m2m() 
            return redirect('MonCal:Property_edit', pk=schedule.pk)
#設備予約の削除
class PropertyDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    success_url = reverse_lazy('MonCal:home_page')    

#予約カレンダーページ
class EventCalendar(LoginRequiredMixin,generic.CreateView):
    model = Event
    form_class=EventScheduleform
    template_name = 'MonCal/Eventcalendar.html'
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        # どの日を基準にカレンダーを表示するかの処理。年月日の指定がなければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date =  datetime.date.today()
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        head_time=event.head_time
        tail_time=event.tail_time
        display_period=7
        timestep=30
        days = [base_date + datetime.timedelta(days=day) for day in range(display_period)]
        start_day = days[0]
        end_day = days[-1]
        loop_tail= datetime.datetime.combine(start_day,tail_time)
        loop_time= datetime.datetime.combine(start_day, head_time)
        times=[]
        while loop_time < loop_tail:
            times.append(loop_time.time())
            loop_time = loop_time + datetime.timedelta(minutes=timestep)
        # head_timeからtail_timeまでtimestep分刻み、display_period分の、値がNothingなカレンダーを作る
        #subjects=Suresubject.objects.all()
        subjects=Suresubject.objects.filter(subjectclass='room')
        rowspan=1 +subjects.count()
        
        calendar = {}
        for day in days:
            shcelist={}
            for subject in subjects:
                row = {}
                for time in times:
                    row[time] = 'Nothing'
                shcelist[subject]=row
            calendar[day] = shcelist
        for subject in subjects:
            calendar=calumndays(calendar,subject,days)
        context['event'] =event
        context['calendar'] =calendar
        context['rowspan'] =rowspan
        context['times'] = times
        context['days'] = days
        context['start_day'] =start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=display_period)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = datetime.date.today()
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        kwgs["categories"] = choicetime(event)
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        schedule.event = event
        schedule.updateuser= self.request.user
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
        elif schedule.subject =='meeting_room':
            meeting_room=get_object_or_404(Suresubject,name='会議室')
            if Schedule.objects.filter(date=schedule.date,subject_name=meeting_room,cycle='nocycle')\
                .exclude(Q(starttime__gte= schedule.endtime) | Q(endtime__lte=schedule.starttime)).exists()\
                or cyclebooking(schedule,meeting_room) or newcyclecheck(schedule,meeting_room):
                messages.error(self.request, 'すでに予約がありました。')
                return redirect('MonCal:event_list', pk=event.pk)
            else:        
                subschedule=Schedule(date=schedule.date,starttime=schedule.starttime,
                                    endtime=schedule.endtime,subject_name=meeting_room,
                                    user=self.request.user,title=schedule.title,
                                    cycle=schedule.cycle,detail=schedule.detail)
                subschedule.save()
                
                schedule.subschedule=subschedule
                schedule.save() 
                return redirect('MonCal:event_list', pk=event.pk)
        else:
            schedule.save() 
            return redirect('MonCal:event_list', pk=event.pk)
def calumndays(calendar,subject,days):
    for day in days:
        for schedule in Schedule.objects.filter(subject_name=subject,cycle='nocycle',date=day):
            booking_date = day
            booking_time = schedule.starttime
            calendar[booking_date][subject][booking_time]=schedule
            int_time=datetime.datetime.combine(booking_date,booking_time)
            whileboolen=True
            while whileboolen:
                int_time=int_time + datetime.timedelta(minutes=30)
                if int_time.time() < schedule.endtime:
                    booking_time=int_time.time()
                    calendar[booking_date][subject][booking_time] = 'same'
                else:
                    whileboolen=False
    return calendar

#営業所ごとの直近の行事予定
class EventList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/Event_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        dt_nextmon=dt_today  + datetime.timedelta(days=30) 
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        schedule=EventSchedule.objects.filter(event=event,date__gte=dt_today,\
                     date__lte=dt_nextmon,cycle='nocycle').order_by('date','starttime')
        cyschedule=EventSchedule.objects.filter(event=event,date__lte=dt_nextmon)\
                    .exclude(cycle='nocycle').order_by('date','starttime')
        context['single_list'] = schedule.distinct()
        context['cycle_list'] = cyschedule.distinct()
        context['event']=event
        return context

#時刻の選択肢作成
def choicetime(subject):
    looptime=subject.head_time
    today = datetime.date.today()
    choicelist=[]     
    while looptime <= subject.tail_time:
        choicelist.append((looptime,looptime))
        loopdate=datetime.datetime.combine(today, looptime)
        loopdate=loopdate + datetime.timedelta(minutes=30)
        looptime=loopdate.time()
    category_choice = tuple(choicelist)
    return(category_choice)
#カレンダー作成
def makecalendar(subject,base_date,context):
    head_time=subject.head_time
    tail_time=subject.tail_time
    display_period=7
    timestep=30
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
    for schedule in Schedule.objects.filter(subject_name=subject)\
                        .exclude(Q(date__gt=end_day) | Q(cycle='nocycle')):
        if schedule.cycle=='week':
            day=weeklymatch(date=schedule.date,days=days)
            calendar=scheincal(calendar,schedule,day)

    # カレンダー表示する最初と最後の日時の間にある予約を取得する
    for schedule in Schedule.objects.filter(subject_name=subject,cycle='nocycle')\
                        .exclude(Q(date__gt=end_day) | Q(date__lt=start_day)):
        if schedule.starttime in calendar and schedule.date in calendar[schedule.starttime]: 
            calendar=scheincal(calendar,schedule,schedule.date)  
    context['subject'] =subject
    context['calendar'] =calendar
    context['days'] = days
    context['start_day'] =start_day
    context['end_day'] = end_day
    context['before'] = context['days'][0] - datetime.timedelta(days=display_period)
    context['next'] = context['days'][-1] + datetime.timedelta(days=1)
    context['today'] = datetime.date.today()
    return(context)
#カレンダーに予定を入力
def scheincal(calendar,schedule,date):
    booking_date = date
    booking_time = schedule.starttime
    timestep=30
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
#一致する曜日を探す
def weeklymatch(date,days):
    for day in days:
        if day.weekday() ==date.weekday():
            return(day)
#繰り返しスケジュールとの衝突確認
def cyclebooking(schedule,subject):
    cyboolean=False
    for cysche in Schedule.objects.filter(date__lte=schedule.date,subject_name=subject)\
                    .exclude(Q(starttime__gte= schedule.endtime)|Q(endtime__lte=schedule.starttime)|\
                             Q(cycle='nocycle')| Q(pk=schedule.pk)):
        if cysche.cycle == 'week' and cysche.date.weekday()==schedule.date.weekday():
            cyboolean=True
    print(cyboolean)
    return(cyboolean)
#繰り返しを追加するときの衝突確認
def newcyclecheck(schedule,subject):
    cyboolean=False
    if schedule.cycle =='nocycle':
        cyboolean=False
    else:
        for cysche in Schedule.objects.filter(date__gte=schedule.date,subject_name=subject)\
            .exclude(Q(starttime__gte= schedule.endtime)|Q(endtime__lte=schedule.starttime)| Q(pk=schedule.pk)):
            if cysche.cycle == 'week' and cysche.date.weekday()==schedule.date.weekday():
                cyboolean=True
    print(cyboolean)
    return(cyboolean)