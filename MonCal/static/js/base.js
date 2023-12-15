//スケジュール編集ページの時の初期動作
window.addEventListener("load", () => {
    const url= location.pathname.split("/")
    console.log(url)
    const message=document.querySelectorAll(".message");
    if(message.length>0){
        let messages=""
        for(step=0;step<message.length;step++){
            messages=message[step].innerText+"\n"
        }
        alert(messages);
    }
    if( (url.includes("edit") ||  url.includes("calendar"))){
        //どこでマウスを離してもいいように
        const html = document.getElementsByTagName('html')[0];
        html.addEventListener('mouseup', select_finish ,false );
        //予定があるページの共通要素
        const sche_subject=document.getElementById("sche_subject");
        const sche_date=document.getElementById("sche_date");
        const sche_start=document.getElementById("sche_start");
        const sche_end=document.getElementById("sche_end");
        const input_reset=document.getElementById("input_reset");
        const input_caltr=document.querySelectorAll(".input_caltr");
        const palces = document.getElementsByName('place');
        for(let step=0;step<palces.length;step++){
            let place_pk='place_room_'+palces[step].value
            let room_ul=document.getElementById(place_pk);
            palces[step].addEventListener("click",()=> {
                if (palces[step].checked == true) {
                    room_ul.style.display = '';
                  } else {
                    room_ul.style.display = 'none';
                    let roomlist=document.querySelectorAll("."+place_pk);
                    for(let i=0;i<roomlist.length;i++){
                        roomlist[i].checked=false;
                    }
                  }
                
            });
        }
        if(sche_date != null && sche_start != null && sche_end != null){
            if(sche_subject !=null){
                allpre_set_selecttime(sche_subject.innerText,sche_date.innerText,sche_start.innerText,sche_end.innerText)
                input_reset.addEventListener("click",
                ()=> {allpre_set_selecttime(sche_subject.innerText,sche_date.innerText,sche_start.innerText,sche_end.innerText);});
            }else{
                set_selecttime(sche_date.innerText,sche_start.innerText,sche_end.innerText);
                input_reset.addEventListener("click",
                ()=> {set_selecttime(sche_date.innerText,sche_start.innerText,sche_end.innerText);});
            }
        }else{input_reset.addEventListener("click",()=> {reset_timeform();});}
        timebutton("start_up");
        timebutton("start_down");
        timebutton("end_up");
        timebutton("end_down");
        const MCnextmonth=document.getElementById("MCnextmonth");
            MCnextmonth.addEventListener('click', get_nextmonth);
        const MCbeforemonth=document.getElementById("MCbeforemonth");
            MCbeforemonth.addEventListener('click', get_beforemonth);
        //行事予定の時
        if(url.includes("event")){
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    let td = input_caltr[i].cells[j];
                    if((td.classList.contains("choice_cell"))){
                        td.addEventListener('mousedown', () => {mousedown(td)});
                    }
                    td.addEventListener('mouseover', () => {mouseover(td,"event")});
                }
            }
            
        }//社用車予約の時
        else if(url.includes("property")){
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    if(input_caltr[i].cells[j].classList.contains("choice_cell")){
                        let td = input_caltr[i].cells[j];
                        td.addEventListener('mousedown', () => {mousedown(td)});
                        td.addEventListener('mouseover', () => {mouseover(td,"subject")});
                    }
                }
            }
        }
        else if(url.includes("allproperty")){
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    if(input_caltr[i].cells[j].classList.contains("choice_cell")){
                        let td = input_caltr[i].cells[j];
                        let subject = input_caltr[i].cells[1].innerText;
                        td.addEventListener('mousedown', () => {all_sub_mousedown(td,subject)});
                        td.addEventListener('mouseover', () => {mouseover(td,"subject")});
                    }
                }
            }
            
        }
    }else if(url.includes("list")){
        detail_hide();
        const sche_box=document.querySelectorAll(".schedule");
        for(let step=0;step<sche_box.length;step++){
            for(let i=0;i<sche_box[step].cells.length;i++){
                sche_box[step].cells[i].addEventListener('mouseover',() => {detail_show(sche_box[step])});
            }            
        }
    }
}); 

//セルををした時の関数
function mousedown(td){
    const input_caltr = td.parentNode;
    const date = input_caltr.className.split(" ")[0];
    inputdate(date);
    //ここまでが日付に関するもの
    reset_timeform();
    const start= get_starttime(td);
    const end= get_endtime(td)
    input_time(start,end);
    td.classList.add("selecttime");
    td.setAttribute("id","down_td");
}
function mouseover(td,sche_type){
    if(document.getElementById("down_td") == null){}
    else if(sche_type=="subject"){sub_fill_time(td)}
    else if(sche_type=="event"){ev_fill_time(td)}
}
//時刻調整ボタン用のaddEventListener
function timebutton(id){
    let btn_elem=document.getElementById(id);
    let id_list=id.split("_")
    btn_elem.addEventListener("click",()=> {time_btn(id_list[0],id_list[1]);});
}
//ボタンで時刻を修正
function time_btn(form_kind,up_down){
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
//スケジュール編集ページの初期状態に戻す関数
function set_selecttime(date,starttime,endtime){
    reset_timeform()
    inputdate(date);
    input_time(starttime,endtime);
    const input_tr=date_check(date);
    if(input_tr!=null){
        const cal_tail = input_tr.cells.length;
        let selectF = false;
        for(let step =1;step<cal_tail;step++){
            let checktd=input_tr.cells[step];
            selectF=select_cells(checktd,selectF,starttime,endtime);
        }
    }
}
function allpre_set_selecttime(subject,date,starttime,endtime){
    reset_timeform()
    inputdate(date);
    input_time(starttime,endtime);
    const input_tr_list=document.querySelectorAll(".input_caltr");
    let input_tr=null;
    for(let step=0;step<input_tr_list.length;step++){
        let tr_date=input_tr_list[step].className.split(" ")[0];
        let tr_subject=input_tr_list[step].cells[1].innerText;
        if(tr_date==date && tr_subject==subject){input_tr=input_tr_list[step]}
    }
    if(input_tr!=null){
        const cal_tail = input_tr.cells.length;
        let selectF = false;
        for(let step =1;step<cal_tail;step++){
            let checktd=input_tr.cells[step];
            selectF=select_cells(checktd,selectF,starttime,endtime);
        }
    }
}
//選択セルの右端を取得
function starttime_td(selectcells){
    let start=-1;
    for(let step=0;step<selectcells.length;step++){
        if(selectcells[step].cellIndex < start || start < 0){
            start=selectcells[step].cellIndex;
        }
    }
    return start
}
function endtime_td(selectcells){
    let end=-1;
    for(let step=0;step<selectcells.length;step++){
        if(selectcells[step].cellIndex > end || end < 0){
            end=selectcells[step].cellIndex;
        }
    }
    return end
}
//日時の入力を終了する関数<html>に入れる
function select_finish(){
    var down_cell=document.getElementById("down_td");
    if(down_cell !=null){down_cell.id = '';}
}
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
    if(time_p!=null){
        var text=time_p.innerText.split(":");
        time_p.innerHTML=text[0] +":"+ time;
    }
}

//フォームに日付を入力
function inputdate(date){
    const dateform = document.getElementById("id_date");
    dateform.value = date;
}
//フォームに時刻を入力
function input_time(start,end){
    const starttime  = document.getElementById("id_starttime");
    const endtime    = document.getElementById("id_endtime");
    starttime.value = start+":00";
    endtime.value = end+":00";
    outputtext("s_timetext",start);
    outputtext("e_timetext",end);
}

//表示されている日付の中にdateが含まれているか判定
function date_check(date){
    const input_tr_list=document.querySelectorAll(".input_caltr");
    for(let step=0;step<input_tr_list.length;step++){
        let tr_date=input_tr_list[step].className.split(" ")[0];
        if(tr_date==date){return input_tr_list[step]}
    }
}
//最終時刻を取得
function get_tailtime(){
    const tailtime_cell= document.getElementById("tailtime").innerText.split('\n')
    if(tailtime_cell.length ==2){var tailtime= tailtime_cell[1];}
    else{var tailtime= tailtime_cell[0];}
    return tailtime
}
//選択セルから開始時刻を取得
function get_starttime(td){
    var starttime=td.className.split(" ")[0];
    return starttime;
}
//選択セルから終了時刻を取得
function get_endtime(td){
    const tailtime=get_tailtime();
    const column = td.cellIndex;
    const tr = td.parentNode;
	const row = tr.sectionRowIndex;
    const Mycalendar = document.getElementById("calendar");
    const cal_tail   = Mycalendar.rows[row+1].cells.length;
    if(column+1==cal_tail){var endtime=tailtime;}
    else if( Mycalendar.rows[row+1].cells[column+1].classList.contains("date_col") || Mycalendar.rows[row+1].cells[column+1].classList.contains("sub_name_cell")){var endtime=tailtime;}
    else{var endtime=Mycalendar.rows[row+1].cells[column+1].className.split(" ")[0];}
    return endtime;
}
//月カレンダー操作
//来月のカレンダー生成
function get_nextmonth(){
    const monthcalednar= document.getElementById("monthcalednar");
    const caption= monthcalednar.tHead.rows[0].cells[1].innerText;
    const cap_arr=caption.split(/年|月/);
    const year=cap_arr[0];
    const month=cap_arr[1];
    if(month ==12){ next_firstday = new Date(Number(year)+1,0);}
    else{  next_firstday = new Date(year,Number(month) % 12);}
    makeMonthcalendar(next_firstday);
}
//先月のカレンダーを生成
function get_beforemonth(){
    const monthcalednar= document.getElementById("monthcalednar");
    const caption= monthcalednar.tHead.rows[0].cells[1].innerText;
    const cap_arr=caption.split(/年|月/);
    const year=cap_arr[0];
    const month=cap_arr[1];
    if(month ==1){ before_firstday = new Date(Number(year)-1,11);}
    else{  before_firstday = new Date(year,Number(month) -2);}
    makeMonthcalendar(before_firstday);
}
//月初めからその月のカレンダーを作成
function makeMonthcalendar(firstday){
    const checkmonth=firstday.getMonth();
    const capyear=firstday.getFullYear();
    firstweek_list=[0,0,0,0,0,0,0];
    next_day=firstday;
    for(let step=0;step<firstweek_list.length;step++){
        if((next_day.getDay()+6) % 7 ==step){
            firstweek_list[step]=new Date(next_day.getFullYear(),next_day.getMonth(),next_day.getDate());
            next_day.setDate(next_day.getDate() + 1 );
        }
    }
    MW_list=[0,0,0,0,0,0];
    MW_list[0]=firstweek_list;
    for(let i=1;i<MW_list.length;i++){
        week_list=[0,0,0,0,0,0,0];
        for(let step=0;step<week_list.length;step++){
            if(next_day.getMonth() == checkmonth){
                week_list[step]=new Date(next_day.getFullYear(),next_day.getMonth(),next_day.getDate());
                next_day.setDate(next_day.getDate() + 1 );
            }
        }
        MW_list[i]=[week_list[0],week_list[1],week_list[2],week_list[3],week_list[4],week_list[5],week_list[6]];
    }
    var selectcells=document.querySelectorAll(".base_date");
    var cellsnum=selectcells.length
    for(let step=0;step < cellsnum;step++){
        selectcells[step].classList.remove("base_date"); 
    }
    const calednar= document.getElementById("calendar");
    const basedate=calednar.caption.innerText.split(/\n| - /)[1].split(/年|月|日/);
    console.log(basedate)
    const url= location.pathname.split("/")

    console.log(checkmonth)
    monthcalednar.tHead.rows[0].cells[1].innerText=String(capyear) + "年"+String(checkmonth+1)+"月";
    for(step=2;step<8;step++){
        input_list=MW_list[step-2];
        for(let column=0;column<7;column++){
            if(input_list[column]!=0){
                if(url[1]="event"){
                    href=[url[1],url[2],String(input_list[column].getFullYear()),String(input_list[column].getMonth()+1),String(input_list[column].getDate())];
                }else{
                    href=[url[1],url[2],url[3],String(input_list[column].getFullYear()),String(input_list[column].getMonth()+1),String(input_list[column].getDate())];
                }
                monthcalednar.rows[step].cells[column].innerHTML="<a href=\"/"+href.join('/')+"/\">"+String(input_list[column].getDate())+"</a>";
                if(input_list[column].getFullYear()==basedate[0] && input_list[column].getMonth()+1==basedate[1] && input_list[column].getDate()==basedate[2]){monthcalednar.rows[step].cells[column].classList.add("base_date")}
            }else{monthcalednar.rows[step].cells[column].innerText=""}   
        }
    }
}