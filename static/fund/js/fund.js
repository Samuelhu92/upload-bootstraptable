
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    function upload() {
        var fs = document.getElementById("file").files;
        var fsarray = $("#filelist").data("data");
        if (fsarray){
            $.each(fs,function(i,v) {
                for (var k in fsarray) {
                    if (v.name===fsarray[k].name){
                        return true;
                    }
                }
                fsarray.push(v);
                $("#filediv").append("<tr><td class='xdiv'>" + v.name + "</td><td><button type='button' class='btn btn-default' id='"+v.name+"' onclick='delexcel(this);'><span class='glyphicon glyphicon-remove'></span></button></td></tr>");
                document.getElementById("submit").disabled=false;
                document.getElementById("file").value="";
                }
            )
        }
        else{
            fsarray = new Array;
            $.each(fs, function(i,v){
                    fsarray.push(v);
                    $("#filediv").append("<tr><td class='xdiv'>"+v.name+ "</td><td><button type='button' class='btn btn-default' id='"+v.name+"' onclick='delexcel(this);'><span class='glyphicon glyphicon-remove'></span></button></td></tr>");
                    document.getElementById("submit").disabled=false;
                }
            );
            $("#filelist").data("data",fsarray);
            document.getElementById("file").value="";
        }
        $("#scts").css("color","green").text("已选择"+fsarray.length+"个文件");

    }

    function delexcel(obj){
        var ar = $("#filelist").data("data");
        for (var v in ar){
            if (ar[v].name===obj.id){
                ar.splice(v,1);
            }
        }
        $(obj).parent().parent().remove();
        $("#scts").css("color", ar.length === 0 ? "red" : "green").text("已选择" + ar.length + "个文件");
        if (ar.length===0){
            document.getElementById("submit").disabled=true;
        }
    }


    function sub() {

        var fd = new FormData();
        if ($("#file").outerHTML) {
            $("#file").outerHTML = $("#file").outerHTML;
        } else {
            $("#file").value = "";
        }
        for (var i = 0;i<$("#filelist").data("data").length;i++ ){
            fd.append("file",$("#filelist").data("data")[i]);
        }
        $.ajax({
            url: "/fund/process/",
            type: "post",
            data: fd,
            processData: false,
            contentType: false,
            success: function (ret) {
                $("#uploadfield").css("display","none");
                $("#ret").css("display","inherit");
                $("#ret").html(ret);
            },
            error: function(){
                alert("false");
            }
        });
    }
