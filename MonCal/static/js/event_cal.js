//日時入力中か判定
function ev_mouse_over(td){
    if(document.getElementById("down_td") != null)
    {ev_fill_time(td)}
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
