// login.html js设置
$(document).ready(function(){
    // 设置提交表单和题目与顶部的距离
    $('.healthms-login-container').css({"padding-top": ($(window).height()-163) * 0.15});
    $(window).resize(function() {
      $('.healthms-login-container').css({"padding-top": ($(window).height()-163) * 0.15});
    });
    $('.healthms-container-height').css({"min-height":$(window).height()-163});
    $(window).resize(function() {
      $('.healthms-container-height').css({"min-height":$(window).height()-163});
    });
    $('.healthms-container-height>row,.healthms-index-main').css({"min-height":$(window).height()-203});
    $(window).resize(function() {
      $('.healthms-container-height>row,.healthms-index-main').css({"min-height":$(window).height()-203});
    });
    

    // 用户 Email input 失去焦点时验证其是否为空 和 Email格式 是否正确
    $('#patientEmail').blur(function(){
        if ($('#patientEmail').val() == '') { 
            loginInputError('patientEmail', 'healthms-login-error-patient-email', true);
        } else if (!checkEmail($('#patientEmail').val())) {
            loginInputError('patientEmail', 'healthms-login-error-patient-email', true);
        } else {
            loginInputError('patientEmail', 'healthms-login-error-patient-email', false);
        }
    });
    // 用户 密码 input 失去焦点时验证其是否为空
    $('#patientPassword').blur(function(){
        if ($('#patientPassword').val() == '') {
            loginInputError('patientPassword', 'healthms-login-error-patient-password', true);
        } else {
            loginInputError('patientPassword', 'healthms-login-error-patient-password', false);
        }
    });
    // 医生 Email input 失去焦点时验证其是否为空 和 Email格式 是否正确
    $('#doctorEmail').blur(function(){
        if ($('#doctorEmail').val() == '') {
            loginInputError('doctorEmail', 'healthms-login-error-doctor-email', true);
        } else if (!checkEmail($('#doctorEmail').val())) {
            loginInputError('doctorEmail', 'healthms-login-error-doctor-email', true);
        } else {
            loginInputError('doctorEmail', 'healthms-login-error-doctor-email', false);
        }
    });
    // 医生 密码 input 失去焦点时验证其是否为空
    $('#doctorPassword').blur(function(){
        if ($('#doctorPassword').val() == '') {
            loginInputError('doctorPassword', 'healthms-login-error-doctor-password', true);
        } else {
            loginInputError('doctorPassword', 'healthms-login-error-doctor-password', false);
        }
    });
});

// 以 Ajax 方式提交登录信息
function ajaxLoginForm(typ){
    $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT,
        dataType: 'json',
        data: {
            'type': typ,
            'patientEmail': $('#patientEmail').val(),
            'patientPassword': $('#patientPassword').val(),
            'doctorEmail': $('#doctorEmail').val(),
            'doctorPassword': $('#doctorPassword').val()
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            if (data.typ == 'patient') {
                if (data.result == 'emailError') {
                    $('#patientEmail').focus();
                    loginInputError('patientEmail', 'healthms-login-error-patient-email', true);
                } else if (data.result == 'pwdError') {
                    $('#patientPassword').focus();
                    loginInputError('patientPassword', 'healthms-login-error-patient-password', true);
                } else if (data.result == 'success') {
                    window.location.href = "/index"
                }
            } else if (data.typ == 'doctor') {
                if (data.result == 'emailError') {
                    $('#doctorEmail').focus();
                    loginInputError('doctorEmail', 'healthms-login-error-doctor-email', true);
                } else if (data.result == 'pwdError') {
                    $('#doctorPassword').focus();
                    loginInputError('doctorPassword', 'healthms-login-error-doctor-password', true);
                }  
                else if (data.result == 'success') {
                    window.location.href = "/"
                }
            } 
        }
    });
    return false
}

// 表单验证时修改 DOM
function loginInputError(id, cla, error) {
    if (error) { 
        $('#' + id).parent().addClass('has-error has-feedback');
        $('#' + id).after('<span class="' + cla + ' glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span id="inputError2Status" class="' + cla + ' sr-only">(error)</span>');
    } else {
        $('#' + id).parent().removeClass('has-error has-feedback');
        $('.' + cla).remove();
    }
}

// patient_register js 设置
$(document).ready(function(){
    // 从 json 数组中 动态添加民族
    var patientNationSelect = $('#patientRegNation');
    patientNationSelect.append('<option value="">请选择</option>');
    for(var i= 0; i < nationItems.length; i++) {
        var nation = nationItems[i];
        var name = nation.name;
        patientNationSelect.append('<option value="' + name + '">' + name + '</option>');
    };

    // 设置点击出生日期时 弹出 datetimepicker
    $('#patientRegBirthday').datetimepicker({
        lang:'ch',
        timepicker:false,
        format:'Y-m-d'
    });

    // 验证表单
    var flag = true;

    $('#regEmail').blur(function(){
        var result = 'true';
        var userTyp = getUserTyp();
        if ($('#regEmail').val() == '') { 
            result = '电子邮箱不能为空';
        } else if (userTyp == 'patient') {
            if (checkEmailExist($('#regEmail').val(), 'patient')) {
                result = '电子邮箱已经存在';
            };
        } else if (userTyp == 'doctor') {
            if (checkEmailExist($('#regEmail').val(), 'doctor')) {
                result = '电子邮箱已经存在';
            };
        };
        if (result != 'true') {
            flag = false;
            regInputError('regEmail', 'healthms-reg-email-err', result, true);
        } else {
            flag = true;
            regInputError('regEmail', 'healthms-reg-email-err', '', false);
        };
    });

    $('#patientRegEmail').keyup(function(){
        if (!checkEmail($('#patientRegEmail').val())) {
            flag = false;
            regInputError('patientRegEmail', 'healthms-patient-reg-email-err', '电子邮箱格式不正确', true);
        } else {
            flag = true;
            regInputError('patientRegEmail', 'healthms-patient-reg-email-err', '', false);
        };
    });



    $('#patientRegPassword').blur(function(){
        if ($('#patientRegPassword').val() == '') { 
            flag = false;
            regInputError('patientRegPassword', 'healthms-patient-reg-pwd-err', '密码不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegPassword', 'healthms-patient-reg-pwd-err', '', false);
        };
    });

    $('#patientRegPassword').keyup(function(){
        if (!checkPwdLength($('#patientRegPassword').val())) {
            flag = false;
            regInputError('patientRegPassword', 'healthms-patient-reg-pwd-err', '密码长度为6-20位字符', true);
        } else {
            flag = true;
            regInputError('patientRegPassword', 'healthms-patient-reg-pwd-err', '', false);
        };
    })

    $('#patientRegPasswordCon').blur(function(){
        if ($('#patientRegPasswordCon').val() == '') { 
            flag = false;
            regInputError('patientRegPasswordCon', 'healthms-patient-reg-pwdcon-err', '密码不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegPasswordCon', 'healthms-patient-reg-pwdcon-err', '', false);
        };
    });
    $('#patientRegPasswordCon').keyup(function(){
        if (!checkPwdEqual($('#patientRegPassword').val(), $('#patientRegPasswordCon').val())) {
            flag = false;
            regInputError('patientRegPasswordCon', 'healthms-patient-reg-pwdcon-err', '两次输入密码不一致', true);
        } else {
            flag = true;
            regInputError('patientRegPasswordCon', 'healthms-patient-reg-pwdcon-err', '', false);
        };
    })

    $('#patientRegName').blur(function(){
        if ($('#patientRegName').val() == '') {
            flag = false;
            regInputError('patientRegName', 'healthms-patient-reg-name-err', '姓名不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegName', 'healthms-patient-reg-name-err', '', false);
        };
    });
    $('#patientRegBirthday').blur(function(){
        if ($('#patientRegBirthday').val() == '') {
            flag = false;
            regInputError('patientRegBirthday', 'healthms-patient-reg-birthday-err', '出生日期不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegBirthday', 'healthms-patient-reg-birthday-err', '', false);
        };
    });
    $('#patientRegNation').blur(function(){
        if ($('#patientRegNation').val() == '') {
            flag = false;
            regNoInputError('patientRegNation', '民族不能为空', true);
        } else {
            flag = true;
            regNoInputError('patientRegNation', '', false);
        };
    });
    $('#patientRegProvince').blur(function(){
        if ($('#patientRegCounty').hasClass('hidden')) {
            if (($('#patientRegProvince').val() == '') || ($('#patientRegCity').val() == '') || ($('#patientRegCity').val() == '请选择')) {
                flag = false;
                regNoInputError('patientRegProvince', '籍贯不能为空', true);
            } else {
                flag = true;
                regNoInputError('patientRegProvince', '', false);
            };
        } else {
            if (($('#patientRegProvince').val() == '') || ($('#patientRegCity').val() == '') || ($('#patientRegCity').val() == '请选择') || ($('#patientRegCounty').val() == '') || ($('#patientRegCounty').val() == '请选择')) {
                flag = false;
                regNoInputError('patientRegProvince', '籍贯不能为空', true);
            } else {
                flag = true;
                regNoInputError('patientRegProvince', '', false);
            };
        };
    });
    $('#patientRegCity').blur(function(){
        if ($('#patientRegCounty').hasClass('hidden')) {
            if ($('#patientRegCity').val() == '' || $('#patientRegCity').val() == '请选择') {
                flag = false;
                regNoInputError('patientRegProvince', '籍贯不能为空', true);
            } else {
                flag = true;
                regNoInputError('patientRegProvince', '', false);
            };
        } else {
            if (($('#patientRegCity').val() == '') || ($('#patientRegCity').val() == '请选择') || ($('#patientRegCounty').val() == '') || ($('#patientRegCounty').val() == '请选择')) {
                flag = false;
                regNoInputError('patientRegProvince', '籍贯不能为空', true);
            } else {
                flag = true;
                regNoInputError('patientRegProvince', '', false);
            };
        };
    });
    $('#patientRegCounty').blur(function(){
        if ($('#patientRegCounty').val() == '' || $('#patientRegCounty').val() == '请选择') {
            flag = false;
            regNoInputError('patientRegProvince', '籍贯不能为空', true);
        } else {
            flag = true;
            regNoInputError('patientRegProvince', '', false);
        };
    });
    $('#patientRegProfession').blur(function(){
        if ($('#patientRegProfession').val() == '') {
            flag = false;
            regInputError('patientRegProfession', 'healthms-patient-reg-profession-err', '职业不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegProfession', 'healthms-patient-reg-profession-err', '', false);
        };
    });
    $('#patientRegAddress').blur(function(){
        if ($('#patientRegAddress').val() == '') {
            flag = false;
            regInputError('patientRegAddress', 'healthms-patient-reg-address-err', '住址/单位不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegAddress', 'healthms-patient-reg-address-err', '', false);
        };
    });
    $('#patientRegTel').blur(function(){
        if ($('#patientRegTel').val() == '') { 
            flag = false;
            regInputError('patientRegTel', 'healthms-patient-reg-tel-err', '电话不能为空', true);
        } else {
            flag = true;
            regInputError('patientRegTel', 'healthms-patient-reg-tel-err', '', false);
        };
    });
    $('#patientRegTel').blur(function(){
        if (!checkTel($('#patientRegTel').val())) {
            flag = false;
            regInputError('patientRegTel', 'healthms-patient-reg-tel-err', '电话格式不正确', true);
        } else {
            flag = true;
            regInputError('patientRegTel', 'healthms-patient-reg-tel-err', '', false);
        };
    })
    $('#patientRegCode').blur(function(){
        var result = 'true';
        if ($('#patientRegCode').val() == '') { 
            result = '验证码不能为空';
        } else if (!checkCode()) {
            result = '验证码不正确';
        }
        if (result != 'true') {
            flag = false;
            $("#patientRegCode").parent().parent().parent().removeClass('has-success has-feedback');
            $("#patientRegCode").parent().parent().parent().addClass('has-error has-feedback');
            $(".healthms-patient-reg-code-err").remove();
            $("#patientRegCode").parent().after('<span class="healthms-patient-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-patient-reg-code-err sr-only">(error)</span>');
            $("#patientRegCodeEMsg").html(result);
                } else {
            flag = true;
            $("#patientRegCode").parent().parent().parent().removeClass('has-error has-feedback');
            $("#patientRegCode").parent().parent().parent().addClass('has-success has-feedback');
            $(".healthms-patient-reg-code-err").remove();
            $("#patientRegCode").parent().after('<span class="healthms-patient-reg-code-err glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span><span class="healthms-patient-reg-code-err sr-only">(success)</span>');
            $("#patientRegCodeEMsg").html("");
        };
    });
    // 当点击重置按钮时，让提交按钮显示为不可点击状态
    $('#patientRegReset').click(function(){
        $('#patientRegSubmit').attr('disabled','disabled');
    });
    // 当点击提交按钮时，对所有组件验证不为空时，再提交
    $('#patientRegSubmit').click(function(){
        if ($('#patientRegCode').val() == '') {
            flag = false;
            $('#patientRegCode').focus();
            $("#patientRegCode").parent().parent().parent().removeClass('has-success has-feedback');
            $("#patientRegCode").parent().parent().parent().addClass('has-error has-feedback');
            $(".healthms-patient-reg-code-err").remove();
            $("#patientRegCode").parent().after('<span class="healthms-patient-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-patient-reg-code-err sr-only">(error)</span>');
            $("#patientRegCodeEMsg").html('验证码不能为空');
        }
        if ($('#patientRegTel').val() == '') {
            flag = false;
            $('#patientRegTel').focus();
            regInputError('patientRegTel', 'healthms-patient-reg-tel-err', '电话不能为空', true);
        };
        if ($('#patientRegAddress').val() == '') {
            flag = false;
            $('#patientRegAddress').focus();
            regInputError('patientRegAddress', 'healthms-patient-reg-address-err', '住址/单位不能为空', true);
        };
        if ($('#patientRegProfession').val() == '') {
            flag = false;
            $('#patientRegProfession').focus();
            regInputError('patientRegProfession', 'healthms-patient-reg-profession-err', '职业不能为空', true);
        };
        if ($('#patientRegCounty').hasClass('hidden')) {
            if (($('#patientRegProvince').val() == '') || ($('#patientRegCity').val() == '') || ($('#patientRegCity').val() == '请选择')) {
                flag = false;
                regNoInputError('patientRegProvince', '籍贯不能为空', true);
            };
        } else {
            if (($('#patientRegProvince').val() == '') || ($('#patientRegCity').val() == '') || ($('#patientRegCity').val() == '请选择') || ($('#patientRegCounty').val() == '') || ($('#patientRegCounty').val() == '请选择')) {
                flag = false;
                regNoInputError('patientRegProvince', '籍贯不能为空', true);
            };
        };
        if ($('#patientRegNation').val() == '') {
            flag = false;
            regNoInputError('patientRegNation', '民族不能为空', true);
        };
        if ($('#patientRegBirthday').val() == '') {
            flag = false;
            $('#patientRegName').focus();
            regInputError('patientRegBirthday', 'healthms-patient-reg-birthday-err', '出生日期不能为空', true);
        };
        if ($('#patientRegName').val() == '') {
            flag = false;
            $('#patientRegName').focus();
            regInputError('patientRegName', 'healthms-patient-reg-name-err', '姓名不能为空', true);
        };
        if ($('#patientRegPasswordCon').val() == '') {
            flag = false;
            $('#patientRegPasswordCon').focus();
            regInputError('patientRegPasswordCon', 'healthms-patient-reg-pwdcon-err', '密码不能为空', true);
        };
        if ($('#patientRegPassword').val() == '') {
            flag = false;
            $('#patientRegPassword').focus();
            regInputError('patientRegPassword', 'healthms-patient-reg-pwd-err', '密码不能为空', true);
        };
        if ($('#patientRegEmail').val() == '') {
            flag = false;
            $('#patientRegEmail').focus();
            regInputError('patientRegEmail', 'healthms-patient-reg-email-err', '电子邮箱不能为空', true);
        };
        // 当 flag 为 true 时，即 所有组件验证正确时，提交
        if (flag) {
            $('#patientRegForm').submit();
        };
    });
});

function getUserTyp() {
    return $("#regType").val();
}

function loadCity() {
    var provinceName = $("#patientRegProvince option:selected").val();
    $('#patientRegCounty').empty();
    $('#patientRegCounty').html("<option value=''>请选择</option>");
    for (var i = 0; i < chinaItems.length; i++) {
        var provinceItem = chinaItems[i];
        if (provinceItem.name == provinceName) {
            var cityItems = provinceItem.sub;
            var cityHtml = "";
            if (provinceItem.type == 0) {
                $('#patientRegCounty').addClass('hidden');
                $("#patientRegCity").removeAttr("onclick","loadCounty();");

            } else {
                $('#patientRegCounty').removeClass('hidden');
                $("#patientRegCity").attr("onclick","loadCounty('" + JSON.stringify(cityItems) + "');");
            };
            for (var i = 0; i < cityItems.length; i++) {
                var cityItem = cityItems[i];
                cityHtml += "<option value='" + cityItem.name + "'>" + cityItem.name + "</option>";
            };
            $('#patientRegCity').html(cityHtml);
            break;
        };
    };
};

function loadCounty(cityItemsStr) {
    var cityName = $("#patientRegCity option:selected").val();
    var cityItems = JSON.parse(cityItemsStr)
    for (var i = 0; i < cityItems.length; i++) {
        var cityItem = cityItems[i];
        if (cityItem.name == cityName) {
            var countyItems = cityItem.sub;
            var countyHtml = "";
            if (cityItem.name == '其他'){
                $('#patientRegCounty').addClass('hidden');
            } else {
                $('#patientRegCounty').removeClass('hidden');
                if (countyItems.length == 0 && cityItem.name != '请选择') {
                    countyHtml += "<option value=''>请选择</option><option value='其他'>其他</option>";
                } else if (cityItem.name == '请选择') {
                    countyHtml += "<option value=''>请选择</option>";
                } else {
                    for (var i = 0; i < countyItems.length; i++) {
                        var countyItem = countyItems[i];
                        countyHtml += "<option value='" + countyItem.name + "'>" + countyItem.name + "</option>";     
                    };   
                };
            };
            $('#patientRegCounty').html(countyHtml);
            break;
        };
    };
};

function checkProtocol() {
    if ($('#patientRegProt').is(':checked')) {
        $('#patientRegSubmit').removeAttr('disabled');
    } else {
        $('#patientRegSubmit').attr('disabled','disabled');
    };
};

function checkEmail(email) {
    if (email.match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)) { 
        return true; 
    }
    return false;
};

function checkEmailExist (email, typ) {
    var result;
    $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT + '/check_email_exist',
        dataType: 'json',
        async:false,
        data: {
            'typ': typ,
            'email' : email
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            result = data.result;
        }
    });
    return result;
}

function checkPwdLength(pwd) {
    if (6 <= pwd.length && 20 >= pwd.length) { 
        return true; 
    }
    return false;
};

function checkPwdEqual(pwd, pwdCon) {
    if (pwd == pwdCon) { 
        return true; 
    }
    return false;
};

function checkTel(tel) {
    if (tel.match(/^(?:13\d|15\d|18\d)\d{5}(\d{3}|\*{3})$/) || tel.match(/^((0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/)) { 
        return true; 
    }
    return false;
};

function changeCode(){    
    var url = "/code/" + Math.random();
    $("#patientRegCodeImg").attr("src",url);
    $("#patientRegCode").parent().parent().parent().removeClass('has-success has-feedback');
    $("#patientRegCode").parent().parent().parent().addClass('has-error has-feedback');
    $(".healthms-patient-reg-code-err").remove();
    $("#patientRegCode").parent().after('<span class="healthms-patient-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-patient-reg-code-err sr-only">(error)</span>');
    $("#patientRegCodeEMsg").html('验证码不正确');
    return false;
};

function checkCode() {
    var result;
    $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT + '/code/0.1',
        dataType: 'json',
        async:false,
        data: {
            'code' : $('#patientRegCode').val()
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            result = data.result;
        }
    });
    return result;
};

function regInputError(id, cla, str, error) {
    if (error) {
        $("#" + id).parents().filter(".form-group").removeClass('has-success has-feedback');
        $("#" + id).parents().filter(".form-group").addClass('has-error has-feedback');
        $("." + cla).remove();
        $("#" + id).after('<span class="' + cla + ' glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="' + cla + ' sr-only">(error)</span>');
        $("#" + id + "EMsg").html(str);
    } else {
        $("#" + id).parents().filter(".form-group").removeClass('has-error has-feedback');
        $("#" + id).parents().filter(".form-group").addClass('has-success has-feedback');
        $("." + cla).remove();
        $("#" + id).after('<span class="' + cla + ' glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span><span class="' + cla + ' sr-only">(success)</span>');
        $("#" + id + "EMsg").html(str);
    }
}

function regNoInputError(id, str, error) {
    if (error) {
        $("#" + id + "EMsg").html(str);
    } else {
        $("#" + id + "EMsg").html(str);
    };

}

function ajaxDelTestResult (delId) {
    $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT + '/index/history',
        dataType: 'json',
        data: {
            'delId': delId,
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            if (data.result == 'success') {
                history.go(0);
            };
        }
    });
    return false
}



