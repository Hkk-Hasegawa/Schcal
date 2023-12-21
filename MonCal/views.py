

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.urls import reverse,reverse_lazy
from .models import Suresubject, Schedule,Event,EventSchedule,Subject_type,Booking_time,Working_day,Cycle_pause,Room
from .forms import Scheduleform,EventScheduleform,AllScheduleform
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
    success_url=reverse_lazy('MonCal:Booking_time_list')
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
        subjecttype = Subject_type.objects.get(name='社用車')
        subject_list[subjecttype]=Suresubject.objects.filter(subject_type=subjecttype).order_by('name')
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


class AllPropertyList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/All_Property_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        dt_nextmon=dt_today  + datetime.timedelta(days=30) 
        subject_type = get_object_or_404(Subject_type, pk=self.kwargs['pk'])
        
        all_schedule=betweenschedule(Schedule,dt_today,dt_nextmon)
        schedule_list=[]
        for schedule in all_schedule:
            if schedule[2].subject_name.subject_type == subject_type:
                schedule_list.append((schedule[0],schedule[2]))
        context['all_schedule'] = schedule_list
        context['subject_type']=subject_type
        return context

class AllPropertyCalendar(LoginRequiredMixin, generic.CreateView):
    model = Schedule
    form_class=AllScheduleform
    template_name = 'MonCal/allprcalendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_type = get_object_or_404(Subject_type, pk=self.kwargs['pk'])
        subjects=Suresubject.objects.filter(subject_type=subject_type)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date =  datetime.date.today()
        context=makecal(context,base_date,3)
        calender_dic={}
        for subject in subjects:
            calender_dic[subject]=subject_calender(context,subject,0)
        moncal_base=display_period_days(base_date,1)[0]
        context=make_monthly_calendar(context,base_date)
        context['base_date']=moncal_base
        context['calender_dic']=calender_dic
        context['subject_type']=subject_type
        context['datespan']=subjects.count()
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        categories={}
        
        subject_type = get_object_or_404(Subject_type, pk=self.kwargs['pk'])
        subjects=Suresubject.objects.filter(subject_type=subject_type)
        subject_list=[]
        for subject in subjects:
            subject_list.append((subject.pk,subject.name))
        categories['subject']=subject_list
        categories['time']=choicetime()
        kwgs["categories"] = categories
        return kwgs
    def form_valid(self, form):
        subject_type = get_object_or_404(Subject_type, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        subject_pk = form.cleaned_data.get('subject')
        schedule.subject_name=Suresubject.objects.get(pk=subject_pk)
        schedule_list=Schedule.objects.filter(date=schedule.date,subject_name=schedule.subject_name)\
                                      .exclude(Q(starttime__gte=schedule.endtime)|
                                               Q(endtime__lte=schedule.starttime))
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        redirect_check=True
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            redirect_check=False
        elif  schedule_list.exists():
            messages.error(self.request, 'すでに予約がありました。')
            redirect_check=False
        else:
            schedule.user= self.request.user
            schedule.save() 
        if redirect_check:
            return redirect('MonCal:all_property_list', pk=subject_type.pk)
        elif year and month and day:
            return redirect('MonCal:all_pr_calendar', pk=subject_type.pk,year=year,month=month,day=day)
        else:
            return redirect('MonCal:all_pr_calendar', pk=subject_type.pk)

class AllPropertyEdit(LoginRequiredMixin,generic.UpdateView):
    model = Schedule
    form_class=AllScheduleform
    template_name = 'MonCal/allprcalendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject_type = schedule.subject_name.subject_type
        subjects=Suresubject.objects.filter(subject_type=subject_type)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date =  datetime.date.today()
        context=makecal(context,base_date,3)
        calender_dic={}
        for subject in subjects:
            calender_dic[subject]=subject_calender(context,subject,schedule.pk)
        moncal_base=display_period_days(base_date,1)[0]
        context=make_monthly_calendar(context,base_date)
        context['base_date']=moncal_base
        context['calender_dic']=calender_dic
        context['subject_type']=subject_type
        context['datespan']=subjects.count()
        context['schedule']=schedule
        return context
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        categories={}
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject_type = schedule.subject_name.subject_type
        subjects=Suresubject.objects.filter(subject_type=subject_type)
        subject_list=[]
        for subject in subjects:
            subject_list.append((subject.pk,subject.name))
        categories['subject']=subject_list
        categories['time']=choicetime()
        kwgs["categories"] = categories
        return kwgs
    def form_valid(self, form):
        sche = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject_type = sche.subject_name.subject_type
        schedule = form.save(commit=False)
        subject_pk = form.cleaned_data.get('subject')
        schedule.subject_name=Suresubject.objects.get(pk=subject_pk)
        schedule_list=Schedule.objects.filter(date=schedule.date,subject_name=schedule.subject_name)\
                                      .exclude(Q(starttime__gte=schedule.endtime)|
                                               Q(endtime__lte=schedule.starttime)|
                                               Q(pk=schedule.pk))
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        redirect_check=True
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            redirect_check=False
        elif  schedule_list.exists():
            messages.error(self.request, 'すでに予約がありました。')
            redirect_check=False
        else:
            schedule.user= self.request.user
            schedule.save() 
        if redirect_check:
            return redirect('MonCal:all_property_list', pk=subject_type.pk)
        elif year and month and day:
            return redirect('MonCal:all_pr_calendar', pk=subject_type.pk,year=year,month=month,day=day)
        else:
            return redirect('MonCal:all_pr_calendar', pk=subject_type.pk)
#設備の直近の予定
class PropertyList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/Property_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt_today =datetime.date.today()
        dt_nextmon=dt_today  + datetime.timedelta(days=30) 
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        all_schedule=betweenschedule(Schedule,dt_today,dt_nextmon)
        schedule_list=[]
        for schedule in all_schedule:
            if schedule[2].subject_name == subject:
                schedule_list.append((schedule[0],schedule[2]))
        context['all_schedule'] = schedule_list
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
        context=makecal(context,base_date,7)
        context['calender']=subject_calender(context,subject,0)
        context['subject'] =subject
        context=make_monthly_calendar(context,base_date)
        return context
    #時刻の選択肢
    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        categories={}
        categories
        kwgs["categories"] = choicetime()
        return kwgs
    #フォームの保存
    def form_valid(self, form):
        subject = get_object_or_404(Suresubject, pk=self.kwargs['pk'])
        schedule = form.save(commit=False)
        schedule_list=Schedule.objects.filter(date=schedule.date,subject_name=subject)\
                                      .exclude(Q(starttime__gte=schedule.endtime)|
                                               Q(endtime__lte=schedule.starttime))
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        redirect_check=True
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            redirect_check=False
        elif  schedule_list.exists():
            messages.error(self.request, 'すでに予約がありました。')
            redirect_check=False
        else:
            schedule.subject_name = subject
            schedule.user= self.request.user
            schedule.save() 
        if redirect_check:
            return redirect('MonCal:property_list', pk=subject.pk)
        elif year and month and day:
            return redirect('MonCal:calendar', pk=subject.pk,year=year,month=month,day=day)
        else:
            return redirect('MonCal:calendar', pk=subject.pk)
            
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
    template_name = 'MonCal/calendar.html'
    #カレンダーの作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject=schedule.subject_name
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date=schedule.date
        context=makecal(context,base_date,7)
        context['calender']=subject_calender(context,subject,schedule.pk)
        context['subject'] =subject
        context['schedule']=schedule
        context=make_monthly_calendar(context,base_date)
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
        schedule_list=Schedule.objects.filter(date=schedule.date,subject_name=subject)\
                                      .exclude(Q(starttime__gte=schedule.endtime)|
                                               Q(endtime__lte=schedule.starttime)|
                                               Q(pk=schedule.pk)).exists()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        redirect_check=True
        if schedule.starttime >= schedule.endtime:
            messages.error(self.request, '時刻が不正です。')
            redirect_check=False
        elif schedule_list:
            messages.error(self.request, 'すでに予約がありました。')
            redirect_check=False
        else:
            schedule.subject_name = subject
            schedule.user= self.request.user
            schedule.save()                
        if redirect_check:
            return redirect('MonCal:Property_detail', pk=schedule.pk)
        elif year and month and day:
            return redirect('MonCal:Property_edit', pk=schedule.pk,year=year,month=month,day=day)
        else:
            return redirect('MonCal:Property_edit', pk=schedule.pk)
#設備予約の削除
class PropertyDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    def get_success_url(self):
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        subject_pk=schedule.subject_name.pk
        return reverse('MonCal:property_list', kwargs={'pk': subject_pk})

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
        placelist={}
        num=-1
        for place in Event.objects.all():
            roomlist=[]
            for room in Room.objects.filter(place=place).order_by('place'):
                num=1+num
                roomlist.append({'room':room,'pk':str(room.pk),"id":'id_room_'+str(num)})
            placelist[place.name]=(roomlist,place.pk)
        context['room_dic']=placelist
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        context=makecal(context,base_date,7)
        schedule_list= betweenschedule(EventSchedule,context['start_day'],context['end_day'])
        context['calendar']=calumndays(context['days'],context['input_times'],schedule_list)
        context=make_monthly_calendar(context,base_date)
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
        if eventform_savecheck(self,schedule,rooms,0):
            schedule.updateuser=self.request.user
            schedule.save()
            for room_pk in rooms:
                room = Room.objects.get(pk=room_pk)
                schedule.room.add(room)
            schedule.save()
            form.save_m2m()
            return redirect('MonCal:event_list')
        else:
            year = self.kwargs.get('year')
            month = self.kwargs.get('month')
            day = self.kwargs.get('day')
            if year and month and day:
                return redirect('MonCal:eventcalendar', year=year,month=month,day=day)
            else:
                return redirect('MonCal:eventcalendar')


class EventyearList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'MonCal/Event_year_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        if not year:
            year=datetime.date.today().year
        fst_day=datetime.date(year=year,month=1,day=1)
        lst_day=datetime.date(year=fst_day.year+1,month=1,day=1) - datetime.timedelta(days=1) 
        place_list=Event.objects.all()
        all_schedule=betweenschedule(EventSchedule,fst_day,lst_day)
        year_schedule={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
        for schedule in all_schedule:
            year_schedule[schedule[0].month].append((schedule[0],schedule[2]))
        context['year_schedule'] = year_schedule
        context['place_list'] = place_list 
        context['year'] = year 
        context['next'] = year +1
        context['before'] = year -1
        return context
        
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
        year = self.kwargs.get('year')
        if not year:
            year=datetime.date.today().year
        fst_day=datetime.date(year=year,month=1,day=1)
        lst_day=datetime.date(year=fst_day.year+1,month=1,day=1) - datetime.timedelta(days=1) 
        ayear_schedule=betweenschedule(EventSchedule,fst_day,lst_day)
        year_schedule={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
        for schedule in ayear_schedule:
            year_schedule[schedule[0].month].append((schedule[0],schedule[2]))
        context['all_schedule'] = schedule_list
        context['place_list'] = place_list 
        context['year_schedule'] = year_schedule
        context['year'] = year 
        context['next'] = year +1
        context['before'] = year -1
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
    template_name = 'MonCal/Eventcalendar.html'
    def get_initial(self):
        initial = super().get_initial()
        schedule = get_object_or_404(EventSchedule, pk=self.kwargs['pk'])
        place_list=[]
        for place in schedule.place.all():
            place_list.append(place.pk)
        initial["place"] =place_list
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
            base_date = datetime.date(year=schedule.date.year, month=schedule.date.month, day=schedule.date.day)
        context['schedule'] =schedule
        placelist={}
        num=-1
        for place in Event.objects.all():
            roomlist=[]
            for room in Room.objects.filter(place=place).order_by('place'):
                num=1+num
                roomlist.append({'room':room,'pk':str(room.pk),"id":'id_room_'+str(num)})
            placelist[place.name]=(roomlist,place.pk)
        context['room_dic']=placelist
        # カレンダーは、基準日から表示期間分の日付を作成しておく
        context=makecal(context,base_date,7)
        schedule_list= betweenschedule(EventSchedule,context['start_day'],context['end_day'])
        new_schedule_list=[]
        for sche_box in schedule_list:
            if sche_box[2].pk!=schedule.pk:
                new_schedule_list.append(sche_box)
        context['calendar']=calumndays(context['days'],context['input_times'],new_schedule_list)
        context=make_monthly_calendar(context,base_date)
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
        if eventform_savecheck(self,schedule,rooms,schedule.pk):
            schedule.updateuser=self.request.user
            for room_pk in rooms:
                room = Room.objects.get(pk=room_pk)
                schedule.room.add(room)
            schedule.save()
            form.save_m2m()
            return redirect('MonCal:Event_detail', pk=schedule.pk)
        else:
            year = self.kwargs.get('year')
            month = self.kwargs.get('month')
            day = self.kwargs.get('day')
            if year and month and day:
                return redirect('MonCal:Event_edit', pk=schedule.pk,year=year,month=month,day=day)
            else:
                return redirect('MonCal:Event_edit', pk=schedule.pk)
#行事予定の削除
class EventDelete(LoginRequiredMixin, generic.DeleteView):
    model = EventSchedule
    success_url=reverse_lazy('MonCal:event_list')
#繰り返し休止日設定
class EventCycleEdit(LoginRequiredMixin,generic.CreateView):
    model=Cycle_pause
    template_name = 'MonCal/Event_cycle_edit.html'
    fields=('pause_type',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        schedule = get_object_or_404(EventSchedule, pk=self.kwargs['pk'])
        base_date = datetime.date(year=year, month=month, day=day)
        today = datetime.date.today()
        after_pause=Cycle_pause.objects.filter(date__gte=today,schedule=schedule)
        context['schedule'] =schedule
        context['date'] =base_date
        context['after_pause'] =after_pause
        return context
    def form_valid(self, form):
        pause = form.save(commit=False)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        schedule = get_object_or_404(EventSchedule, pk=self.kwargs['pk'])
        base_date = datetime.date(year=year, month=month, day=day)
        if pause.pause_type.code == 'Single':
            pause.date= base_date
            pause.schedule=schedule
            pause.updateuser=self.request.user
            pause.save()
        if pause.pause_type.code == 'After':
            if Cycle_pause.objects.filter(schedule=schedule,pause_type__code='After').exists():
                pause=Cycle_pause.objects.get(schedule=schedule,pause_type__code='After')
            pause.updateuser=self.request.user
            pause.date= base_date
            pause.save()
        return redirect('MonCal:event_list')
#繰り返し休止日削除
class EventCycleDelete(LoginRequiredMixin, generic.DeleteView):
    model = Cycle_pause
    success_url=reverse_lazy('MonCal:event_list')
    template_name = 'MonCal/delete_event_cycle.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pause = get_object_or_404(Cycle_pause, pk=self.kwargs['pk'])
        schedule=pause.schedule
        rooms=[]
        for room in schedule.room.all():
            rooms.append(room.pk)
        context['savecheck']=eventform_savecheck(self,schedule,rooms,schedule.pk)

        return context
#時刻の選択肢作成
def choicetime():
    looptime=get_object_or_404(Booking_time, pk=1).time
    end_time=get_object_or_404(Booking_time,pk=2).time
    today = datetime.date.today()
    choicelist=[]     
    while looptime <= end_time:
        choicelist.append((looptime,looptime))
        loopdate=datetime.datetime.combine(today, looptime)
        loopdate=loopdate + datetime.timedelta(minutes=5)
        looptime=loopdate.time()
    category_choice = tuple(choicelist)
    return(category_choice)

#行事予定フォーム選択肢作成
def eventform_choice():
    roomlist=[]
    for room in Room.objects.all().order_by('place'):
        roomlist.append((str(room.pk),room))
    placelist=[]
    for place in Event.objects.all():
        placelist.append((str(place.pk),place.name))
    categories={}
    categories['time']=choicetime()
    categories['room']=roomlist
    categories['place']=placelist
    return(categories)
def display_period_days(base_date,display_period):
    days=[]
    date=base_date
    
    while len(days)<display_period :
        if date.weekday() <5 and not Working_day.objects.filter(date=date).exists()   or (  Working_day.objects.filter(date=date).exists() and date.weekday() >=5):
            days.append(date)
        date=date+ datetime.timedelta(days=1)
    return days
def before_display_period(base_date,display_period):
    days=[]
    date=base_date- datetime.timedelta(days=1)
    while len(days)<display_period :
        if date.weekday() <5 and not Working_day.objects.filter(date=date).exists()   or (  Working_day.objects.filter(date=date).exists() and date.weekday() >=5):
            days.append(date)
        date=date- datetime.timedelta(days=1)
    return days[display_period-1]
#カレンダーページに必要な
def makecal(context,base_date,display_period):
    head_time=get_object_or_404(Booking_time, pk=1).time
    tail_time=get_object_or_404(Booking_time,pk=2).time
    
    timestep=30
    input_timestep=5
    days =display_period_days(base_date,display_period)
    #days = [base_date + datetime.timedelta(days=day) for day in range(display_period)]
    start_day = days[0]
    end_day = days[-1]
    loop_tail= datetime.datetime.combine(start_day,tail_time)
    loop_time= datetime.datetime.combine(start_day, head_time)
    times=[]
    while loop_time < loop_tail:
        times.append(loop_time.time())
        loop_time = loop_time + datetime.timedelta(minutes=timestep)
    loop_tail= datetime.datetime.combine(start_day,tail_time)
    loop_time= datetime.datetime.combine(start_day, head_time)
    hours=[]
    while loop_time < loop_tail:
        hours.append(loop_time.time())
        loop_time = loop_time + datetime.timedelta(hours=1)
    hour_list={}
    if times[0].minute == 0:
        minute=60
    else:
        minute=times[0].minute
    hour_list[datetime.time(hour=times[0].hour)]=minute //input_timestep 
    time_span=1    
    input_times=[]
    loop_tail= datetime.datetime.combine(start_day,tail_time)
    loop_time= datetime.datetime.combine(start_day, head_time)
    while loop_time < loop_tail:
        input_times.append(loop_time.time())
        loop_time = loop_time + datetime.timedelta(minutes=input_timestep)
        if loop_time.time() in hours :
            hour_list[datetime.time(hour=loop_time.time().hour)]=time_span
            time_span=1
        else:
            time_span=1+time_span
    if tail_time.minute == 0:
        minute=60
    else:
        minute=tail_time.minute
    if tail_time.minute !=0:
        hour_list[datetime.time(hour=tail_time.hour)]=minute //input_timestep
    workingdays=Working_day.objects.filter(date__gte=start_day,date__lte=end_day)
    workingday_list=[]
    for workingday in workingdays:
        workingday_list.append(workingday.date)
    context['workingday_list'] =workingday_list
    context['times'] = times
    context['input_times'] =input_times
    context['headtime'] = times[0]
    context['tailtime'] = tail_time
    context['hour_list'] = hour_list
    context['days'] = days
    context['start_day'] =start_day
    context['end_day'] = end_day
    context['before'] = before_display_period(base_date,display_period)
    context['next'] = days[-1] + datetime.timedelta(days=1)
    context['today'] = datetime.date.today()
    return context

#行事カレンダー作成
def makecalendar(context,base_date,EventSchedule):
    context=makecal(context,base_date,7)
    schedule_list= betweenschedule(EventSchedule,context['start_day'],context['end_day'])
    context['calendar']=calumndays(context['days'],context['input_times'],schedule_list)
    return(context)

def subject_calender(context,subject,pk):
    schedule_list= betweenschedule(Schedule,context['start_day'],context['end_day'])
    if pk !=0:
        newschedule_list=[]
        for scheset in schedule_list:
            if scheset[2].pk != pk:
                newschedule_list.append(scheset)
        schedule_list=newschedule_list
    calendar=pre_calumndays(context['days'],context['input_times'],schedule_list,subject)
    
    return(calendar)

def pre_calumndays(days,input_times,schedule_list,subject):
    calendar = {}
    for day in days:
        row = {}
        for time in input_times:
            row[time] = 'Nothing'
        day_schedule=[]
        for schedule in schedule_list:
            if day == schedule[0].date() and schedule[2].subject_name ==subject:
                day_schedule.append(schedule[2])
        for schedule in day_schedule:
            row=input_row(row,input_times,schedule)
        calendar[day]=row
    return calendar

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
        day_dic={'date_span':max_row+2,'shce_list':shce_list}
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
#予定をカレンダーに入力
def input_row(row,times,schedule):
    inputF=True
    col=1
    for time in times:
        if time >=schedule.starttime and time < schedule.endtime:
            if inputF:
                inputF=False
                row[time] =schedule
                starttime=time
            else:
                row[time]='same'
                col=1+col
    book={'col_span':col,'schedule':schedule}
    row[starttime] =book
    return row

#行事フォーム保存
def eventform_savecheck(self,schedule,rooms,sche_pk):
    if schedule.starttime >= schedule.endtime:
        messages.error(self.request, '時刻が不正です。')
        return False
    #設備予約をチェック
    if schedule.cycle_type.code == 'nocycle':
        samedaysche=betweenschedule(EventSchedule,schedule.date,schedule.date)
        for sche_list in samedaysche:
            sche=sche_list[2]
            if (sche.starttime < schedule.endtime or sche.endtime > schedule.starttime) and sche.pk !=sche_pk:
                for room in sche.room.all():
                    if str(room.pk ) in rooms:
                        messages.error(self.request,room.name + 'にすでに予約がありました。')
                        return False
    #繰り返しありの場合
    elif schedule.cycle_type.code == 'week':
        for room_pk in rooms:
            if EventSchedule.objects.filter(date__week_day=weekdaychinge(schedule.date.weekday()),
                                        room=room_pk,cycle_type__code='nocycle')\
                                .exclude(Q(starttime__gte= schedule.endtime) |
                                         Q(endtime__lte=schedule.starttime) | 
                                         Q(date__lt=schedule.date)| 
                                         Q(pk=sche_pk)).exists() \
            or EventSchedule.objects.filter(date__week_day=weekdaychinge(schedule.date.weekday()),
                                        room=room_pk,cycle_type__code='week')\
                                .exclude(Q(starttime__gte= schedule.endtime) | 
                                         Q(endtime__lte=schedule.starttime)| 
                                         Q(pk=sche_pk)).exists():
                subject = get_object_or_404(Room, pk=room_pk)
                messages.error(self.request,subject.name + 'にすでに予約がありました。')
                return False
    else:
        for room_pk in rooms:
            if EventSchedule.objects.filter(room=room_pk,cycle_type=schedule.cycle_type)\
                                .exclude(Q(starttime__gte= schedule.endtime) | Q(endtime__lte=schedule.starttime)| Q(pk=sche_pk)).exists():
                subject = get_object_or_404(Room, pk=room_pk)
                messages.error(self.request,subject.name + 'にすでに予約がありました。')
                return False
    return True

#ある期間の中にあるスケジュールを抽出
def betweenschedule(Schedule,dt_today,dt_nextmon):
    schedule=Schedule.objects.filter(date__gte=dt_today,date__lte=dt_nextmon,
                                     cycle_type__code='nocycle').order_by('date','starttime')

    weekschedule=Schedule.objects.filter(date__lte=dt_nextmon,
                                         cycle_type__code='week').order_by('date','starttime')
    firstday_sche=Schedule.objects.filter(date__lte=dt_nextmon,
                                         cycle_type__code='first_working').order_by('date','starttime')
    f_Monday_sche=Schedule.objects.filter(date__lte=dt_nextmon,
                                         cycle_type__code='first_monday').order_by('date','starttime')
    loop_dt=dt_today
    firstday_list=[]
    firstMonday_list=[]
    while loop_dt<=dt_nextmon:
        firstday_list.append(find_firstday(loop_dt.year,loop_dt.month))
        firstMonday_list.append(find_firstMonday(loop_dt.year,loop_dt.month))
        loop_dt=datetime.date(year=loop_dt.year+ (loop_dt.month // 12),month=(loop_dt.month % 12) +1,day=1)


    dt=dt_today
    sche_list=[]
    num=0
    for sche in schedule:
        sche_datetime=datetime.datetime.combine(sche.date, sche.starttime)
        sche_list.append([sche_datetime,num,sche])
        sche_datetime.month
        num=num+1
    while dt <= dt_nextmon:
        if not  Working_day.objects.filter(date=dt,weekend_f=False).exists() \
            or Working_day.objects.filter(date=dt,weekend_f=True).exists():
            for sche in weekschedule:
                if dt.weekday()  == sche.date.weekday() and dt >= sche.date \
                    and stopdaycheck(sche,dt):
                        sche_datetime=datetime.datetime.combine(dt, sche.starttime)
                        sche_list.append([sche_datetime,num,sche])
                        num=num+1
        if dt in firstday_list:
            for sche in firstday_sche:
                if dt >= sche.date and stopdaycheck(sche,dt):
                    sche_datetime=datetime.datetime.combine(dt, sche.starttime)
                    sche_list.append([sche_datetime,num,sche])
                    num=num+1
        if dt in firstMonday_list:
            for sche in f_Monday_sche:
                if dt >= sche.date and stopdaycheck(sche,dt):
                    sche_datetime=datetime.datetime.combine(dt, sche.starttime)
                    sche_list.append([sche_datetime,num,sche])
                    num=num+1
        dt=dt+ datetime.timedelta(days=1)



    return sorted(sche_list)

def find_firstday(year,month):
    start_day=datetime.date(year=year,month=month,day=1)
    loopF=True
    while loopF:
        if start_day.weekday() <5 and not Working_day.objects.filter(date=start_day).exists() \
            or start_day.weekday() >=5 and Working_day.objects.filter(date=start_day).exists() :
            loopF=False
        else:
            start_day=datetime.date(year=year,month=month,day=start_day.day+1)
    return start_day

def find_firstMonday(year,month):
    start_day=datetime.date(year=year,month=month,day=1)
    loopF=True
    while loopF:
        if start_day.weekday() ==0 and not Working_day.objects.filter(date=start_day).exists():
            loopF=False
        else:
            start_day=datetime.date(year=year,month=month,day=start_day.day+1)
    return start_day

def stopdaycheck(schedule,date):
    if Cycle_pause.objects.filter(date=date,schedule=schedule).exists()\
    or Cycle_pause.objects.filter(date__lte=date,schedule=schedule,pause_type__code='After').exists():
        return False
    return True

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
    singleboolean=Schedule.objects.filter(date=schedule.date,
                                          subject_name=subject,cycle_type__code='nocycle')\
                                  .exclude(Q(starttime__gte= schedule.endtime) | 
                                           Q(endtime__lte=schedule.starttime)|
                                           Q(pk=schedule_pk)).exists()
    return(singleboolean)
#繰り返しスケジュールとの衝突確認
def cyclebooking(schedule,subject,schedule_pk):
    cyboolean=False
    for cysche in Schedule.objects.filter(date__lte=schedule.date,subject_name=subject)\
                                  .exclude(Q(starttime__gte= schedule.endtime)|
                                           Q(endtime__lte=schedule.starttime)|
                                           Q(cycle_type__code='nocycle')| 
                                           Q(pk=schedule_pk)):
        if cysche.cycle_type.code == 'week' \
        and cysche.date.weekday()==schedule.date.weekday():
                cyboolean=True
    return(cyboolean)
#繰り返しを追加するときの衝突確認
def newcyclecheck(schedule,subject,schedule_pk):
    cyboolean=False
    if schedule.cycle_type.code =='nocycle':
        cyboolean=False
    elif schedule.cycle_type.code =='week':
        for cysche in Schedule.objects.filter(date__gte=schedule.date,
                                              subject_name=subject)\
                                      .exclude(Q(starttime__gte= schedule.endtime)|
                                               Q(endtime__lte=schedule.starttime)| 
                                               Q(pk=schedule_pk)):
            if cysche.date.weekday()==schedule.date.weekday():
                cyboolean=True
    return(cyboolean)

def weekdaychinge(weekday):
    newweekday= (weekday+1) % 7 +1
    return(newweekday)
    
def make_monthly_calendar(context,base_date):
    moncal_base=display_period_days(base_date,1)[0]
    day_list=calendar.monthcalendar(moncal_base.year, moncal_base.month)
    if len(day_list)<6:
        day_list.append([0,0,0,0,0,0,0])
    firstday=datetime.date(moncal_base.year, moncal_base.month, 1)
    context['day_list']=day_list
    context['firstday']=firstday
    return context    