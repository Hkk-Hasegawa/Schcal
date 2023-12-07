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
    var text=time_p.innerText.split(":");
    time_p.innerHTML=text[0] +":"+ time;
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
function get_tailtime(){
    const tailtime= document.getElementById("tailtime").innerText.split('\n')[1];
    return tailtime
}