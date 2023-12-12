//日時をフォームに入力する開始の関数
function ev_mouse_down(td){
    const tailtime=get_tailtime();
    let tr = td.parentNode;
    let date= tr.id;
    let dateform = document.getElementById("id_date");
    dateform.value = date;
    let s_time= get_starttime(td);
    let e_time=get_endtime(td,tailtime);
    reset_timeform();
    let starttime  = document.getElementById("id_starttime");
    let endtime    = document.getElementById("id_endtime");
    starttime.value = s_time+":00";
    endtime.value = e_time+":00";
    outputtext("s_timetext",s_time);
    outputtext("e_timetext",e_time);
    td.classList.add("selecttime");
    td.setAttribute("id","down_td");
}
//日時入力中か判定
function ev_mouse_over(td){
    if(document.getElementById("down_td") != null)
    {ev_fill_time(td)}
}
//日時をフォームに入力する途中の関数
function ev_fill_time(td){
    const column = td.cellIndex;
    const Mycalendar = document.getElementById("calendar");
    
    const starttime  = document.getElementById("id_starttime");
    const endtime    = document.getElementById("id_endtime");

    const down_cell = document.getElementById("down_td");
    const down_column = down_cell.cellIndex;
	const down_tr = down_cell.parentNode;
	const down_row = down_tr.sectionRowIndex;
    const cal_tail   = Mycalendar.rows[down_row+1].cells.length;
    const down_time=down_cell.className.split(" ")[0]
    const td_time=td.className.split(" ")[0]
    selectF=false;
    if(comparison_time(down_time,td_time)){
        var s_time=get_starttime(down_cell);
        var e_time=get_endtime(td);
        for(let step =1;step<cal_tail;step++){
            let checktd=Mycalendar.rows[down_row+1].cells[step];
            if(checktd.classList.contains(s_time)){selectF=true;}
            if(checktd.classList.contains(e_time)){selectF=false;}
            if(selectF){checktd.classList.add("selecttime")}
            else{checktd.classList.remove("selecttime")}
            
        }
    }else{
        var s_time=get_starttime(td);
        var e_time=get_endtime(down_cell);
        for(let step =1;step<cal_tail;step++){
            let checktd=Mycalendar.rows[down_row+1].cells[step];
            if(checktd.classList.contains(s_time)){selectF=true;}
            if(checktd.classList.contains(e_time)){selectF=false;}
            if(selectF){checktd.classList.add("selecttime")}
            else{checktd.classList.remove("selecttime")}
        }
    }
    starttime.value = s_time+":00";
    endtime.value = e_time+":00";
    outputtext("s_timetext",s_time);
    outputtext("e_timetext",e_time);
}
function comparison_time(down_time,td_time){
    const down_hour=Number(down_time.split(":")[0]);
    const down_min=Number(down_time.split(":")[1]);
    const td_hour=Number(td_time.split(":")[0]);
    const td_min=Number(td_time.split(":")[1]);
    
    if(down_hour<td_hour){result=true}
    else if(down_hour>td_hour){result=false}
    else{if(down_min<=td_min){result=true}
        else{result=false}}
    return result
}
//選択セルから開始時刻を取得

//行事スケジュール編集ページの初期状態に戻す関数
function ev_set_selecttime(date,starttime,endtime){
    reset_timeform()
    const calendar=document.getElementById("calendar");
    const form_date_Value=date.substr(8,2);
    outputtext("s_timetext",starttime);
    outputtext("e_timetext",endtime);
    if(monthcheck(date,calendar)){
        var set_startcol=ev_timematch(calendar,starttime);
        var set_endcol=ev_timematch(calendar,endtime)-1;
        var setrow =0;
        for(let step=0;step<calendar.rows.length;step++){
            var th_Value=calendar.rows[step].cells[0].innerText.substr(0,2);
            if(form_date_Value==th_Value){setrow=step;}
        }
        if (!(setrow==0)){
            for(let step=set_startcol;step<=set_endcol;step++){
                calendar.rows[setrow].cells[step].classList.add("selecttime");
            }
        }
        
    }
}
//timeと一致する列を取得
function ev_timematch(calendar,time){
    var setcol=0;
    for(let step=1;step<calendar.rows[1].cells.length;step++){
        var cal_value=calendar.rows[1].cells[step].innerText;
        cal_value=cal_value;                
        if(cal_value==time){setcol=step;}
    }   
    if(setcol==0){setcol=calendar.rows[1].cells.length-1}
    return setcol;
}
function starttime_td(selectcells){
    let start=-1;
    for(let step=0;step<selectcells.length;step++){
        if(selectcells[step].cellIndex < start || start < 0){
            start=selectcells[step].cellIndex;
            start_td=selectcells[step];
        }
    }
    return start
}
function endtime_td(selectcells){
    let end=-1;
    for(let step=0;step<selectcells.length;step++){
        if(selectcells[step].cellIndex > end || end < 0){
            end=selectcells[step].cellIndex;
            end_td=selectcells[step];
        }
    }
    return end
}
//ボタンで時刻を修正
function ev_time_bottun(form_kind,up_down){
    var selectcells=document.querySelectorAll(".selecttime");
    if(selectcells.length>0){
        const select_tr = selectcells[0].parentNode;
        const hide_times_tr = document.getElementById("hide_times_tr");
        const starttime  = document.getElementById("id_starttime");
        const endtime    = document.getElementById("id_endtime");
        const start_col=starttime_td(selectcells);
        const end_col=endtime_td(selectcells);
        if(form_kind=='start' && up_down=='up' 
            && select_tr.cells[start_col-1].classList.contains( "choice_cell" )){
            let newstart=hide_times_tr.cells[start_col-1].className.split(" ")[0];
            starttime.value = newstart+":00";
            outputtext("s_timetext",newstart);
            select_tr.cells[start_col-1].classList.add("selecttime");
        }else if(form_kind=='start' && up_down=='down' && start_col!=end_col){
            let newstart=hide_times_tr.cells[start_col+1].className.split(" ")[0];
            starttime.value = newstart+":00";
            outputtext("s_timetext",newstart);
            select_tr.cells[start_col].classList.remove("selecttime")
        }else if(form_kind=='end' && up_down=='up' && end_col!=start_col){
            var newend=hide_times_tr.cells[end_col].className.split(" ")[0];
            endtime.value = newend+":00";
            outputtext("e_timetext",newend);
            select_tr.cells[end_col].classList.remove("selecttime")
        }else if(form_kind=='end' && up_down=='down'  
        && select_tr.cells[end_col+1].classList.contains( "choice_cell" )){
            var newend=hide_times_tr.cells[end_col+2].className.split(" ")[0];
            endtime.value = newend+":00";
            outputtext("e_timetext",newend);
            select_tr.cells[end_col+1].classList.add("selecttime")
        }
    }
}