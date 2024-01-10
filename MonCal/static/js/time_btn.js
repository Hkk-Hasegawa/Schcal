//ボタン用関数
//時刻調整ボタン用のaddEventListener
function timebutton(id){
    let btn_elem=document.getElementById(id);
    let id_list=id.split("_")
    btn_elem.addEventListener("click",()=> {time_btn(id_list[0],id_list[1]);});
}
//ボタンで時刻を修正
function time_btn(form_kind,up_down){
    const selectcells=document.querySelectorAll("#calendar .selecttime");
    if(selectcells.length>0){
        const calendar  = document.getElementById("calendar");
        const select_tr = selectcells[0].parentNode;
        const starttime  = document.getElementById("id_starttime");
        const endtime    = document.getElementById("id_endtime");
        const start_col=starttime_td(selectcells);
        const end_col=endtime_td(selectcells);
        let id="";
        let new_value="";
        let startrow=0;
        let endrow=0;
        if(form_kind=='start' && up_down=='up' 
            && select_tr.cells[start_col-1].classList.contains( "choice_cell" )){
            const newstart=calendar.rows[0].cells[start_col-1].className.split(" ")[0];
            starttime.value = newstart+":00";
            id="s_timetext";
            new_value=newstart;
            select_tr.cells[start_col-1].classList.add("selecttime");
            startrow=start_col-1;
            endrow=end_col;
        }else if(form_kind=='start' && up_down=='down' && start_col!=end_col){
            const newstart=calendar.rows[0].cells[start_col+1].className.split(" ")[0];
            starttime.value = newstart+":00";
            id="s_timetext";
            new_value=newstart;
            select_tr.cells[start_col].classList.remove("selecttime");
            startrow=start_col+1;
            endrow=end_col;
        }else if(form_kind=='end' && up_down=='up' && end_col!=start_col){
            const newend=calendar.rows[0].cells[end_col].className.split(" ")[0];
            endtime.value = newend+":00";
            id="e_timetext";
            new_value=newend;
            select_tr.cells[end_col].classList.remove("selecttime");
            startrow=start_col;
            endrow=end_col-1;
        }else if(form_kind=='end' && up_down=='down'  
                && select_tr.cells[end_col+1].classList.contains( "choice_cell" )){
            let newend="00:00";
            if(select_tr.cells[end_col+2].classList.contains("choice_cell")){
                newend=calendar.rows[0].cells[end_col+2].className.split(" ")[0];            
                endtime.value = newend+":00";
            }else{newend=get_tailtime();}
            id="e_timetext";
            new_value=newend;
            select_tr.cells[end_col+1].classList.add("selecttime");
            startrow=start_col;
            endrow=end_col+1;
        }
        const time_p = document.getElementById(id);
        if(time_p!=null){
        const text=time_p.innerText.split(":");
        time_p.innerText=text[0] +":"+ new_value;
        }
        const swap_cal=document.getElementById("swapcalendar");
        if(swap_cal!=null){
            const swap_select=document.querySelectorAll("#swapcalendar .selecttime");
            const swap_column=swap_select[0].cellIndex;
            for(let step=0;step<swap_cal.rows.length;step++){
                if(startrow <=step && step <=endrow){
                    swap_cal.rows[step].cells[swap_column].classList.add("selecttime");
                }else{
                    swap_cal.rows[step].cells[swap_column].classList.remove("selecttime");
                }
            }
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