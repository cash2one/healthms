$(document).ready(function(){

    var userTyp = getUserTyp();

    // 从 json 数组中 动态添加民族
    var patientNationSelect = $('#patientRegNation');
    patientNationSelect.append('<option value="">请选择</option>');
    for(var i= 0; i < nationItems.length; i++) {
        var nation = nationItems[i];
        var name = nation.name;
        patientNationSelect.append('<option value="' + name + '">' + name + '</option>');
    };

    // 设置点击出生日期时 弹出 datetimepicker
    $('#regBirthday').datetimepicker({
        lang:'ch',
        timepicker:false,
        format:'Y-m-d'
    });

    // 验证表单
    var flag = true;

    $('#regEmail').blur(function(){
        var result = 'true';
        if ($('#regEmail').val() == '') { 
            result = '电子邮箱不能为空';
        } else if (!checkEmail($('#regEmail').val())) {
            result = '电子邮箱格式不正确';
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

    $('#regEmail').keyup(function(){
        if (!checkEmail($('#regEmail').val())) {
            flag = false;
            regInputError('regEmail', 'healthms-reg-email-err', '电子邮箱格式不正确', true);
        } else {
            flag = true;
            regInputError('regEmail', 'healthms-reg-email-err', '', false);
        };
    });



    $('#regPassword').blur(function(){
        if ($('#regPassword').val() == '') { 
            flag = false;
            regInputError('regPassword', 'healthms-reg-pwd-err', '密码不能为空', true);
        } else if (!checkPwdLength($('#regPassword').val())) {
            flag = false;
            regInputError('regPassword', 'healthms-reg-pwd-err', '密码长度为6-20位字符', true);
        } else {
            flag = true;
            regInputError('regPassword', 'healthms-reg-pwd-err', '', false);
        };
    });

    $('#regPassword').keyup(function(){
        if (!checkPwdLength($('#regPassword').val())) {
            flag = false;
            regInputError('regPassword', 'healthms-reg-pwd-err', '密码长度为6-20位字符', true);
        } else {
            flag = true;
            regInputError('regPassword', 'healthms-reg-pwd-err', '', false);
        };
    });

    $('#regPasswordCon').blur(function(){
        if ($('#regPasswordCon').val() == '') { 
            flag = false;
            regInputError('regPasswordCon', 'healthms-reg-pwdcon-err', '密码不能为空', true);
        } else if (!checkPwdEqual($('#regPassword').val(), $('#regPasswordCon').val())) {
            flag = false;
            regInputError('regPasswordCon', 'healthms-reg-pwdcon-err', '两次输入密码不一致', true);
        } else {
            flag = true;
            regInputError('regPasswordCon', 'healthms-reg-pwdcon-err', '', false);
        };
    });
    $('#regPasswordCon').keyup(function(){
        if (!checkPwdEqual($('#regPassword').val(), $('#regPasswordCon').val())) {
            flag = false;
            regInputError('regPasswordCon', 'healthms-reg-pwdcon-err', '两次输入密码不一致', true);
        } else {
            flag = true;
            regInputError('regPasswordCon', 'healthms-reg-pwdcon-err', '', false);
        };
    });

    $('#regName').blur(function(){
        if ($('#regName').val() == '') {
            flag = false;
            regInputError('regName', 'healthms-reg-name-err', '姓名不能为空', true);
        } else {
            flag = true;
            regInputError('regName', 'healthms-reg-name-err', '', false);
        };
    });

    $('#regBirthday').blur(function(){
        if ($('#regBirthday').val() == '') {
            flag = false;
            regInputError('regBirthday', 'healthms-reg-birthday-err', '出生日期不能为空', true);
        } else {
            flag = true;
            regInputError('regBirthday', 'healthms-reg-birthday-err', '', false);
        };
    });

    $('#regCode').blur(function(){
        var result = 'true';
        if ($('#regCode').val() == '') { 
            result = '验证码不能为空';
        } else if (!checkCode()) {
            result = '验证码不正确';
        }
        if (result != 'true') {
            flag = false;
            $("#regCode").parent().parent().parent().removeClass('has-success has-feedback');
            $("#regCode").parent().parent().parent().addClass('has-error has-feedback');
            $(".healthms-reg-code-err").remove();
            $("#regCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(error)</span>');
            $("#regCodeEMsg").html(result);
                } else {
            flag = true;
            $("#regCode").parent().parent().parent().removeClass('has-error has-feedback');
            $("#regCode").parent().parent().parent().addClass('has-success has-feedback');
            $(".healthms-reg-code-err").remove();
            $("#regCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(success)</span>');
            $("#regCodeEMsg").html("");
        };
    });
    $('#regTel').blur(function(){
        if (!checkTel($('#regTel').val())) {
            flag = false;
            regInputError('regTel', 'healthms-reg-tel-err', '电话格式不正确', true);
        } else if ($('#regTel').val() == '') { 
            flag = false;
            regInputError('regTel', 'healthms-reg-tel-err', '电话不能为空', true);
        } else {
            flag = true;
            regInputError('regTel', 'healthms-reg-tel-err', '', false);
        };
    });
    $('#regTel').keyup(function(){
        if (!checkTel($('#regTel').val())) {
            flag = false;
            regInputError('regTel', 'healthms-reg-tel-err', '电话格式不正确', true);
        } else {
            flag = true;
            regInputError('regTel', 'healthms-reg-tel-err', '', false);
        };
    });
    // 用户注册特有字段
    if (userTyp == 'patient') {
        $('#patientRegNation').blur(function(){
            if ($('#patientRegNation').val() == '') {
                flag = false;
                regNoInputError('patientRegNation', '民族不能为空', true);
            } else {
                flag = true;
                regNoInputError('patientRegNation', '', false);
            };
        });
        $('#regProvince').blur(function(){
            if ($('#regCounty').hasClass('hidden')) {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择')) {
                    flag = false;
                    regNoInputError('regProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('regProvince', '', false);
                };
            } else {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择')) {
                    flag = false;
                    regNoInputError('regProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('regProvince', '', false);
                };
            };
        });
        $('#regCity').blur(function(){
            if ($('#regCounty').hasClass('hidden')) {
                if ($('#regCity').val() == '' || $('#regCity').val() == '请选择') {
                    flag = false;
                    regNoInputError('regProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('regProvince', '', false);
                };
            } else {
                if (($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择')) {
                    flag = false;
                    regNoInputError('regProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('regProvince', '', false);
                };
            };
        });
        $('#regCounty').blur(function(){
            if ($('#regCounty').val() == '' || $('#regCounty').val() == '请选择') {
                flag = false;
                regNoInputError('regProvince', '籍贯不能为空', true);
            } else {
                flag = true;
                regNoInputError('regProvince', '', false);
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
    } else if (userTyp == 'doctor') { // 医生注册特有字段
        $('#doctorRegCheckTelCode').blur(function(){
            if ($('#doctorRegCheckTelCode').val() == '' || $('#doctorRegCheckTel').val() == '') {
                flag = false;
                regInputError('doctorRegCheckTel', 'healthms-reg-check-tel-err', '身份核实电话不能为空', true);
            } else {
                flag = true;
                regInputError('doctorRegCheckTel', 'healthms-reg-check-tel-err', '', false);
            };
        });
        $('#doctorRegCheckTel').blur(function(){
            if ($('#doctorRegCheckTel').val() == '' || $('#doctorRegCheckTelCode').val() == '') {
                flag = false;
                regInputError('doctorRegCheckTel', 'healthms-reg-check-tel-err', '身份核实电话不能为空', true);
            } else {
                flag = true;
                regInputError('doctorRegCheckTel', 'healthms-reg-check-tel-err', '', false);
            };
        });
        $('#regProvince').blur(function(){
            if ($('#regCounty').hasClass('hidden')) {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
                };
            } else {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
                };
            };
        });
        $('#regCity').blur(function(){
            if ($('#regCounty').hasClass('hidden')) {
                if ($('#regCity').val() == '' || $('#regCity').val() == '请选择' || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
                };
            } else {
                if (($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
                };
            };
        });
        $('#regCounty').blur(function(){
            if ($('#regCounty').val() == '' || $('#regCounty').val() == '请选择' || ($('#regHospitalName').val() == '')) {
                flag = false;
                regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
            } else {
                flag = true;
                regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
            };
        });
        $('#regHospitalName').blur(function(){
            if ($('#regCounty').hasClass('hidden')) {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
                };
            } else {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '', false);
                };
            };
        });
        $('#doctorRegOffices').blur(function(){
            if ($('#doctorRegOffices').val() == '') {
                flag = false;
                regInputError('doctorRegOffices', 'healthms-reg-offices-err', '科室不能为空', true);
            } else {
                flag = true;
                regInputError('doctorRegOffices', 'healthms-reg-offices-err', '', false);
            };
        });
        $('#doctorRegProfessional').blur(function(){
            if ($('#doctorRegProfessional').val() == '') {
                flag = false;
                regNoInputError('doctorRegProfessional', '职称不能为空', true);
            } else {
                flag = true;
                regNoInputError('doctorRegProfessional', '', false);
            };
        });
        $('#doctorRegJob').blur(function(){
            if ($('#doctorRegJob').val() == '') {
                flag = false;
                regInputError('doctorRegJob', 'healthms-reg-job-err', '职务不能为空', true);
            } else {
                flag = true;
                regInputError('doctorRegJob', 'healthms-reg-job-err', '', false);
            };
        });
        $('#doctorRegSpecialty').blur(function(){
            if ($('#doctorRegSpecialty').val() == '') {
                flag = false;
                regInputError('doctorRegSpecialty', 'healthms-reg-specialty-err', '专业特长不能为空', true);
            } else {
                flag = true;
                regInputError('doctorRegSpecialty', 'healthms-reg-specialty-err', '', false);
            };
        });
    };

    // 当点击重置按钮时，让提交按钮显示为不可点击状态
    $('#regReset').click(function(){
        $('#regSubmit').attr('disabled','disabled');
    });
    // 当点击提交按钮时，对所有组件验证不为空时，再提交
    $('#regSubmit').click(function(){
        if ($('#regCode').val() == '') {
            flag = false;
            $('#regCode').focus();
            $("#regCode").parent().parent().parent().removeClass('has-success has-feedback');
            $("#regCode").parent().parent().parent().addClass('has-error has-feedback');
            $(".healthms-reg-code-err").remove();
            $("#regCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(error)</span>');
            $("#regCodeEMsg").html('验证码不能为空');
        }
        if ($('#regTel').val() == '') {
            flag = false;
            $('#regTel').focus();
            regInputError('patientRegTel', 'healthms-reg-tel-err', '电话不能为空', true);
        };
        if (userTyp == 'patient') {
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
            if ($('#regCounty').hasClass('hidden')) {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择')) {
                    flag = false;
                    regNoInputError('regProvince', '籍贯不能为空', true);
                };
            } else {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择')) {
                    flag = false;
                    regNoInputError('regProvince', '籍贯不能为空', true);
                };
            };
            if ($('#patientRegNation').val() == '') {
                flag = false;
                regNoInputError('patientRegNation', '民族不能为空', true);
            };
        } else if (userTyp == 'doctor') {
            if ($('#doctorRegSpecialty').val() == '') {
                flag = false;
                $('#doctorRegSpecialty').focus();
                regInputError('doctorRegSpecialty', 'healthms-reg-specialty-err', '专业特长不能为空', true);
            };
            if ($('#doctorRegJob').val() == '') {
                flag = false;
                $('#doctorRegJob').focus();
                regInputError('doctorRegJob', 'healthms-reg-job-err', '职务不能为空', true);
            };
            if ($('#doctorRegProfessional').val() == '') {
                flag = false;
                regNoInputError('doctorRegProfessional', '职称不能为空', true);
            }
            if ($('#doctorRegOffices').val() == '') {
                flag = false;
                regInputError('doctorRegOffices', 'healthms-reg-offices-err', '科室不能为空', true);
            }
            if ($('#regCounty').hasClass('hidden')) {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    $('#regHospitalName').focus();
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                };
            } else {
                if (($('#regProvince').val() == '') || ($('#regCity').val() == '') || ($('#regCity').val() == '请选择') || ($('#regCounty').val() == '') || ($('#regCounty').val() == '请选择') || ($('#regHospitalName').val() == '')) {
                    flag = false;
                    $('#regHospitalName').focus();
                    regInputError('regHospitalName', 'healthms-reg-hospital-err', '工作医院不能为空', true);
                };
            };
            if ($('#doctorRegCheckTel').val() == '' || $('#doctorRegCheckTelCode').val() == '') {
                flag = false;
                regInputError('doctorRegCheckTel', 'healthms-reg-tel-err', '身份核实电话不能为空', true);
            };
        };
        if ($('#regBirthday').val() == '') {
            flag = false;
            $('#regBirthday').focus();
            regInputError('regBirthday', 'healthms-reg-birthday-err', '出生日期不能为空', true);
        };
        if ($('#regName').val() == '') {
            flag = false;
            $('#regName').focus();
            regInputError('regName', 'healthms-reg-name-err', '姓名不能为空', true);
        };
        if ($('#regPasswordCon').val() == '') {
            flag = false;
            $('#regPasswordCon').focus();
            regInputError('regPasswordCon', 'healthms-reg-pwdcon-err', '密码不能为空', true);
        };
        if ($('#regPassword').val() == '') {
            flag = false;
            $('#regPassword').focus();
            regInputError('regPassword', 'healthms-reg-pwd-err', '密码不能为空', true);
        };
        if ($('#regEmail').val() == '') {
            flag = false;
            $('#regEmail').focus();
            regInputError('regEmail', 'healthms-reg-email-err', '电子邮箱不能为空', true);
        };
        // 当 flag 为 true 时，即 所有组件验证正确时，提交
        if (flag) {
            $('#regForm').submit();
        };
    });
});

function getUserTyp() {
    return $("#regType").val();
}

function loadCity() {
    var provinceName = $("#regProvince option:selected").val();
    $('#regCounty').empty();
    $('#regCounty').html("<option value=''>请选择</option>");
    for (var i = 0; i < chinaItems.length; i++) {
        var provinceItem = chinaItems[i];
        if (provinceItem.name == provinceName) {
            var cityItems = provinceItem.sub;
            var cityHtml = "";
            if (provinceItem.type == 0) {
                $('#regCounty').addClass('hidden');
                $("#regCity").removeAttr("onclick","loadCounty();");

            } else {
                $('#regCounty').removeClass('hidden');
                $("#regCity").attr("onclick","loadCounty('" + JSON.stringify(cityItems) + "');");
            };
            for (var i = 0; i < cityItems.length; i++) {
                var cityItem = cityItems[i];
                cityHtml += "<option value='" + cityItem.name + "'>" + cityItem.name + "</option>";
            };
            $('#regCity').html(cityHtml);
            break;
        };
    };
};

function loadCounty(cityItemsStr) {
    var cityName = $("#regCity option:selected").val();
    var cityItems = JSON.parse(cityItemsStr)
    for (var i = 0; i < cityItems.length; i++) {
        var cityItem = cityItems[i];
        if (cityItem.name == cityName) {
            var countyItems = cityItem.sub;
            var countyHtml = "";
            if (cityItem.name == '其他'){
                $('#regCounty').addClass('hidden');
            } else {
                $('#regCounty').removeClass('hidden');
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
            $('#regCounty').html(countyHtml);
            break;
        };
    };
};

function checkProtocol() {
    if ($('#regProt').is(':checked')) {
        $('#regSubmit').removeAttr('disabled');
    } else {
        $('#regSubmit').attr('disabled','disabled');
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
    $("#regCodeImg").attr("src",url);
    $("#regCode").parent().parent().parent().removeClass('has-success has-feedback');
    $("#regCode").parent().parent().parent().addClass('has-error has-feedback');
    $(".healthms-reg-code-err").remove();
    $("#regCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(error)</span>');
    $("#regCodeEMsg").html('验证码不正确');
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
            'code': $('#regCode').val()
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