//年間スケジュール作成関数
function set_four_season(year_schedule,head_row,tail_row){
    const schedule_data=document.getElementById("schedule_data");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    const htr=document.createElement("tr");
    //ヘッダー作成
    for(let row=head_row;row<tail_row;row++){
        let th= document.createElement("th");
        th.textContent=schedule_data.rows[row].cells[0].textContent +"月";
        th.colSpan=schedule_data.rows[row].cells[0].rowSpan;
        th.className=schedule_data.rows[row].cells[0].className;
        htr.appendChild(th);
    }
    thead.appendChild(htr);
    year_schedule.appendChild(thead);
    //ボディ作成
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
    const fixed_detail= document.getElementById("fixed_detail");
    const detail= document.getElementById("detail");
    detail.innerText="";
    fixed_detail.classList.add("hide_elem");
}
function detail_show(tr){
    const fixed_detail= document.getElementById("fixed_detail");
    const title= document.getElementById("title");
    const detail= document.getElementById("detail");
    title.innerText=tr.cells[1].innerText + "\n" + tr.cells[2].innerText;
    detail.innerText=tr.cells[0].innerText;
    fixed_detail.classList.remove("hide_elem");
}
function schedule_filter(){
    const filter_select=document.getElementById("filter_select");
    const num = filter_select.selectedIndex;
    const value =filter_select[num].value;
    const schedule=document.querySelectorAll(".schedule");
    if(value=="本社"){
        for(let step=0;step<schedule.length;step++){
            if(schedule[step].cells[3].innerText==""){
                schedule[step].classList.add("hide_elem");
            }else{
                schedule[step].classList.remove("hide_elem");
            }
        }
    }else if(value=="岡崎"){
        for(let step=0;step<schedule.length;step++){
            if(schedule[step].cells[4].innerText==""){
                schedule[step].classList.add("hide_elem");
            }else{
                schedule[step].classList.remove("hide_elem");
            }
        }
    }else{
        for(let step=0;step<schedule.length;step++){
            schedule[step].classList.remove("hide_elem");
        }
    } 
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