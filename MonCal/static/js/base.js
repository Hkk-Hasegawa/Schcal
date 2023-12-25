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
        const fixed_form=document.getElementById("fixed_form");
        for(let step=0;step<palces.length;step++){
            palces[step].addEventListener("click",()=> {
                room_view(palces[step])
            });
            room_view(palces[step])
        }
        if(sche_date != null && sche_start != null && sche_end != null){
            if(sche_subject !=null){
                allpre_set_selecttime(sche_subject.innerText,sche_date.innerText,sche_start.innerText,sche_end.innerText)
                input_reset.addEventListener("click",()=> {
                    allpre_set_selecttime(sche_subject.innerText,sche_date.innerText,sche_start.innerText,sche_end.innerText);
                    
                });
            }else{
                set_selecttime(sche_date.innerText,sche_start.innerText,sche_end.innerText);
                input_reset.addEventListener("click",()=> {
                    set_selecttime(sche_date.innerText,sche_start.innerText,sche_end.innerText);
                    
                });
            }
            const schedule_data=document.getElementById("schedule_data");
            schedule_data.remove();
        }else{
            input_reset.addEventListener("click",()=> {
                reset_timeform();
                
            });}
        timebutton("start_up");
        timebutton("start_down");
        timebutton("end_up");
        timebutton("end_down");
        const close_x=document.querySelectorAll(".close_x");
            close_x[0].addEventListener("click",()=> {fixed_form.classList.add("hide_elem");});
        const MCnextmonth=document.getElementById("MCnextmonth");
            MCnextmonth.addEventListener('click', get_nextmonth);
        const MCbeforemonth=document.getElementById("MCbeforemonth");
            MCbeforemonth.addEventListener('click', get_beforemonth);
        const cal_table=document.getElementById("calendar");
        const swap_cal=document.getElementById("swapcalendar");
        //行事予定の時
        if(url.includes("event")){
            swapcalendar(cal_table,swap_cal);
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    let td = input_caltr[i].cells[j];
                    let swap_td=swap_cal.rows[j].cells[i+1];
                    if((td.classList.contains("choice_cell"))){
                        td.addEventListener('mousedown', () => {
                            fixed_form.classList.add("hide_elem");
                            mousedown(td);
                            swap_mousedown(swap_td);
                        });
                    }
                    if(!(td.classList.contains("sche_box") || td.classList.contains("hide_elem"))){
                        td.addEventListener('mouseover', () => {
                            mouseover(td);
                            swap_mouseover(swap_td);
                        });
                    }
                }
            }
            for(let step=1;step<swap_cal.rows.length-1;step++){
                for(let col=1;col<swap_cal.rows[step].cells.length-1;col++){
                    let swap_td=swap_cal.rows[step].cells[col];
                    let td =cal_table.rows[col].cells[step];
                    if((swap_td.classList.contains("choice_cell"))){
                        swap_td.addEventListener('mousedown', () => {
                            fixed_form.classList.add("hide_elem");
                            mousedown(td);
                            swap_mousedown(swap_td);
                        });
                    }
                    if(!(swap_td.classList.contains("sche_box") || swap_td.classList.contains("hide_elem"))){
                        swap_td.addEventListener('mouseover', () => {
                            mouseover(td);
                            swap_mouseover(swap_td);
                        });
                    }
                }
            }
            
        }//社用車予約の時
        else if(url.includes("property")){
            swapcalendar(cal_table,swap_cal);
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    let td = input_caltr[i].cells[j];
                    let swap_td=swap_cal.rows[j].cells[i+1];
                    if(td.classList.contains("choice_cell")){
                        td.addEventListener('mousedown', () => {
                            fixed_form.classList.add("hide_elem");
                            mousedown(td);
                            swap_mousedown(swap_td);
                        });
                        td.addEventListener('mouseover', () => {
                            mouseover(td);
                            swap_mouseover(swap_td);
                        });
                    }
                }
            }
            for(let step=1;step<swap_cal.rows.length-1;step++){
                for(let col=1;col<swap_cal.rows[step].cells.length-1;col++){
                    let swap_td=swap_cal.rows[step].cells[col];
                    let td =cal_table.rows[col].cells[step];
                    if((swap_td.classList.contains("choice_cell"))){
                        swap_td.addEventListener('mousedown', () => {
                            fixed_form.classList.add("hide_elem");
                            mousedown(td);
                            swap_mousedown(swap_td);
                        });
                        swap_td.addEventListener('mouseover', () => {
                            mouseover(td);
                            swap_mouseover(swap_td);
                        });
                    }
                }
            }
        }//全体社用車予約の時
        else if(url.includes("allproperty")){
            all_swapcalender(cal_table,swap_cal);
            for (let i = 0; i < input_caltr.length; i++) {
                for(let j = 1; j < input_caltr[i].cells.length -1; j++){
                    if(input_caltr[i].cells[j].classList.contains("choice_cell")){
                        let td = input_caltr[i].cells[j];
                        let swap_td=swap_cal.rows[j].cells[i+1];
                        let subject = input_caltr[i].cells[1].innerText;
                        td.addEventListener('mousedown', () => {
                            fixed_form.classList.add("hide_elem");
                            all_car_mousedown(td,subject);
                            swap_mousedown(swap_td);
                        });
                        td.addEventListener('mouseover', () => {
                            mouseover(td);
                            swap_mouseover(swap_td);
                        });
                    }
                }

            }
            for(let step=2;step<swap_cal.rows.length-1;step++){
                for(let col=1;col<swap_cal.rows[step].cells.length-1;col++){
                    let swap_td=swap_cal.rows[step].cells[col];
                    let td =cal_table.rows[col].cells[step];
                    let subject = cal_table.rows[col].cells[1].innerText;
                    if((swap_td.classList.contains("choice_cell"))){
                        swap_td.addEventListener('mousedown', () => {
                            fixed_form.classList.add("hide_elem");
                            all_car_mousedown(td,subject);
                            swap_mousedown(swap_td);
                        });
                        swap_td.addEventListener('mouseover', () => {
                            mouseover(td);
                            swap_mouseover(swap_td);
                        });
                    }
                }
            }
        }
        const swap_button=document.getElementById("swap_button");
        swap_button.addEventListener('click',swap_switch,false);
    }else if(url.includes("list")){
        detail_hide();
        const sche_box=document.querySelectorAll(".schedule");
        for(let step=0;step<sche_box.length;step++){
            for(let i=0;i<sche_box[step].cells.length;i++){
                sche_box[step].cells[i].addEventListener('mouseover',() => {detail_show(sche_box[step])});
            }            
        }
        
        const year_schedule=document.querySelectorAll(".year_schedule");
        for(step =0;step<year_schedule.length;step++){
            if(year_schedule[step].classList.contains("first")){
                set_four_season(year_schedule[step],0,8);
            }else if(year_schedule[step].classList.contains("second")){
                set_four_season(year_schedule[step],8,16);
            }else if(year_schedule[step].classList.contains("third")){
                set_four_season(year_schedule[step],16,24);
            }        
        }
        const schedule_data=document.getElementById("schedule_data");
        schedule_data.remove();
    }else if(url.includes("yearlist")){
        const year_schedule=document.querySelectorAll(".year_schedule");
        for(step =0;step<year_schedule.length;step++){
            if(year_schedule[step].classList.contains("first")){
                set_four_season(year_schedule[step],0,8);
            }else if(year_schedule[step].classList.contains("second")){
                set_four_season(year_schedule[step],8,16);
            }else if(year_schedule[step].classList.contains("third")){
                set_four_season(year_schedule[step],16,24);
            }        
        }
        const schedule_data=document.getElementById("schedule_data");
        schedule_data.remove();
    }
}); 
//行列入れ替えたカレンダーを作成
function all_swapcalender(cal_table,swap_cal){
    const swap_cap = document.createElement("caption");
    const swap_head = document.createElement("thead");
    const swap_body = document.createElement("tbody");
    let swap_tr = document.createElement("tr");
    let swap_th =document.createElement("th");
    const before=document.getElementById("before");
    const next=document.getElementById("next");
    const headtime=document.getElementById("headtime");
    const tailtime=document.getElementById("tailtime");
    swap_tr=input_swap_cell(swap_tr,"th",before);
    for(let step=1;step<cal_table.rows.length;step++){
        let date_th=cal_table.rows[step].cells[0];
        let swap_date= document.createElement("th");
        swap_date.colSpan=date_th.rowSpan;
        swap_date.className=date_th.className;
        swap_date.innerHTML=date_th.innerHTML;
        swap_tr.appendChild(swap_date);
    }
    swap_tr=input_swap_cell(swap_tr,"th",next);
    swap_head.appendChild(swap_tr);
    swap_tr = document.createElement("tr");
    swap_th =document.createElement("th");
    swap_tr=input_swap_cell(swap_tr,"th",headtime);
    for(let step=1;step<cal_table.rows.length;step++){
        let car_th = cal_table.rows[step].cells[1];
        swap_tr=input_swap_cell(swap_tr,"th",car_th);
    }
    swap_tr=input_swap_cell(swap_tr,"th",headtime);
    swap_head.appendChild(swap_tr);
    for(let column=2;column<cal_table.rows[1].cells.length-2;column++){
        let swap_tr = document.createElement("tr");
        swap_tr=input_swap_cell(swap_tr,"th",cal_table.rows[0].cells[column]);
        for(let row=1;row<cal_table.rows.length;row++){
            swap_tr=input_swap_cell(swap_tr,"td",cal_table.rows[row].cells[column]);
        }
        swap_tr=input_swap_cell(swap_tr,"th",cal_table.rows[0].cells[column]);
        swap_body.appendChild(swap_tr);
    }
    swap_tr = document.createElement("tr");
    swap_tr=input_swap_cell(swap_tr,"th",tailtime);
    for(let step=1;step<cal_table.rows.length;step++){
        let car_th = cal_table.rows[step].cells[1];
        swap_tr=input_swap_cell(swap_tr,"th",car_th);
    }
    swap_tr=input_swap_cell(swap_tr,"th",tailtime);
    swap_body.appendChild(swap_tr);
    swap_cap.innerHTML=cal_table.caption.innerHTML;
    swap_cal.appendChild(swap_cap);
    swap_cal.appendChild(swap_head);
    swap_cal.appendChild(swap_body);
    return swap_cal;
}
function swapcalendar(cal_table,swap_cal){
    const swap_head = document.createElement("thead");
        swap_head.appendChild(swap_top_bottom(cal_table,"top"));
    const swap_body = document.createElement("tbody");
    for(let column=1;column<cal_table.rows[1].cells.length-1;column++){
        let swap_tr = document.createElement("tr");
        swap_tr=input_swap_cell(swap_tr,"th",cal_table.rows[0].cells[column]);
        for(let row=1;row<cal_table.rows.length;row++){
            swap_tr=input_swap_cell(swap_tr,"td",cal_table.rows[row].cells[column]);
        }
        swap_tr=input_swap_cell(swap_tr,"th",cal_table.rows[0].cells[column]);
        swap_body.appendChild(swap_tr);
    }
    swap_body.appendChild(swap_top_bottom(cal_table,"bottom"));
    const swap_cap = document.createElement("caption");
    swap_cap.innerHTML=cal_table.caption.innerHTML;
    swap_cal.appendChild(swap_cap);
    swap_cal.appendChild(swap_head);
    swap_cal.appendChild(swap_body);
    return swap_cal;
}
function swap_top_bottom(cal_table,top_bottom){
    const swap_tr = document.createElement("tr");
    const headtime=document.getElementById("headtime");
    const tailtime=document.getElementById("tailtime");
    if(top_bottom=="top"){
        const swap_th= document.createElement("th");
        swap_th.innerHTML=headtime.innerHTML;
        swap_th.className=headtime.className;
        swap_tr.appendChild(swap_th);
    }else{
        const swap_th= document.createElement("th");
        swap_th.innerText=tailtime.innerText.split("\n")[1];
        swap_th.className=tailtime.className;
        swap_tr.appendChild(swap_th);
    }
    for(let step=1;step<cal_table.rows.length;step++){
        let swap_th= document.createElement("th");
        swap_th.colSpan=cal_table.rows[step].cells[0].rowSpan;
        swap_th.className=cal_table.rows[step].cells[0].className;
        swap_th.innerHTML=cal_table.rows[step].cells[0].innerHTML;
        swap_tr.appendChild(swap_th);
    }
    if(top_bottom=="top"){
        const swap_th= document.createElement("th");
        swap_th.innerHTML=tailtime.innerHTML.split("<br>")[0]+"<br>"+headtime.innerText.split("\n")[1];
        swap_th.className=tailtime.className;
        swap_tr.appendChild(swap_th);
    }else{
        const swap_th= document.createElement("th");
        swap_th.innerText=tailtime.innerText.split("\n")[1];
        swap_th.className=tailtime.className;
        swap_tr.appendChild(swap_th);
    }
    return swap_tr
}
function input_swap_cell(swap_tr,elem,cell){
    const swap_cell= document.createElement(elem);
    swap_cell.rowSpan=cell.colSpan;
    swap_cell.className=cell.className;
    swap_cell.innerHTML=cell.innerHTML;
    swap_tr.appendChild(swap_cell);
    return swap_tr
}
function swap_switch(){
    const cal_table=document.getElementById("calendar");
    const swap_cal=document.getElementById("swapcalendar");
    if(cal_table.classList.contains("hide_elem")){
        cal_table.classList.remove("hide_elem");
        swap_cal.classList.add("hide_elem");
    }else{
        cal_table.classList.add("hide_elem");
        swap_cal.classList.remove("hide_elem");
    }
}

//セルを選択した時の関数
function mousedown(td){
    const input_caltr = td.parentNode;
    const date = input_caltr.className.split(" ")[0];
    inputdate(date);
    //ここまでが日付に関するもの
    reset_timeform();
    const start= st_time(td,"calendar");
    const end= ed_time(td,"calendar");
    input_time(start,end);
    td.classList.add("selecttime");
    td.setAttribute("id","down_td");
}
function swap_mousedown(td){
    td.classList.add("selecttime");
    td.setAttribute("id","swap_down");
}
//社用車全体用
function all_car_mousedown(td,subject){
    const id_subject = document.getElementById('id_subject');
    let options = id_subject.options;
    for(let step=0;step<options.length;step++){
        if(options[step].innerText==subject){options[step].selected = true;}
    }
    mousedown(td)
}
function mouseover(td){
    if(document.getElementById("down_td") == null){}
    else{fill_time(td);}
}
function fill_time(td){
    const down_cell = document.getElementById("down_td");
    const down_tr = down_cell.parentNode;
    const column = td.cellIndex;
    const down_col = down_cell.cellIndex;
    let start_time="";
    let end_time="";
    if(down_col<column){
        for(let step=1;step<down_col;step++){
            down_tr.cells[step].classList.remove("selecttime");
        }
        let endcol=column;
        for(let step =down_col;step<=column;step++){
            if(!(down_tr.cells[step].classList.contains("choice_cell"))){
                endcol=step-1;
                break;
            }
            down_tr.cells[step].classList.add("selecttime");
        }
        for(let step=endcol+1;step<down_tr.cells.length;step++){
            down_tr.cells[step].classList.remove("selecttime");
        }
        start_time=st_time(down_cell,"calendar");
        
        end_time=ed_time(down_tr.cells[endcol],"calendar");
    }else{
        for(let step=down_tr.cells.length;step<down_col;step--){
            down_tr.cells[step].classList.remove("selecttime");
        }
        let startcol=column;
        for(let step =down_col;step>=column;step--){
            if(!(down_tr.cells[step].classList.contains("choice_cell"))){
                startcol=step+1;
                break;
            }
            down_tr.cells[step].classList.add("selecttime");
        }
        for(let step=startcol-1;step>0;step--){
            down_tr.cells[step].classList.remove("selecttime");
        }
        start_time=st_time(down_tr.cells[startcol],"calendar");
        end_time=ed_time(down_cell,"calendar");
    }
    input_time(start_time,end_time);
}

function swap_mouseover(td){
    if(document.getElementById("swap_down") == null){}
    else{swap_fill(td);}
}
function swap_fill(td){
    const swap_cal=document.getElementById("swapcalendar");
    const down_cell = document.getElementById("swap_down");
    const down_row=down_cell.parentNode.rowIndex;
    const row=td.parentNode.rowIndex;
    const down_col = down_cell.cellIndex;
    if(down_row<row){
        for(let step=1;step<down_row;step++){
            swap_cal.rows[step].cells[down_col].classList.remove("selecttime");
        }
        let endrow=row;
        for(let step =down_row;step<=row;step++){
            if(!(swap_cal.rows[step].cells[down_col].classList.contains("choice_cell"))){
                endrow=step-1;
                break;
            }
            swap_cal.rows[step].cells[down_col].classList.add("selecttime");
        }
        for(let step=endrow+1;step<swap_cal.rows.length-1;step++){
            swap_cal.rows[step].cells[down_col].classList.remove("selecttime");
        }
    }else{
        for(let step=swap_cal.rows.length;step<down_row;step--){
            swap_cal.rows[step].cells[down_col].classList.remove("selecttime");
        }
        let startrow=row;
        for(let step =down_row;step>=row;step--){
            if(!(swap_cal.rows[step].cells[down_col].classList.contains("choice_cell"))){
                startrow=step+1;
                break;
            }
            swap_cal.rows[step].cells[down_col].classList.add("selecttime");
        }
        for(let step=startrow-1;step>0;step--){
            swap_cal.rows[step].cells[down_col].classList.remove("selecttime");
        }
    }
}
function swap_eff(startrow,endrow,swap_column){
    const swap_cal=document.getElementById("swapcalendar");
    for(let step=0;step<swap_cal.rows.length;step++){
        if(startrow <=step && step <=endrow){
            swap_cal.rows[step].cells[swap_column].classList.add("selecttime");
        }else{
            swap_cal.rows[step].cells[swap_column].classList.remove("selecttime");
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
        const startcol= get_column(starttime)-1;
        const endcol= get_column(endtime);
        const row=input_tr.rowIndex;
        for(let step=1;step<cal_tail-1;step++){
            if(startcol<step && step <endcol){
                input_tr.cells[step].classList.add("selecttime");
            }
        }
        swap_eff(startcol,endcol,row);
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
function get_column(time){
    const calendar=document.getElementById("calendar");
    for(let step=1;step<calendar.rows[0].cells.length-1;step++){
        if(calendar.rows[0].cells[step].classList.contains(time)){
            return step;
        }
    }
    

}
//日時の入力を終了する関数<html>に入れる
function select_finish(){
    const down_cell=document.getElementById("down_td");
    const fixed_form=document.getElementById("fixed_form");
    if(down_cell !=null){
        down_cell.id = '';
        fixed_form.classList.remove("hide_elem");
    }
    const swap_down=document.getElementById("swap_down");
    if(swap_down !=null){
        swap_down.id = '';
        fixed_form.classList.remove("hide_elem");
    }
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
    const time_p = document.getElementById(id);
    if(time_p!=null){
        const text=time_p.innerText.split(":");
        time_p.innerText=text[0] +":"+ time;
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
    const tailtime_cell= document.getElementById("tailtime");
    const tailtime=tailtime_cell.className.split(" ")[0];
    return tailtime;
}
//選択セルから開始時刻を取得
function st_time(td,id){
    const calender=document.getElementById(id);
    const column = td.cellIndex;
    const time=calender.rows[0].cells[column].className.split(" ")[0];
    return time
}
//選択セルから終了時刻を取得
function ed_time(td,id){
    const calender=document.getElementById(id);
    const tr = td.parentNode;
    const row =tr.rowIndex;
    const column = td.cellIndex;
    let time="";
    const next_cell=calender.rows[row].cells[column+1];
    if(next_cell.tagName=="TD"){
        time=calender.rows[0].cells[column+1].className.split(" ")[0];
    }else{
        time=get_tailtime();
    }
    return time
}

//月カレンダー操作
//来月のカレンダー生成
function get_nextmonth(){
    const monthcalendar= document.getElementById("monthcalendar");
    const caption= monthcalendar.tHead.rows[0].cells[1].innerText;
    const cap_arr=caption.split(/年|月/);
    const year=cap_arr[0];
    const month=cap_arr[1];
    if(month ==12){ next_firstday = new Date(Number(year)+1,0);}
    else{  next_firstday = new Date(year,Number(month) % 12);}
    makeMonthcalendar(next_firstday);
}
//先月のカレンダーを生成
function get_beforemonth(){
    const monthcalendar= document.getElementById("monthcalendar");
    const caption= monthcalendar.tHead.rows[0].cells[1].innerText;
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
    const calendar= document.getElementById("calendar");
    const basedate=calendar.caption.innerText.split(/\n| - /)[1].split(/年|月|日/);
    console.log(basedate)
    const url= location.pathname.split("/")

    console.log(checkmonth)
    monthcalendar.tHead.rows[0].cells[1].innerText=String(capyear) + "年"+String(checkmonth+1)+"月";
    for(step=2;step<8;step++){
        input_list=MW_list[step-2];
        for(let column=0;column<7;column++){
            if(input_list[column]!=0){
                if(url[1]=="event" && !(url[3]=="edit")){
                    href=[url[1],url[2],String(input_list[column].getFullYear()),String(input_list[column].getMonth()+1),String(input_list[column].getDate())];
                }else if(url[1]=="event" && url[3]=="edit"){
                    href=[url[1],url[2],url[3],url[4],String(input_list[column].getFullYear()),String(input_list[column].getMonth()+1),String(input_list[column].getDate())];
                }
                else{
                    href=[url[1],url[2],url[3],String(input_list[column].getFullYear()),String(input_list[column].getMonth()+1),String(input_list[column].getDate())];
                }
                monthcalendar.rows[step].cells[column].innerHTML="<a href=\"/"+href.join('/')+"/\">"+String(input_list[column].getDate())+"</a>";
                if(input_list[column].getFullYear()==basedate[0] && input_list[column].getMonth()+1==basedate[1] && input_list[column].getDate()==basedate[2]){monthcalendar.rows[step].cells[column].classList.add("base_date")}
            }else{monthcalendar.rows[step].cells[column].innerText=""}   
        }
    }
}