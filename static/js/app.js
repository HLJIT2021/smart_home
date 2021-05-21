// function project_add() {

//     var app_name = $.trim($('#app_name').val());

//     var param = "app_name=" + app_name;
//     $.post('/app_add', param, function (data) {
//         if (data == "add-pass") {
//             alert('新增项目成功');
//             location.href = '/index'
//         }
//         else {
//             alert("新增项目失败，请重新尝试");
//             return false;
//         }
//     });
// }


function del_project() {
    $.post('/del-project')
}