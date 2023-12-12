//スケジュール編集ページの時の初期動作
window.addEventListener("load", () => {
    const url= location.pathname.split("/")
    console.log(url)
    if( (url.includes("edit") ||  url.includes("calendar"))){
        //どこでマウスを離してもいいように
        let html = document.getElementsByTagName('html')[0];
        html.addEventListener('mouseup', select_finish ,false );
        //予定があるページの共通要素
        let sche_date=document.getElementById("sche_date");
        let sche_start=document.getElementById("sche_start");
        let sche_end=document.getElementById("sche_end");
        let input_reset=document.getElementById("input_reset");
        const input_caltr=document.querySelectorAll(".input_caltr");
        if(sche_date != null && sche_start != null && sche_end != null){
            ev_set_selecttime(sche_date.innerText,sche_start.innerText,sche_end.innerText);
            input_reset.addEventListener("click",
            ()=> {ev_set_selecttime(sche_date.innerText,sche_start.innerText,sche_end.innerText);});
        }else{input_reset.addEventListener("click",()=> {reset_timeform();});}
        timebutton("start_up");
        timebutton("start_down");
        timebutton("end_up");
        timebutton("end_down");
        let MCnextmonth=document.getElementById("MCnextmonth");
            MCnextmonth.addEventListener('click', get_nextmonth);
        let MCbeforemonth=document.getElementById("MCbeforemonth");
            MCbeforemonth.addEventListener('click', get_beforemonth);
        //行事予定の時
        if(url.includes("event")){
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    let td = input_caltr[i].cells[j];
                    if((td.classList.contains("choice_cell"))){
                        td.addEventListener('mousedown', () => {ev_mouse_down(td)});
                    }
                    td.addEventListener('mouseover', () => {ev_mouse_over(td)});
                }
            }
        }//社用車予約の時
        else if(url.includes("property")){
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    if(input_caltr[i].cells[j].classList.contains("choice_cell")){
                        let date = input_caltr[i].id;
                        let td = input_caltr[i].cells[j];
                        td.addEventListener('mousedown', () => {sub_mousedown(td,date)});
                        td.addEventListener('mouseover', () => {sub_mouseover(td)});
                    }
                }
            }
        }
        else if(url.includes("allproperty")){
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    if(input_caltr[i].cells[j].classList.contains("choice_cell")){
                        let date = input_caltr[i].className.split(" ")[0];
                        let td = input_caltr[i].cells[j];
                        let subject = get_subject(input_caltr[i])
                        td.addEventListener('mousedown', () => {all_sub_mousedown(td,date,subject)});
                        td.addEventListener('mouseover', () => {sub_mouseover(td)});
                    }
                }
            }
            
        }
    }
}); 
//時刻調整ボタン用のaddEventListener
function timebutton(id){
    let btn_elem=document.getElementById(id);
    let id_list=id.split("_")
    btn_elem.addEventListener("click",()=> {ev_time_bottun(id_list[0],id_list[1]);});
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
//次の月のカレンダー生成

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
                href=["",url[1],url[2],url[3],String(input_list[column].getFullYear()),String(input_list[column].getMonth()+1),String(input_list[column].getDate())];
                monthcalednar.rows[step].cells[column].innerHTML="<a href=\""+href.join('/')+"/\">"+String(input_list[column].getDate())+"</a>";
                if(input_list[column].getFullYear()==basedate[0] && input_list[column].getMonth()+1==basedate[1] && input_list[column].getDate()==basedate[2]){monthcalednar.rows[step].cells[column].classList.add("base_date")}
            }else{monthcalednar.rows[step].cells[column].innerText=""}   
        }
    }
}