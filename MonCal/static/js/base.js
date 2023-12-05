        function date_Normalization(date){
            const datearr=date.replace(/(年|月)/g, '-').replace('日', '').split('-');
            for(let step=1;step<datearr.length;step++){
                if(datearr[step].length==1){datearr[step]='0'+ datearr[step];}
                datearr[0]=datearr[0]+'-' + datearr[step];
            }
            return datearr[0]
        }
        function time_Normalization(time){
            var timearr=time.split(':');
            if(timearr.length<3){timearr=(time+':00').split(':')}
            if(timearr[0].length==1){timearr[0]='0'+ timearr[0];}
            for(let step=1;step<timearr.length;step++){
                if(timearr[step].length==1){timearr[step]='0'+ timearr[step];}
                timearr[0]=timearr[0]+':' + timearr[step];
            }
            return timearr[0]
        }

        function select_patterns(td,nextclass,beforeclass,s_time,e_time){
            const starttime  = document.getElementById("id_starttime");
            const endtime    = document.getElementById("id_endtime");
            var selectcells=document.getElementsByClassName("selecttime");
            if (selectcells.length==0){
                console.log("条件1");
                starttime.value = s_time;
                endtime.value = e_time;
                outputtext("s_timetext",s_time);
                outputtext("e_timetext",e_time);
                td.classList.add("selecttime");
            }else if(selectcells.length==1 && td.classList.contains("selecttime")){
                console.log("条件2");
                starttime.value = "0";
                endtime.value = "0";
                outputtext("s_timetext","0");
                outputtext("e_timetext","0");
                td.classList.remove("selecttime");
            }else if(nextclass && !(beforeclass) ){
                console.log("条件3");
                if(td.classList.contains("selecttime")){
                    starttime.value = e_time;
                    outputtext("s_timetext",e_time);
                    td.classList.remove("selecttime");
                }else{
                    starttime.value = s_time;
                    outputtext("s_timetext",s_time);
                    td.classList.add("selecttime");
                }
            }else if(!(nextclass) && beforeclass){
                console.log("条件4");
                if(td.classList.contains("selecttime")){
                    endtime.value = s_time;
                    outputtext("e_timetext",s_time);
                    td.classList.remove("selecttime");
                }else{
                    endtime.value = e_time;
                    outputtext("e_timetext",e_time);
                    td.classList.add("selecttime");
                }
            }else{
                console.log("条件6");
                reset_timeform()
                starttime.value = s_time;
                endtime.value = e_time;
                outputtext("s_timetext",s_time);
                outputtext("e_timetext",e_time);
                td.classList.add("selecttime");
            }
        }


        
        function indate(dateV){
            let newdateV = date_Normalization(dateV);
            let Myelement = document.getElementById("id_date");
            Myelement.value = newdateV;
        }
        function intime(td,date,time,tailtime){
            const column = td.cellIndex;
	        const tr = td.parentNode;
	        const row = tr.sectionRowIndex+1;
            const Mycalender = document.getElementById("calender");
            const row_tail   = Mycalender.rows.length;
            indate(date);
            var s_time       = time;
            s_time=time_Normalization(s_time);
            if (row_tail == row+1){
                var e_time=time_Normalization(tailtime);
                var underclass =false;
            }else{
                var e_time=time_Normalization(Mycalender.rows[row+1].cells[0].innerText);
                var undercell =Mycalender.rows[row+1].cells[column];
                var underclass= undercell.classList.contains("selecttime");
            }
            var overclass=Mycalender.rows[row-1].cells[column].classList.contains("selecttime");
            console.log("underclass:"+underclass);
            console.log("overclass:"+overclass);
            if(underclass && overclass){
                console.log("条件5");
                for(let step=row;step < row_tail;step++){
                    Mycalender.rows[step].cells[column].classList.remove("selecttime");
                }
                const endtime = document.getElementById("id_endtime");
                endtime.value = e_time;
                outputtext("e_timetext",e_time);
                td.classList.add("selecttime");
            }else{select_patterns(td,underclass,overclass,s_time,e_time)}
        }
        function pr_timematch(calender,time){
            var setrow=0;
            for(let step=2;step<calender.rows.length;step++){
                var cal_value=calender.rows[step].cells[0].innerText;
                cal_value=time_Normalization(cal_value);               
                if(cal_value==time){setrow=step;}
            }   
            if(setrow==0){setrow=calender.rows.length-1}
            return setrow;
        }
        function pr_set_selecttime(day,start,end){
            const date=date_Normalization(day);
            const starttime=time_Normalization(start)
            const endtime=time_Normalization(end)
            const calender=document.getElementById("calender");
            const form_date_Value=date.substr(8,2);
            outputtext("s_timetext",starttime);
            outputtext("e_timetext",endtime);
            if(monthcheck(date,calender)){
                var set_startrow=pr_timematch(calender,starttime);
                var set_endrow=pr_timematch(calender,endtime)-1;
                var setcol =0;
                for(let step=0;step<calender.tHead.rows[0].cells.length;step++){
                    var date_th=calender.tHead.rows[0].cells[step];
                    var th_Value=date_th.innerText;
                    if(th_Value.indexOf("稼働",0)){
                        th_Value=th_Value.substr(0,2);
                    }else{
                        th_Value=th_Value.split("\n");
                        th_Value=th_Value[1].substr(0,2);
                        }
                    if(form_date_Value==th_Value){setcol=step;}
                }
                if (!(setcol==0)){
                    for(let step=set_startrow;step<=set_endrow;step++){
                        calender.rows[step].cells[setcol].classList.add("selecttime");
                    }
                }
            }
        }
        
