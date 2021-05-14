

function doReg() {
    var regname = $.trim($('#regname').val());
    var regpass = $.trim($('#regpass').val());

    if (!regname.match(/.+@.+\..+/) || regpass.length < 6) {
        bootbox.alert({ title: '错误提示', message: '注册邮箱不正确或密码少于6位' })
        return false;
    }
    else {
        // 构建POST请求的正文数据
        var param = 'username=' + regname;
        param += '&password=' + regpass;
        // 利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/user', param, function (data) {
            // if (data=='ecode-error'){
            //     bootbox.alert({title:'错误提示', message:'验证码无效'});
            //     $("#regcode").val('');  // 清除验证码框的值
            //     $("#regcode").focus();  // 让验证码框获取到焦点供用户输入
            // }
            if (data == 'up-invalid') {
                bootbox.alert({ title: '错误提示', message: '用户名和密码不能少于6位' });
            }
            else if (data == "user-repeated") {
                bootbox.alert({ title: '错误提示', message: '该用户已经被注册' });
                $("#regname").focus();
            }
            else if (data == "reg-pass") {
                bootbox.alert({ title: '错误提示', message: '恭喜你，注册成功' });
                setTimeout('location.reload();', 1000);
            }
            else if (data == "reg-fail") {
                bootbox.alert({ title: '错误提示', message: '注册失败，请联系管理员' });
            }
        });
    }
}

function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());

    if (loginname.length < 6 || loginpass.length < 6) {
        bootbox.alert({ title: '错误提示', message: '用户名或密码少于6位' })
        return false;
    }
    else {
        // 构建POST请求的正文数据
        var param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&vcode=" + logincode;
        // 利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/login', param, function (data) {
            if (data == "vcode-error") {
                bootbox.alert({ title: "错误提示", message: '验证码无效' });
                $("#logincode").val('');  // 清除验证码框的值
                $("#logincode").focus();  // 让验证码框获取到焦点供用户输入
            }
            else if (data == "login-pass") {
                location.href = '/index'
            }
            else if (data == "login-fail") {
                bootbox.alert({ title: "错误提示", message: '用户名或密码错误' });
            }
        });
    }
}