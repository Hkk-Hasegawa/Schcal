//時刻の入力をリセットする
function reset_timeform(){
    var selectcells=document.querySelectorAll(".selecttime");
    var cellsnum=selectcells.length
    for(let step=0;step < cellsnum;step++){
        selectcells[step].classList.remove("selecttime"); 
    }
    outputtext("s_timetext","0");
    outputtext("e_timetext","0");
}
//入力時刻を表示する
function outputtext(id,time){
    var time_p = document.getElementById(id);
    var text=time_p.innerText.split(":");
    time_p.innerHTML=text[0] +":"+ time;
}
//日時をフォームに入力する開始の関数
function ev_intime(td,date,tailtime){
    const column = td.cellIndex;
    const Mycalender = document.getElementById("calender");
    const cal_tail   = Mycalender.rows[1].cells.length;
    let dateform = document.getElementById("id_date");
    dateform.value = date;
    var s_time= get_ev_starttime(td);
    var e_time=get_ev_endtime(td,tailtime);
    reset_timeform();
    const starttime  = document.getElementById("id_starttime");
    const endtime    = document.getElementById("id_endtime");
    starttime.value = s_time+":00";
    endtime.value = e_time+":00";
    outputtext("s_timetext",s_time);
    outputtext("e_timetext",e_time);
    td.classList.add("selecttime");
    td.setAttribute("id","down_td");
}
//日時入力中か判定
function ev_mouse_over(td,tailtime){
    if(document.getElementById("down_td") != null)
    {ev_fill_time(td,tailtime)}
}
//日時をフォームに入力する途中の関数
function ev_fill_time(td,tailtime){
    const column = td.cellIndex;
    const Mycalender = document.getElementById("calender");
    const cal_tail   = Mycalender.rows[1].cells.length;
    const starttime  = document.getElementById("id_starttime");
    const endtime    = document.getElementById("id_endtime");

    const down_cell = document.getElementById("down_td");
    const down_column = down_cell.cellIndex;
	const down_tr = down_cell.parentNode;
	const down_row = down_tr.sectionRowIndex;
    for(let step =1;step<cal_tail;step++){
        if(down_column <= step && step <=column || column <= step && step <=down_column){
            Mycalender.rows[down_row+1].cells[step].classList.add("selecttime")
        }else{
            Mycalender.rows[down_row+1].cells[step].classList.remove("selecttime")
        }
    }
    if(down_column==column){
        var s_time=get_ev_starttime(down_cell);
        var e_time=get_ev_endtime(down_cell,tailtime);
    }else if(down_column<column){
        var s_time=get_ev_starttime(down_cell);
        var e_time=get_ev_endtime(td,tailtime);
    }else if(down_column>column){
        var s_time=get_ev_starttime(td);
        var e_time=get_ev_endtime(down_cell,tailtime);
    }
    starttime.value = s_time+":00";
    endtime.value = e_time+":00";
    outputtext("s_timetext",s_time);
    outputtext("e_timetext",e_time);
}
//日時の入力を終了する関数<html>に入れる
function select_finish(){
    var down_cell=document.getElementById("down_td");
    if(down_cell !=null){down_cell.id = '';}
}
//選択セルから開始時刻を取得
function get_ev_starttime(td){
    const column = td.cellIndex;
    const Mycalender = document.getElementById("calender");
    var starttime=Mycalender.rows[1].cells[column].innerText;
    return starttime;
}
//選択セルから終了時刻を取得
function get_ev_endtime(td,tailtime){
    const column = td.cellIndex;
    const Mycalender = document.getElementById("calender");
    const cal_tail   = Mycalender.rows[1].cells.length;
    if (cal_tail == column+1){var endtime=tailtime;}
    else{var endtime=Mycalender.rows[1].cells[column+1].innerText;}
    //console.log(endtime);
    return endtime;
}
//行事スケジュール編集ページの初期状態に戻す関数
function ev_set_selecttime(date,starttime,endtime){
    const calender=document.getElementById("calender");
    const form_date_Value=date.substr(8,2);
    outputtext("s_timetext",starttime);
    outputtext("e_timetext",endtime);
    if(monthcheck(date,calender)){
        var set_startcol=ev_timematch(calender,starttime);
        var set_endcol=ev_timematch(calender,endtime)-1;
        var setrow =0;
        for(let step=0;step<calender.rows.length;step++){
            var th_Value=calender.rows[step].cells[0].innerText.substr(0,2);
            if(form_date_Value==th_Value){setrow=step;}
        }
        if (!(setrow==0)){
            for(let step=set_startcol;step<=set_endcol;step++){
                calender.rows[setrow].cells[step].classList.add("selecttime");
            }
        }
        
    }
}
//表示されている日付の中にdateが含まれているか判定
function monthcheck(date,calendar){
    const date_month=date.substr(0,7);
    const caption=calendar.caption.innerText.split('\n');
    const days=caption[1].split(' - ');
    var moncheck=false;
    for(let step=0;step<days.length;step++){
        var month=days[step].replace('年', '-').replace('月', ' ').split(' ');
        if(month[0]==date_month || month[0].replace('-', '-0')==date_month){moncheck=true;}
    }
return moncheck
}
//timeと一致する列を取得
function ev_timematch(calender,time){
    var setcol=0;
    for(let step=2;step<calender.rows[1].cells.length;step++){
        var cal_value=calender.rows[1].cells[step].innerText;
        cal_value=cal_value;                
        if(cal_value==time){setcol=step;}
    }   
    if(setcol==0){setcol=calender.rows[1].cells.length-1}
    return setcol;
}

//ボタンで時刻を修正
function ev_time_bottun(form_kind,up_down){
    const start_p = document.getElementById("s_timetext");
    const start_text=start_p.innerText.split(":");
    const end_p = document.getElementById("e_timetext");
    const end_text=end_p.innerText.split(":");
    if(start_text.length>2 && end_text.length >2){
        const start =start_text[1]+':'+start_text[2];
        const end =end_text[1]+':'+end_text[2];
        const Mycalender = document.getElementById("calender");
        const start_col=ev_timematch(Mycalender,start);
        const end_col=ev_timematch(Mycalender,end)-1;
        const cal_tail   = Mycalender.rows[1].cells.length-2;
        const starttime  = document.getElementById("id_starttime");
        const endtime    = document.getElementById("id_endtime");
        var selectcells=document.querySelectorAll(".selecttime");
	    const select_tr = selectcells[0].parentNode;
	    const select_row = select_tr.sectionRowIndex;
        if(form_kind=='start' && up_down=='up' && start_col>2){
            var newstart=Mycalender.rows[1].cells[start_col-1].innerText;
            starttime.value = newstart+":00";
            outputtext("s_timetext",newstart);
            Mycalender.rows[select_row+1].cells[start_col-1].classList.add("selecttime");
        }else if(form_kind=='start' && up_down=='down' && start_col<end_col){
            var newstart=Mycalender.rows[1].cells[start_col+1].innerText;
            starttime.value = newstart+":00";
            outputtext("s_timetext",newstart);
            Mycalender.rows[select_row+1].cells[start_col].classList.remove("selecttime")
        }else if(form_kind=='end' && up_down=='up' && end_col>start_col){
            var newend=Mycalender.rows[1].cells[end_col].innerText;
            endtime.value = newend+":00";
            outputtext("e_timetext",newend);
            Mycalender.rows[select_row+1].cells[end_col].classList.remove("selecttime")
        }else if(form_kind=='end' && up_down=='down' && end_col<cal_tail){
            var newend=Mycalender.rows[1].cells[end_col+2].innerText;
            endtime.value = newend+":00";
            outputtext("e_timetext",newend);
            Mycalender.rows[select_row+1].cells[end_col+1].classList.add("selecttime")
        }
    }
}