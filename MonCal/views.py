
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.urls import reverse,reverse_lazy
from .models import Suresubject, Schedule,Event,EventSchedule,Subject_type,Booking_time,Working_day
from .forms import Scheduleform,EventScheduleform
import datetime,calendar

User = get_user_model()

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class TimeListView(SuperuserRequiredMixin,generic.ListView):
    model = Booking_time
    ordering ='pk'
    context_object_name ='times'


class TimeUpdate(SuperuserRequiredMixin,generic.UpdateView):
    model = Booking_time
    fields=('time',)
    template_name = 'MonCal/time_update.html'
    success_url=reverse_lazy('Booking_time_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookingtime']= get_object_or_404(Booking_time, pk=self.kwargs['pk'])
        return context

#ホームページ
class HomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/home_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_list={}
        for subjecttype in Subject_type.objects.all().order_by('-name'):
            subject_list[subjecttype.name]=Suresubject.objects.filter(subject_type=subjecttype).order_by('name')
        context['subject_list']= subject_list
        context['event_list']= Event.objects.all().order_by('name')
        return context

#稼働日非稼働日一覧
class Workingdaylist(LoginRequiredMixin,generic.TemplateView):
    template_name = 'MonCal/Working_day_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        notworkdays= Working_day.objects.filter(date__gte=dt_today,weekend_f=False).order_by('date')
        workdays= Working_day.objects.filter(date__gte=dt_today,weekend_f=True).order_by('date')
        context['notworkdays']=notworkdays
        context['workdays']=workdays
        return context
#稼働日非稼働日登録
class SetWorkingday(LoginRequiredMixin,generic.CreateView):
    template_name = 'MonCal/set_workingday.html'
    model = Working_day
    fields=('date',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        if not(year and month):
            dt_today =datetime.date.today()
            year=dt_today.year
            month=dt_today.month
        day_list=calendar.monthcalendar(year, month)
        firstday=datetime.date(year, month, 1)
        workdays= Working_day.objects.filter(date__gte=firstday)
        registration_list=[]
        for workday in workdays:
            if workday.date.year==year and workday.date.month==month:
                registration_list.append(workday.date.day)
        context['day_list']=day_list
        context['year']=year
        context['month']=month
        context['registration_list']=registration_list
        context['before']=firstday- datetime.timedelta(days=1)
        context['after']=firstday+ datetime.timedelta(days=31)
        return context
    def form_valid(self, form):
        day = form.save(commit=False)
        if Working_day.objects.filter(date=day.date).exists():
            messages.error(self.request, 'その日は既に登録されています')
            return redirect('MonCal:set_workingday')
        day.weekend_f=day.date.weekday() >=5
        day.save()
        return redirect('MonCal:Working_day_list')
#稼働日非稼働日削除
class WorkingdayDelete(LoginRequiredMixin, generic.DeleteView):
    model = Working_day
    success_url=reverse_lazy('MonCal:Working_day_list')
    template_name = 'MonCal/delete_working.html'

#設備の区分別予約カレンダー
class SubjectTypeCal(LoginRequiredMixin,generic.CreateView):
    template_name = 'MonCal/SubjectTypeCal.html'
    model = Schedule

#設備の直近の予定
class PropertyList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/Property_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        dt_nextmon=dt_today  + datetime.timedelta(days=30) 
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule=Schedule.objects.filter(subject_name=subject,date__gte=dt_today,\
                     date__lte=dt_nextmon,cycle_type__code='nocycle').order_by('date','starttime')
        cyschedule=Schedule.objects.filter(subject_name=subject,date__lte=dt_nextmon)\
                    .exclude(cycle_type__code='nocycle').order_by('date','starttime')
        context['single_list'] = schedule.distinct()
        context['cycle_list'] = cyschedule.distinct()
        context['subject']=subject
        return context
#予約カレンダーページ
class PropertyCalendar(LoginRequiredMixin,generic.CreateView):
    model = Schedule
    form_class=Scheduleform
    template_name = 'MonCal/calendar.html'
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
        context=makecalendar(subject,base_date,context,0)
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        #subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        categories={}
        categories
        kwgs["categories"] = choicetime()
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        date=schedule.date
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
        elif  bookingcheck(schedule,subject,0):
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
        context['event']=event
        return context
#設備予約の編集
class PropertyEdit(LoginRequiredMixin,generic.UpdateView):
    model = Schedule
    form_class=Scheduleform
    template_name = 'MonCal/Property_edit.html'
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject=get_object_or_404(Suresubject, pk=self.kwargs['subject_pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date=event.date
        context=makecalendar(subject,base_date,context,event.pk)
        context['event']=event
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)        
        kwgs["categories"] = choicetime()
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        schedule = form.save(commit=False)
        subject=schedule.subject_name 
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')  
            return redirect('MonCal:Property_edit', pk=schedule.pk)
        elif bookingcheck(schedule,subject,schedule.pk):
            messages.error(self.request, 'すでに予約がありました。')
            return redirect('MonCal:Property_edit', pk=schedule.pk)
        else:
            schedule.user= self.request.user
            schedule.save()                
            form.save_m2m() 
        return redirect('MonCal:Property_detail', pk=schedule.pk)
#設備予約の削除
class PropertyDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    def get_success_url(self):
        return reverse('MonCal:property_list', kwargs={'pk': self.kwargs['subject_pk']})

#行事予約カレンダーページ
class EventCalendar(LoginRequiredMixin,generic.CreateView):
    model = EventSchedule
    form_class=EventScheduleform
    template_name = 'MonCal/Eventcalendar.html'
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どの日を基準にカレンダーを表示するかの処理。年月日の指定がなければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date =  datetime.date.today()
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        context=makeeventcal(context,base_date)
        return context
    #選択肢の生成
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["categories"] =eventform_choice()
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        schedule=form.save(commit=False)
        rooms = form.cleaned_data.get('room')
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            return redirect('MonCal:eventcalendar')
        #設備予約をチェック
        if schedule.cycle_type.code == 'nocycle':
            samedaysche=betweenschedule(EventSchedule,schedule.date,schedule.date)
            for sche_list in samedaysche:
                sche=sche_list[2]
                if sche.starttime < schedule.endtime or sche.endtime > schedule.starttime:
                    for subject in sche.room.all():
                        if str(subject.pk ) in rooms:
                            messages.error(self.request,subject.name + 'にすでに予約がありました。')
                            return redirect('MonCal:eventcalendar')
        elif schedule.cycle_type.code == 'week':
            for subject_pk in rooms:
                subject=Suresubject.objects.get(pk=int(subject_pk))
                if EventSchedule.objects.filter(date__week_day=schedule.date.weekday(),room=subject,cycle_type__code='nocycle')\
                                .exclude(Q(starttime__gte= schedule.endtime) | Q(endtime__lte=schedule.starttime)| Q(date__lt=schedule.date)).exists():
                    messages.error(self.request,subject.name + 'にすでに予約がありました。')
                    return redirect('MonCal:eventcalendar')
        else:
            for subject_pk in rooms:
                subject=Suresubject.objects.get(pk=int(subject_pk))
                if EventSchedule.objects.filter(room__in=subject,cycle_type=schedule.cycle_type)\
                                        .exclude(Q(starttime__gte= schedule.endtime) | Q(endtime__lte=schedule.starttime)).exists():
                    messages.error(self.request,subject.name + 'にすでに予約がありました。')
                    return redirect('MonCal:eventcalendar')
        schedule.updateuser=self.request.user
        schedule.save()
        form.save_m2m()
        return redirect('MonCal:event_list')

#営業所ごとの直近の行事予定
class EventList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/Event_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        dt_nextmon=dt_today  + datetime.timedelta(days=30) 
        place_list=Event.objects.all()
        all_schedule=betweenschedule(EventSchedule,dt_today,dt_nextmon)
        schedule_list=[]
        for schedule in all_schedule:
            schedule_list.append((schedule[0],schedule[2]))
        context['all_schedule'] = schedule_list
        context['place_list'] = place_list
        return context
#行事予定の詳細ページ
class EventDetail(LoginRequiredMixin,generic.TemplateView):
    template_name = 'MonCal/Event_detail.html'
    #スケジュールの情報を表示
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = get_object_or_404(EventSchedule, pk=self.kwargs['pk'])
        context['schedule']=schedule
        return context
#行事予定の編集
class EventEdit(LoginRequiredMixin,generic.UpdateView):
    model = EventSchedule
    form_class=EventScheduleform
    template_name = 'MonCal/Event_edit.html'
    def get_initial(self):
        initial = super().get_initial()
        schedule = get_object_or_404(EventSchedule, pk=self.kwargs['pk'])
        room_list=[]
        for room in schedule.room.all():
            room_list.append(room.pk)
        place_list=[]
        for place in schedule.place.all():
            place_list.append(place.pk)
        initial["place"] =place_list
        initial["room"] = room_list
        return initial
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = get_object_or_404(EventSchedule, pk=self.kwargs['pk'])
        
        # どの日を基準にカレンダーを表示するかの処理。年月日の指定がなければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date =  datetime.date.today()
        context['schedule'] =schedule
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        context=makeeventcal(context,base_date)
        return context
    #フォームの選択肢を取得
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["categories"] = eventform_choice()
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        schedule = form.save(commit=False)
        rooms=form.cleaned_data.get('room')
        #時刻が不正の場合
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            return redirect('MonCal:Event_edit', pk=schedule.pk)
        schedule.updateuser= self.request.user
        beforesche=EventSchedule.objects.get(pk=schedule.pk)
        
        pre_schedule_list=[]
        for subject_pk in rooms:
            subject=Suresubject.objects.get(pk=subject_pk)
            
            pre_schedule=Schedule(date=schedule.date,starttime=schedule.starttime,endtime=schedule.endtime,
                                        subject_name=subject,user= self.request.user,title=schedule.title,
                                        cycle_type=schedule.cycle_type,detail=schedule.detail)
            pre_schedule_pk=0
            for before_sche_room in beforesche.subschedule.all():
                if subject.pk == before_sche_room.subject_name.pk:
                    pre_schedule_pk=before_sche_room.pk
                    pre_schedule.pk=pre_schedule_pk
            if bookingcheck(pre_schedule,subject,pre_schedule_pk):
                messages.error(self.request,subject.name + 'にすでに予約がありました。')
                return redirect('MonCal:Event_edit', pk=schedule.pk)
            pre_schedule_list.append(pre_schedule)
        for before_sche_room in beforesche.subschedule.all():
            before_sche_room.delete()
        for pre_schedule in pre_schedule_list:
            pre_schedule.save()
            schedule.subschedule.add(pre_schedule)
        schedule.save()
        form.save_m2m()
        return redirect('MonCal:Event_detail', pk=schedule.pk)
#行事予定の削除
class EventDelete(LoginRequiredMixin, generic.DeleteView):
    model = EventSchedule
    success_url=reverse_lazy('MonCal:event_list')

#時刻の選択肢作成
def choicetime():
    looptime=get_object_or_404(Booking_time, pk=1).time
    end_time=get_object_or_404(Booking_time,pk=2).time
    today = datetime.date.today()
    choicelist=[]     
    while looptime <= end_time:
        choicelist.append((looptime,looptime))
        loopdate=datetime.datetime.combine(today, looptime)
        loopdate=loopdate + datetime.timedelta(minutes=30)
        looptime=loopdate.time()
    category_choice = tuple(choicelist)
    return(category_choice)

#行事予定フォーム選択肢作成
def eventform_choice():
    subjectlist=[]
    for subject in Suresubject.objects.all().exclude(subject_type=3):
        subjectlist.append((str(subject.pk),subject.name))
    placelist=[]
    for place in Event.objects.all():
        placelist.append((str(place.pk),place.name))
    categories={}
    categories['time']=choicetime()
    #categories['cycle_type']=[('nocycle','繰り返さない'),('week','毎週')]
    categories['room']=subjectlist
    categories['place']=placelist
    return(categories)

#カレンダー作成
def makecalendar(subject,base_date,context,pk):
    head_time=get_object_or_404(Booking_time, pk=1).time
    tail_time=get_object_or_404(Booking_time,pk=2).time
    display_period=7
    timestep=30
    days = [base_date + datetime.timedelta(days=day) for day in range(display_period)]
    start_day = days[0]
    end_day = days[-1]
    # head_timeからtail_timeまでtimestep分刻み、display_period分の、値がNothingなカレンダーを作る
    calendar = {}
    loop_time= datetime.datetime.combine(start_day, head_time)
    loop_tail= datetime.datetime.combine(start_day,tail_time)
    workingdays=[]
    for workingday in Working_day.objects.filter(Q(date__gte=start_day) | Q(date__lte=end_day)):
        workingdays.append(workingday.date)
    while loop_time < loop_tail:
        row = {}
        for day in days:
            if (day.weekday() < 5 and not day in workingdays)\
                or (day.weekday() >= 5 and day in workingdays):
                row[day] = 'Nothing'
            else:
                row[day] = 'notworkday'
        calendar[loop_time.time()] = row
        loop_time = loop_time + datetime.timedelta(minutes=timestep) 
    #繰り返しスケジュールを取得する
    for schedule in Schedule.objects.filter(subject_name=subject)\
                        .exclude(Q(date__gt=end_day) | Q(cycle_type__code='nocycle')|Q(pk=pk)):
        if schedule.cycle_type.code=='week':
            day=weeklymatch(date=schedule.date,days=days)
            calendar=scheincal(calendar,schedule,day)

    # カレンダー表示する最初と最後の日時の間にある予約を取得する
    for schedule in Schedule.objects.filter(subject_name=subject,cycle_type__code='nocycle')\
                        .exclude(Q(date__gt=end_day) | Q(date__lt=start_day)|Q(pk=pk)):
        if schedule.starttime in calendar and schedule.date in calendar[schedule.starttime]: 
            calendar=scheincal(calendar,schedule,schedule.date)  
    context['workingdays'] = workingdays
    context['subject'] =subject
    context['calendar'] =calendar
    context['tailtime'] = tail_time
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
    frame=1
    while whileboolen:
        int_time=int_time + datetime.timedelta(minutes=timestep)
        if int_time.time() < schedule.endtime:
            booking_time=int_time.time()
            calendar[booking_time][booking_date] = 'same'
            frame=frame+1
        else:
            whileboolen=False
    calendar[schedule.starttime][date]={schedule:frame}
    return(calendar)

#行事カレンダーcontext作成
def makeeventcal(context,base_date):
    head_time=get_object_or_404(Booking_time, pk=1).time
    tail_time=get_object_or_404(Booking_time,pk=2).time
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
    schedule_list= betweenschedule(EventSchedule,start_day,end_day)
    calendar=calumndays(days,times,schedule_list)
    workingdays=Working_day.objects.filter(date__gte=start_day,date__lte=end_day)
    workingday_list=[]
    for workingday in workingdays:
        workingday_list.append(workingday.date)
    context['workingday_list'] =workingday_list
    context['calendar'] =calendar
    context['times'] = times
    context['tailtime'] = tail_time
    context['days'] = days
    context['start_day'] =start_day
    context['end_day'] = end_day
    context['before'] = days[0] - datetime.timedelta(days=display_period)
    context['next'] = days[-1] + datetime.timedelta(days=1)
    context['today'] = datetime.date.today()
    return(context)
#行事カレンダーを作成
def calumndays(days,times,schedule_list):
    calendar = {}
    for day in days:
        shce_list=[]
        row = {}
        for time in times:
            row[time] = 'Nothing'
        day_schedule=[]
        for schedule in schedule_list:
            if day == schedule[0].date():
                day_schedule.append(schedule[2])
        shce_list.append(row)
        max_row=0
        
        for schedule in day_schedule:
            now_row=0
            while not confirmation_sche(shce_list[now_row],times,schedule):
                if now_row == max_row:
                    row = {}
                    for time in times:
                        row[time] = 'Nothing'
                    shce_list.append(row)
                    now_row=now_row+1
                    max_row=now_row
                else:
                    now_row=now_row+1
            shce_list[now_row]=input_row(shce_list[now_row],times,schedule)      
        day_dic={'date_span':max_row+2,'shce_span':max_row+1,'shce_list':shce_list}
        calendar[day] =day_dic
    return calendar
#行事の時間衝突確認
def confirmation_sche(row,times,schedule):
    inputF=True
    for time in times:
        if time >=schedule.starttime \
        and time <= schedule.endtime \
        and row[time] !='Nothing':
            inputF=False
    return inputF
#行事を入力
def input_row(row,times,schedule):
    inputF=True
    col=1
    for time in times:
        if time >=schedule.starttime and time <= schedule.endtime:
            if inputF:
                inputF=False
                row[time] =schedule
                starttime=time
            else:
                row[time]='same'
                col=1+col
    book={'col_span':col-1,'schedule':schedule}
    row[starttime] =book
    return row

#スケジュールを行事カレンダーに入力
def bookingcalmun(calendar,booking_date,subject,booking_time,schedule):
    calendar[booking_date][subject][booking_time]=schedule
    int_time=datetime.datetime.combine(booking_date,booking_time)
    whileboolen=True
    flame=1
    while whileboolen:
        int_time=int_time + datetime.timedelta(minutes=30)
        if int_time.time() < schedule.endtime:
            sametime=int_time.time()
            calendar[booking_date][subject][sametime] = 'same'
            flame=flame+1
        else:
            whileboolen=False
    calendar[booking_date][subject][booking_time]={schedule:flame}
    return calendar

#ある期間の中にあるスケジュールを抽出
def betweenschedule(Schedule,dt_today,dt_nextmon):
    schedule=Schedule.objects.filter(date__gte=dt_today,date__lte=dt_nextmon,
                                     cycle_type__code='nocycle').order_by('date','starttime')
    weekschedule=Schedule.objects.filter(date__lte=dt_nextmon,\
                                       cycle_type__code='week').order_by('date','starttime')
    dt=dt_today
    sche_list=[]
    num=0
    for sche in schedule:
        sche_datetime=datetime.datetime.combine(sche.date, sche.starttime)
        sche_list.append([sche_datetime,num,sche])
        num=num+1
    while dt <= dt_nextmon:
        for sche in weekschedule:
           if dt.weekday()  == sche.date.weekday():
                sche_datetime=datetime.datetime.combine(dt, sche.starttime)
                sche_list.append([sche_datetime,num,sche])
                num=num+1
        dt=dt+ datetime.timedelta(days=1)
    return sorted(sche_list)

#一致する曜日を探す
def weeklymatch(date,days):
    for day in days:
        if day.weekday() ==date.weekday():
            return(day)
#スケジュールとの衝突確認
def bookingcheck(schedule,subject,schedule_pk):
    return(singlebooking(schedule,subject,schedule_pk) or cyclebooking(schedule,subject,schedule_pk) or newcyclecheck(schedule,subject,schedule_pk))
#単発スケジュールとの衝突確認
def singlebooking(schedule,subject,schedule_pk):
    singleboolean=Schedule.objects.filter(date=schedule.date,subject_name=subject,cycle_type__code='nocycle')\
                    .exclude(Q(starttime__gte= schedule.endtime) | Q(endtime__lte=schedule.starttime)|Q(pk=schedule_pk)).exists()
    return(singleboolean)
#繰り返しスケジュールとの衝突確認
def cyclebooking(schedule,subject,schedule_pk):
    cyboolean=False
    for cysche in Schedule.objects.filter(date__lte=schedule.date,subject_name=subject)\
            .exclude(Q(starttime__gte= schedule.endtime)|Q(endtime__lte=schedule.starttime)|\
                     Q(cycle_type__code='nocycle')| Q(pk=schedule_pk)):
        if cysche.cycle_type.code == 'week' and cysche.date.weekday()==schedule.date.weekday():
                cyboolean=True
    return(cyboolean)
#繰り返しを追加するときの衝突確認
def newcyclecheck(schedule,subject,schedule_pk):
    cyboolean=False
    if schedule.cycle_type.code =='nocycle':
        cyboolean=False
    elif schedule.cycle_type.code =='week':
        for cysche in Schedule.objects.filter(date__gte=schedule.date,subject_name=subject)\
            .exclude(Q(starttime__gte= schedule.endtime)|Q(endtime__lte=schedule.starttime)| Q(pk=schedule_pk)):
            if cysche.date.weekday()==schedule.date.weekday():
                cyboolean=True
    return(cyboolean)

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