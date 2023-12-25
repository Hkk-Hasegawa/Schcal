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
function detail_hide(){
    const detail_list=document.querySelectorAll(".detail");
    for(let step=0;step<detail_list.length;step++){
        detail_list[step].style.display = "none";
    } 
}
function detail_show(tr){
    detail_hide()
    const row = tr.sectionRowIndex+1;
    const schedule_list = document.getElementById("schedule_list");
    const detail_tr=schedule_list.rows[row+1];
    detail_tr.cells[0].colSpan =String( tr.cells.length)
    detail_tr.style.display = "";
}

function place_filter(place_num){
    const schedule_list = document.getElementById("schedule_list");
    const list_tr=schedule_list.rows
    for(let step=1;step<list_tr.length;step++){
        if(list_tr[step].cells[place_num]==""){
            list_tr[step].classList.add("hide_elem");
        }else{
            list_tr[step].classList.remove("hide_elem");
        }
    }
}