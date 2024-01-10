//場所を選択したときの部屋の選択肢の表示
function room_view(palce){
    const place_pk='place_room_'+palce.value
    const room_ul=document.getElementById(place_pk);
    if (palce.checked == true){
        room_ul.style.display = '';
    }else{
        room_ul.style.display = 'none';
        const roomlist=document.querySelectorAll("."+place_pk);
        for(let i=0;i<roomlist.length;i++){
            roomlist[i].checked=false;
        }
    }
}


