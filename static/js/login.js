

function doReg(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var regname = $.trim($('#regname').val());
    var regpass = $.trim($('#regpass').val());
    var regcode = $.trim($("#regcode").val());

    if (!regname.match(/.+@.+\..+/) || regpass.length < 6) {
        bootbox.alert({ title: '错误提示', message: '注册邮箱不正确或密码少于6位' })
        return false;
    }
    else {
        // 构建POST请求的正文数据
        var param = 'username=' + regname;
        param += '&password=' + regpass;
        param += '&ecode=' + regcode;
        // 利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/user', param, function (data) {
            if (data == 'up-invalid') {
                alert('用户名和密码不能少于6位');
            }
            else if (data == "ecode-error") {
                alert('验证码无效');
                $("#regcode").val('');  // 清除验证码框的值
                $("#regcode").focus();  // 让验证码框获取到焦点供用户输入
            }
            else if (data == "user-repeated") {
                alert('该用户已经被注册');
                $("#regname").focus();
            }
            else if (data == "reg-pass") {
                alert('恭喜你，注册成功');
                setTimeout(location.href = '/index', 1000);
            }
            else{
                alert('注册失败，请联系管理员');
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
                alert('验证码无效');
                $("#logincode").val('');  // 清除验证码框的值
                $("#logincode").focus();  // 让验证码框获取到焦点供用户输入
            }
            else if (data == "login-pass") {
                alert('登录成功');
                setTimeout(location.href = '/index',10);
            }
            else if (data == "login-fail") {
                alert('用户名或密码错误');
            }
        });
    }
}