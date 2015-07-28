// login.html js设置
$(document).ready(function() {

    // 用户 Email input 失去焦点时验证其是否为空 和 Email格式 是否正确
    $('#email').blur(function(){
        if ($('#email').val() == '') { 
            loginInputError('email', 'healthms-login-error-email', true);
        } else if (!checkEmail($('#email').val())) {
            loginInputError('email', 'healthms-login-error-email', true);
        } else {
            loginInputError('email', 'healthms-login-error-email', false);
        }
    });
    // 用户 密码 input 失去焦点时验证其是否为空
    $('#password').blur(function(){
        if ($('#password').val() == '') {
            loginInputError('password', 'healthms-login-error-password', true);
        } else {
            loginInputError('password', 'healthms-login-error-password', false);
        }
    });
});

// 以 Ajax 方式提交登录信息
function ajaxLoginForm(typ){
    $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT + '/login/' + typ,
        dataType: 'json',
        data: {
            'email': $('#email').val(),
            'password': $('#password').val()
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            if (data.typ == 'patient') {
                if (data.result == 'emailError') {
                    $("#healthms-login-error").empty().append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>对不起，用户不存在！</div>');
                    setTimeout('$("#healthms-login-error").slideDown();', 10);
                    $('#email').focus();
                    loginInputError('email', 'healthms-login-error-email', true);
                } else if (data.result == 'pwdError') {
                    $("#healthms-login-error").empty().append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>对不起，密码错误！</div>');
                    setTimeout('$("#healthms-login-error").slideDown();', 10);
                    $('#password').focus();
                    loginInputError('password', 'healthms-login-error-password', true);
                } else if (data.result == 'success') {
                    window.location.href = "/"
                }
            } else if (data.typ == 'doctor') {
                if (data.result == 'emailError') {
                    $("#healthms-login-error").empty().append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>对不起，用户不存在！</div>').slideDown();
                    $('#email').focus();
                    loginInputError('email', 'healthms-login-error-email', true);
                } else if (data.result == 'notCheck') {
                    $("#healthms-login-error").empty().append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>对不起，您的信息还未审核！</div>').slideDown();
                } else if (data.result == 'checkFailed') {
                    $("#healthms-login-error").empty().append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>对不起，您审核未通过，请重新申请！</div>').slideDown();
                } else if (data.result == 'pwdError') {
                    $("#healthms-login-error").empty().append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>对不起，密码错误！</div>').slideDown();
                    $('#password').focus();
                    loginInputError('password', 'healthms-login-error-password', true);
                } else if (data.result == 'success') {
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


function ajaxDelTestResult (testTitle, delId) {
    $.ajax({
        type: 'POST',
        url: $SCRIPT_ROOT + '/test/history/'+testTitle,
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

$(document).ready(function() {
    $('#healthms-test-nav-panel-2').click(function() {
        $('#healthms-test-nav-panel-2>.collapse').collapse('show');
        $('#healthms-test-nav-panel-3>.collapse').collapse('hide');
        $('#healthms-test-nav-panel-4>.collapse').collapse('hide');
    });
    $('#healthms-test-nav-panel-3').click(function() {
        $('#healthms-test-nav-panel-3>.collapse').collapse('show');
        $('#healthms-test-nav-panel-2>.collapse').collapse('hide');
        $('#healthms-test-nav-panel-4>.collapse').collapse('hide');
    });
    $('#healthms-test-nav-panel-4').click(function() {
        $('#healthms-test-nav-panel-4>.collapse').collapse('show');
        $('#healthms-test-nav-panel-3>.collapse').collapse('hide');
        $('#healthms-test-nav-panel-2>.collapse').collapse('hide');
    });
});

function checkEmail(email) {
    if (email.match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)) { 
        return true; 
    }
    return false;
};

