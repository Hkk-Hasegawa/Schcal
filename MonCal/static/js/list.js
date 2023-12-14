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