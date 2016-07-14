/**
 * Created by zhangfangyan on 14-9-23.
 */
function six_random_num(){
    var a="";
    for(var i=0; i<6 ; i++){
        a += String(Math.floor(Math.random()*10));
    };
    return a;
};

//格式化输出时间
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

jQuery.fn.shake = function(intShakes, intDistance, intDuration) {
    this.each(function() {
        $(this).css("position","relative"); 
        for (var x=1; x<=intShakes; x++) {
        $(this).animate({left:(intDistance*-1)}, (((intDuration/intShakes)/4)))
    .animate({left:intDistance}, ((intDuration/intShakes)/2))
    .animate({left:0}, (((intDuration/intShakes)/4)));
    }
  });
return this;
};

//get the original data from api
function get_original_data(url, async, condition, render){
    var content = [];
    if (condition != null){
        $.ajax({
            url: url,
            type:'POST',
            dataType:'json',
            data:condition,
            async:async,
            success:function(d){
                if('status' in d ){
                    if (d['status'] == 0 && 'content' in d) {
                        content = d['content'];
                    }

                    (typeof render != 'undefined')? render(d) : null;
                }
            }
        });
    }else{
        $.ajax({
            url: url,
            type:'POST',
            dataType:'json',
            async:async,
            success:function(d){
                if('status' in d){
                    if (d['status'] == 0 && 'content' in d) {
                        content = d['content'];
                    }
                    (typeof render != 'undefined')? render() : null;
                }
            }
        });
    }
    return content;
}


//create the option of select
function make_option(id, url, label, value, async, render)
{
    var data = [];
    $.ajax({
        url: url,
        type:'POST',
        dataType:'json',
        async:async,
        success:function(d){
            if('status' in d || 'content' in d){
                if (d['status'] == 0) {
                    var content = d['content'];
                    if (label.indexOf(",") > 0){
                        var label_list = label.split(",");
                        for (var i = 0; i < content.length; i++ ){
                            var label_final = "";
                            for (var l = 0; l < label_list.length; l++){
                                if (l in content[i]){
                                    label_final = label_final + content[i][l] + " ";
                                }
                            }
                            if (value in content[i]){
                                var value_final = content[i][value];
                            }
                            var option = $('<option value='+value_final+'>').append(label_final)
                            data.push(option);
                        }
                    }
                    else{
                        for (var i = 0; i < content.length; i++ ){
                            if (label in content[i]){
                                var label_final = content[i][label];
                            }
                            if (value in content[i]){
                                var value_final = content[i][value];
                            }
                            var option = $('<option value='+value_final+'>').append(label_final)
                            data.push(option);
                        }
                    }
                }
            }
        $("#"+id).html(data);
        (typeof render != 'undefined')? render(d) : null;
        }
    });
}


//create the two grade interaction,you can set up render after ajax.
function two_grade_interaction(condition, id, url, label, value, async, render){
    var data = [];
    $.ajax({
        url: url,
        type:'POST',
        dataType:'json',
        data:condition,
        async:async,
        success:function(d){
            var option = "";
            if('status' in d || 'content' in d){
                if (d['status'] == 0) {
                    var content = d['content'];
                    if (label.indexOf(",") > 0){
                        var label_list = label.split(",");
                        for (var i = 0; i < content.length; i++ ){
                            var label_final = "";
                            for (var l = 0; l < label_list.length; l++){
                                if (l in content[i]){
                                    label_final = label_final + content[i][l] + " ";
                                }
                            }
                            if (value in content[i]){
                                var value_final = content[i][value];
                            }
                            var option = $('<option value='+value_final+'>').append(label_final)
                            data.push(option);
                        }
                    }
                    else{
                        for (var i = 0; i < content.length; i++ ){
                            if (label in content[i]){
                                var label_final = content[i][label];
                            }
                            if (value in content[i]){
                                var value_final = content[i][value];
                            }
                            option += '<option value="'+value_final+'">'+label_final+'</option>';
                        }
                    }
                }
            }
            $("#"+id).html(option);
            (typeof render != 'undefined')? render(d) : null;
        }
    });
}