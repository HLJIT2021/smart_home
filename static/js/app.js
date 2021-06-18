function project_app(){
    location.href="/project/{{session.get('app_id')}}"
}


function show(){
    alert('helloword')
}

function add_app() {
    var s_name=$.trim($("#s_name").val());
    var sno=$.trim($("#sno").val());
    var port=$.trim($("#port").val());
    var tid=$("#tid option:selected").val();
    
    var param = 's_name=' + s_name;
    param += '&sno=' + sno;
    param += '&port=' + port;
    param += '&tid=' + tid;
    $.post('/app_add', param, function(data){
        if (data == 'add-pass'){
            alert('新增成功，返回设备列表')
            location.href='/project/'
            setTimeout(10)
        }
        else if (data == 'add-fail'){
            alert('该端口已使用，请更换端口');
            $("#port").val(''); 
        }
        else{
            alert('添加失败')
        }
    })
}

function add_control(){
    var s_name=$.trim($("#s_name").val());
    var sno=$.trim($("#sno").val());
    var port=$.trim($("#port").val());
    var ssid=$("#ssid option:selected").val();

    var param = 's_name=' + s_name;
    param += '&sno=' + sno;
    param += '&ssid=' + ssid;
    param += '&port=' + port;
    $.post('/add_control', param, function (data){
        if (data=='add-pass'){
            alert('成功添加控制器与控制逻辑');
            setTimeout(location.href='/index',10)
        }
        else {
            alert('添加失败');
        }
    })
}

function del_project() {
    $.post('/del-project', function(data){
        if (data=='del-pass'){
            alert('成功删除')
            setTimeout(location.href='/index',10)
        }
        else {
            alert('删除失败')
        }
    })
}

function modify(){
    var high = $.trim($('#high').val())
    var low=$.trim($("#low").val());

    var param = 'high=' + high
    param += '&low=' + low
    $.post('/threshold', param, function (data){
        if (data=='modify-pass'){
            alert('修改成功');
            location.reload()
        }
        else {
            alert('修改失败');
        }
    })
}

function control_switch(){
    var obj = $("#switch").text().trim();
    if(obj == "开启") {
        $("#switch").text("关闭");
    }
    else {
        $("#switch").text("开启");
    }

    $.post('/control-switch',function (data){
        if(data=='open'){
            alert('设备已开启')
        }
        else if (data=='close'){
            alert('设备已关闭')
        }
        else{
            alert('状态切换失败')
        }
    })
}

function change(){
    var obj = $("#op").text().trim();
    if(obj == "开启") {
        $("#op").text("关闭");
    }
    else {
        $("#op").text("开启");
    }

    $.post('/control-automatic',function (data){
        if(data=='open'){
            alert('已开启自动控制')
        }
        else if (data=='close'){
            alert('已关闭自动控制')
        }
        else{
            alert('修改失败')
        }
    })
}

function del_app(){
    var sid=$("#sid option:selected").val();

    var param = 'sid=' + sid
    $.post('/del-app', param,function (data){
        if(data=='del-pass'){
            alert('设备已删除')
            setTimeout(location.href='/index')
        }
        else {
            alert('删除失败')
        }
    })
}

function newinfo(){
    var nickname=$.tr($('#nickname').val());
    var email=$.trim($("#email").val());
    var phone=$.trim($("#phone").val());

    var param = 'nickname=' + nickname;
    param += '&email=' + email;
    param += '&phone=' + phone;

    $.post('/new-info', param, function (data){
        if (data=='false'){
            alert('原信息与修改后信息一致，请重新输入');
            location.reload();
        }
        else if (data=='modify-pass'){
            alert('修改成功，返回主页')
            location.href='/index'
        }
    })
}