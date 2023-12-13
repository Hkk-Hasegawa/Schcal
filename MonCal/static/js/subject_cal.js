//日時をフォームに入力する開始の関数
function all_sub_mousedown(td,subject){
    const id_subject = document.getElementById('id_subject');
    let options = id_subject.options;
    for(let step=0;step<options.length;step++){
        if(options[step].innerText==subject){options[step].selected = true;}
    }
    mousedown(td)
}

function get_subject(tr){
    subject= tr.cells[1].innerText;
    return subject
}

function sub_mouseover(td){
    if(document.getElementById("down_td") != null)
    {sub_fill_time(td)}
}
function sub_fill_time(td){
    const down_cell = document.getElementById("down_td");
    const down_time=down_cell.className.split(" ")[0];
    const td_time=td.className.split(" ")[0];    
    const td_timecol=get_times_column(td_time);
    const down_timecol=get_times_column(down_time);
    
    input_timedelta(td_time,down_cell,down_timecol<td_timecol);
}

function get_times_column(time){
    const hide_times_tr = document.getElementById("hide_times_tr");
    for(let step =0;step<hide_times_tr.cells.length;step++){
        if(hide_times_tr.cells[step].classList.contains(time)){
            var result_col=step;
            break;
        }
    }
    return result_col
}

function input_timedelta(td_time,down_cell,direction){
    const Mycalendar = document.getElementById("calendar");
    const down_column = down_cell.cellIndex;
	const down_tr = down_cell.parentNode;
	const down_row = down_tr.sectionRowIndex;
    const cal_tail   = down_tr.cells.length;
    remove_swich=false;
    if(direction){
        for(let step =0;step<cal_tail;step++){
            var step_cell=down_tr.cells[step];
            
            if(step<down_column || remove_swich){step_cell.classList.remove("selecttime")}
            else if(step_cell.classList.contains( "sche_box" )){
                endtime=get_starttime(step_cell);//endtime=get_starttimeであってる
                step_cell.classList.remove("selecttime")
                remove_swich=true;
            }else{
                step_cell.classList.add("selecttime");
                if(step_cell.classList.contains( td_time )){
                    endtime=get_endtime(step_cell);
                    remove_swich=true;
                }
            }
        }
        starttime= get_starttime(down_cell);
        input_time(starttime,endtime);
    }else{
        for(let step =cal_tail-1;step>0;step--){
            var step_cell=Mycalendar.rows[down_row+1].cells[step];
            if(step>down_column || remove_swich){step_cell.classList.remove("selecttime")}
            else if(step_cell.classList.contains( "sche_box" )){
                var step_cell=Mycalendar.rows[down_row+1].cells[step+1];
                starttime=get_starttime(step_cell);
                remove_swich=true;
            }else{
                step_cell.classList.add("selecttime");
                if(step_cell.classList.contains( td_time )){
                    starttime=get_starttime(step_cell);
                    remove_swich=true;
                }
                
            }
        }
        endtime=get_endtime(down_cell);
        input_time(starttime,endtime);
    }
    
}



