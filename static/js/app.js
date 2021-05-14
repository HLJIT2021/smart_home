function app_add(){

    var app_name = $.trim($("#app_name").val());

    var param = "app_name=" + app_name;
    $.post('/app_add', param, function (data){
        if (data == "add-pass"){
            bootbox.alert({title:'错误提示',message:'新增项目成功'});
            setTimeout( 'location.reload();', 2000);
        }
        else {
            bootbox.alert({title:"错误提示", message:"新增项目失败，请重新尝试"});
            return false;
        }
    });

}