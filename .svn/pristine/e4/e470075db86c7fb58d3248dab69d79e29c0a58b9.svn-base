$(document).ready(function() {
    var userTyp = $("#userTyp").val();

    // 设置点击出生日期时 弹出 datetimepicker
    $('#editBirthday').datetimepicker({
        lang: 'ch',
        timepicker: false,
        format: 'Y-m-d'
    });

    // 设置省或直辖市
    var provinceItems = ["北京", "上海", "天津", "重庆", "河北", "山西", "河南", "辽宁", "吉林", "黑龙江", "内蒙古", "江苏", "山东", "安徽", "浙江", "福建", "湖北", "湖南", "广东", "广西", "江西", "四川", "海南", "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆", "台湾", "香港", "澳门"];
    var provinceSelect = $("#editProvince");
    provinceSelect.append('<option value="">请选择</option>')
    for (var i = 0; i < provinceItems.length; i++) {
        var province = provinceItems[i];
        if (province == curProvince) {
            provinceSelect.append('<option value="' + province + '" selected="selected">' + province + '</option>')
        } else {
            provinceSelect.append('<option value="' + province + '">' + province + '</option>')
        };
    };
    //设置市
    var cityItems = ""
    var citySelect = $("#editCity");
    for (var i = 0; i < chinaItems.length; i++) {
        var provinceItem = chinaItems[i];
        if (provinceItem.name == curProvince) {
            var cityItems = provinceItem.sub;
            if (provinceItem.type == 0) {
                $('#editCounty').addClass('hidden');
                $("#editCity").removeAttr("onclick", "loadCounty();");

            } else {
                $('#editCounty').removeClass('hidden');
                $("#editCity").attr("onclick", "loadCounty('" + JSON.stringify(cityItems) + "');");
            };
            for (var i = 0; i < cityItems.length; i++) {
                var cityItem = cityItems[i];
                if (cityItem.name == curCity) {
                    citySelect.append('<option value="' + cityItem.name + '" selected = "selected">' + cityItem.name + '</option>');
                } else {
                    citySelect.append("<option value='" + cityItem.name + "'>" + cityItem.name + "</option>");
                }
            };
        };
    };
    //设置区县
    if (curCounty != "") {
        var countySelect = $("#editCounty");
        for (var i = 0; i < cityItems.length; i++) {
            var cityItem = cityItems[i];
            if (cityItem.name == curCity) {
                var countyItems = cityItem.sub;
                for (var i = 0; i < countyItems.length; i++) {
                    var countyItem = countyItems[i];
                    if (countyItem.name == curCounty) {
                        countySelect.append('<option value="' + countyItem.name + '" selected="selected">' + countyItem.name + "</option>");
                    } else {
                        countySelect.append("<option value='" + countyItem.name + "'>" + countyItem.name + "</option>");
                    };
                };
            };
        };
    } else {
        $('#editCounty').addClass('hidden');
        $("#editCity").removeAttr("onclick", "editLoadCounty();");
    }

    if (userTyp == 'patient') {
        // 从 json 数组中 动态添加民族
        var nationSelect = $('#editPatientNation');
        nationSelect.append('<option value="">请选择</option>');
        for (var i = 0; i < nationItems.length; i++) {
            var nation = nationItems[i];
            var name = nation.name;
            if (name == curNation) {
                nationSelect.append('<option value="' + name + '" selected="selected">' + name + '</option>');
            } else {
                nationSelect.append('<option value="' + name + '">' + name + '</option>');
            };
        };
    } else if (userTyp == 'doctor') {
        // 动态添加 职称
        var professionalItems = ["助理医师", "医师", "主治医师", "副主任医师", "主任医师"];
        var professionalSelect = $('#editDoctorProfessional');
        professionalSelect.append('<option value="">请选择</option>');
        for (var i = 0; i < professionalItems.length; i++) {
            var professional = professionalItems[i];
            if (professional == curProfessional) {
                professionalSelect.append('<option value="' + professional + '" selected="selected">' + professional + '</option>');
            } else {
                professionalSelect.append('<option value="' + professional + '">' + professional + '</option>');
            };
        };
    }


    // 验证表单
    var flag = false;
    $("#editBirthday").blur(function() {
        if ($('#editBirthday').val() == '') {
            falg = false;
            regInputError('editBirthday', 'healthms-edit-birthday-err', '出生日期不能为空', true);
        } else {
            falg = true;
            regInputError('editBirthday', 'healthms-edit-birthday-err', '', false);
        };
    });

    $('#editTel').blur(function(){
        if (!checkTel($('#editTel').val())) {
            flag = false;
            regInputError('editTel', 'healthms-tel-err', '电话格式不正确', true);
        } else if ($('#editTel').val() == '') { 
            flag = false;
            regInputError('editTel', 'healthms-tel-err', '电话不能为空', true);
        } else {
            flag = true;
            regInputError('editTel', 'healthms-tel-err', '', false);
        };
    });
    // 患者特有表单
    if (userTyp == "patient") {
        $('#editPatientNation').blur(function() {
            if ($('#editPatientNation').val() == '') {
                falg = false;
                regNoInputError('editPatientNation', '民族不能为空', true);
            } else {
                flag = true;
                regNoInputError('editPatientNation', '', false);
            };
        });
        $('#editProvince').blur(function() {
            if ($('#editCounty').hasClass('hidden')) {
                if (($('#editProvince').val() == '') || ($('#editCity').val() == '') || ($('#editCity').val() == '请选择')) {
                    falg = false;
                    regNoInputError('editProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('editProvince', '', false);
                };
            } else {
                if (($('#editProvince').val() == '') || ($('#editCity').val() == '') || ($('#editCity').val() == '请选择') || ($('#editCounty').val() == '') || ($('#editCounty').val() == '请选择')) {
                    falg = false;
                    regNoInputError('editProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('editProvince', '', false);
                };
            };
        });
        $('#editCity').blur(function() {
            if ($('#editCounty').hasClass('hidden')) {
                if ($('#editCity').val() == '' || $('#editCity').val() == '请选择') {
                    falg = false;
                    regNoInputError('editProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('editProvince', '', false);
                };
            } else {
                if (($('#editCity').val() == '') || ($('#editCity').val() == '请选择') || ($('#editCounty').val() == '') || ($('#editCounty').val() == '请选择')) {
                    falg = false;
                    regNoInputError('editProvince', '籍贯不能为空', true);
                } else {
                    flag = true;
                    regNoInputError('editProvince', '', false);
                };
            };
        });
        $('#editCounty').blur(function() {
            if ($('#editCounty').val() == '' || $('#editCounty').val() == '请选择') {
                flag = false;
                regNoInputError('editProvince', '籍贯不能为空', true);
            } else {
                flag = true;
                regNoInputError('editProvince', '', false);
            };
        });
        $('#editPatientProfession').blur(function() {
            if ($('#editPatientProfession').val() == '') {
                flag = false;
                regInputError('editPatientProfession', 'healthms-edit-profession-err', '职业不能为空', true);
            } else {
                flag = true;
                regInputError('editPatientProfession', 'healthms-edit-profession-err', '', false);
            };
        });
        $('#editPatientAddress').blur(function() {
            if ($('#editPatientAddress').val() == '') {
                flag = false;
                regInputError('editPatientAddress', 'healthms-edit-address-err', '住址/单位不能为空', true);
            } else {
                flag = true;
                regInputError('editPatientAddress', 'healthms-edit-address-err', '', false);
            };
        });
    // 医生特有表单
    } else if (userTyp == 'doctor') {
        $('#editDoctorCheckTel').blur(function() {
            if (!checkTel($('#editDoctorCheckTel').val())) {
                flag = false;
                regInputError('editDoctorCheckTel', 'healthms-check-tel-err', '身份核实电话格式不正确', true);
            } else if ($('#editDoctorCheckTel').val() == '') {
                flag = false;
                regInputError('editDoctorCheckTel', 'healthms-check-tel-err', '身份核实电话不能为空', true);
            } else {
                flag = true;
                regInputError('editDoctorCheckTel', 'healthms-check-tel-err', '', false);
            };
        });
        $('#editProvince').blur(function() {
            if ($('#editCounty').hasClass('hidden')) {
                if (($('#editProvince').val() == '') || ($('#editCity').val() == '') || ($('#editCity').val() == '请选择') || ($('#editDoctorHospitalName').val() == '')) {
                    falg = false;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '', false);
                };
            } else {
                if (($('#editProvince').val() == '') || ($('#editCity').val() == '') || ($('#editCity').val() == '请选择') || ($('#editCounty').val() == '') || ($('#editCounty').val() == '请选择') || ($('#editDoctorHospitalName').val() == '')) {
                    falg = false;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '', false);
                };
            };
        });
        $('#editCity').blur(function() {
            if ($('#editCounty').hasClass('hidden')) {
                if ($('#editCity').val() == '' || $('#editCity').val() == '请选择' || $('#editDoctorHospitalName').val() == '') {
                    falg = false;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '', false);
                };
            } else {
                if (($('#editCity').val() == '') || ($('#editCity').val() == '请选择') || ($('#editCounty').val() == '') || ($('#editCounty').val() == '请选择') || $('#editDoctorHospitalName').val() == '') {
                    falg = false;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '工作医院不能为空', true);
                } else {
                    flag = true;
                    regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '', false);
                };
            };
        });
        $('#editCounty').blur(function() {
            if ($('#editCounty').val() == '' || $('#editCounty').val() == '请选择' || $('#editDoctorHospitalName').val() == '') {
                flag = false;
                regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '工作医院不能为空', true);
            } else {
                flag = true;
                regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '', false);
            };
        });
        $('#editDoctorHospitalName').blur(function() {
            if ($('#editDoctorHospitalName').val() == '') {
                flag = false;
                regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '工作医院不能为空', true);
            } else {
                flag = true;
                regInputError('editDoctorHospitalName', 'healthms-edit-Hospital-name-err', '', false);
            };
        });

        $('#editDoctorOffices').blur(function() {
            if ($('#editDoctorOffices').val() == '') {
                flag = false;
                regInputError('editDoctorOffices', 'healthms-edit-offices-err', '科室不能为空', true);
            } else {
                flag = true;
                regInputError('editDoctorOffices', 'healthms-edit-offices-err', '', false);
            };
        });

        $('#editDoctorJob').blur(function() {
            if ($('#editDoctorJob').val() == '') {
                flag = false;
                regInputError('editDoctorJob', 'healthms-edit-job-err', '职务不能为空', true);
            } else {
                flag = true;
                regInputError('editDoctorJob', 'healthms-edit-job-err', '', false);
            };
        });
        $('#editDoctorSpecialty').blur(function() {
            if ($('#editDoctorSpecialty').val() == '') {
                flag = false;
                regInputError('editDoctorSpecialty', 'healthms-edit-specialty-err', '专业特长不能为空', true);
            } else {
                flag = true;
                regInputError('editDoctorSpecialty', 'healthms-edit-specialty-err', '', false);
            };
        });
        $('#editDoctorProfessional').blur(function() {
            if ($('#editDoctorProfessional').val() == '') {
                flag = false;
                regNoInputError('editDoctorProfessional', '请选择职称', true);
            } else {
                flag = true;
                regNoInputError('editDoctorProfessional', '', false);
            };
        });
    };  // 特有表单验证完毕
    
    $('#editCode').blur(function() {
        var result = 'true';
        if ($('#editCode').val() == '') {
            result = '验证码不能为空';
        } else if (!checkCode()) {
            result = '验证码不正确';
        }
        if (result != 'true') {
            flag = false;
            $("#editCode").parent().parent().parent().removeClass('has-success has-feedback');
            $("#editCode").parent().parent().parent().addClass('has-error has-feedback');
            $(".healthms-reg-code-err").remove();
            $("#editCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(error)</span>');
            $("#editCodeEMsg").html(result);
        } else {
            flag = true;
            $("#editCode").parent().parent().parent().removeClass('has-error has-feedback');
            $("#editCode").parent().parent().parent().addClass('has-success has-feedback');
            $(".healthms-reg-code-err").remove();
            $("#editCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(success)</span>');
            $("#editCodeEMsg").html("");
        };
    });

    // 提交表单
    $("#editSubmit").click(function(){
        if ($('#editCode').val() == '') {
            flag = false;
            $("#editCode").parent().parent().parent().removeClass('has-success has-feedback');
            $("#editCode").parent().parent().parent().addClass('has-error has-feedback');
            $(".healthms-reg-code-err").remove();
            $("#editCode").parent().after('<span class="healthms-reg-code-err glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="healthms-reg-code-err sr-only">(error)</span>');
            $("#editCodeEMsg").html('验证码不能为空');
        };
        if (flag) {
            $("#editForm").submit();
        };
    });
});



function editLoadCity() {
    var provinceName = $("#editProvince option:selected").val();
    $('#editCounty').empty();
    $('#editCounty').html("<option value=''>请选择</option>");
    for (var i = 0; i < chinaItems.length; i++) {
        var provinceItem = chinaItems[i];
        if (provinceItem.name == provinceName) {
            var cityItems = provinceItem.sub;
            var cityHtml = "";
            if (provinceItem.type == 0) {
                $('#editCounty').addClass('hidden');
                $("#editCity").removeAttr("onclick", "editLoadCounty();");

            } else {
                $('#editCounty').removeClass('hidden');
                $("#editCity").attr("onclick", "editLoadCounty('" + JSON.stringify(cityItems) + "');");
            };
            for (var i = 0; i < cityItems.length; i++) {
                var cityItem = cityItems[i];
                cityHtml += "<option value='" + cityItem.name + "'>" + cityItem.name + "</option>";
            };
            $('#editCity').html(cityHtml);
            break;
        };
    };
};

function editLoadCounty(cityItemsStr) {
    var cityName = $("#editCity option:selected").val();
    var cityItems = JSON.parse(cityItemsStr)
    for (var i = 0; i < cityItems.length; i++) {
        var cityItem = cityItems[i];
        if (cityItem.name == cityName) {
            var countyItems = cityItem.sub;
            var countyHtml = "";
            if (cityItem.name == '其他') {
                $('#editCounty').addClass('hidden');
            } else {
                $('#editCounty').removeClass('hidden');
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
            $('#editCounty').html(countyHtml);
            break;
        };
    };
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

function checkTel(tel) {
    if (tel.match(/^(?:13\d|15\d|18\d)\d{5}(\d{3}|\*{3})$/) || tel.match(/^((0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$/)) {
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