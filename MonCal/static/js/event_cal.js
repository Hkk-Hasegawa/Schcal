//年間スケジュール作成関数
function set_four_season(year_schedule,head_row,tail_row){
    const schedule_data=document.getElementById("schedule_data");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    const htr=document.createElement("tr");
    for(let row=head_row;row<tail_row;row++){
        let th= document.createElement("th");
        th.textContent=schedule_data.rows[row].cells[0].textContent +"月";
        th.colSpan=schedule_data.rows[row].cells[0].rowSpan;
        th.className=schedule_data.rows[row].cells[0].className;
        htr.appendChild(th);
    }
    thead.appendChild(htr);
    year_schedule.appendChild(thead);
    const maxrow = maxcal(schedule_data,head_row,tail_row);

    for(let row=1;row<maxrow;row++){
        tbody.appendChild(new_sche_tr(head_row,tail_row));
    }
    year_schedule.appendChild(tbody);
    let sche_col=-1;
    for(let row =head_row;row<tail_row;row++){
        sche_col=sche_col+1;
        let sche_row=0;
        for(let column=1;column<schedule_data.rows[row].cells.length;column++){
            sche_row=sche_row+1;
            year_schedule.rows[sche_row].cells[sche_col].innerHTML=schedule_data.rows[row].cells[column].innerHTML;
            
        }
    }
}
//テーブルの最大列数取得
function maxcal(table,head,tail){
    let maxcal=0;
    for(let row=head;row<tail;row++){
        if(maxcal<table.rows[row].cells.length){
            maxcal=table.rows[row].cells.length;
        }
    }
    return maxcal
}
//tail-head個のtdを持つtrを作成
function new_sche_tr(head,tail){
    const tr=document.createElement("tr");
    for(let step=head;step<tail;step++){
        let td=document.createElement("td");
        tr.appendChild(td);
    }
    return tr
}
function room_view(palce){
    const place_pk='place_room_'+palce.value
    const room_ul=document.getElementById(place_pk);
    if (palce.checked == true) {
        room_ul.style.display = '';
      } else {
        room_ul.style.display = 'none';
        const roomlist=document.querySelectorAll("."+place_pk);
        for(let i=0;i<roomlist.length;i++){
            roomlist[i].checked=false;
        }
      }
}
//日時をフォームに入力する途中の関数
function ev_fill_time(td){
    const down_cell = document.getElementById("down_td");
	const down_tr = down_cell.parentNode;
    const cal_tail   = down_tr.cells.length;
    const down_time=down_cell.className.split(" ")[0]
    const td_time=td.className.split(" ")[0]
    //down_timeとtd_timeはe_timeではない
    let selectF=false;
    let s_time="00:00";
    let e_time="00:00";
    if(comparison_time(down_time,td_time)){
        s_time=down_time;
        e_time=get_endtime(td);
        for(let step =1;step<cal_tail;step++){
            let checktd=down_tr.cells[step];
            selectF=select_cells(checktd,selectF,s_time,e_time);
        }
    }else{
        s_time=td_time;
        e_time=get_endtime(down_cell);
        for(let step =1;step<cal_tail;step++){
            let checktd=down_tr.cells[step];
            selectF=select_cells(checktd,selectF,s_time,e_time);
        }
    }
    input_time(s_time,e_time);
}
//selectFを更新してセル選択を行う
function select_cells(checktd,selectF,start,end){
    if(checktd.classList.contains(start)){selectF=true;}
    if(checktd.classList.contains(end)){selectF=false;}
    if(selectF){checktd.classList.add("selecttime")}
    else{checktd.classList.remove("selecttime")}
    return selectF
}
//時刻を比較する
function comparison_time(down_time,td_time){
    const down_hour=Number(down_time.split(":")[0]);
    const down_min=Number(down_time.split(":")[1]);
    const td_hour=Number(td_time.split(":")[0]);
    const td_min=Number(td_time.split(":")[1]);
    let result=true;
    if(down_hour<td_hour){result=true}
    else if(down_hour>td_hour){result=false}
    else{if(down_min<=td_min){result=true}
        else{result=false}}
    return result
}
