$(document).ready(function() {
    $('#cardinalSymptom').blur(function() {
        if ($('#cardinalSymptom').val() == '') {
            regInputError('cardinalSymptom', 'healthms-ask-cardinal-symptom-err', true);
        } else {
            regInputError('cardinalSymptom', 'healthms-ask-cardinal-symptom-err', false);
        };
    });
    $('#sickTime').blur(function() {
        if ($('#sickTime').val() == '') {
            regInputError('sickTime', 'healthms-ask-sick-time-err', true);
        } else {
            regInputError('sickTime', 'healthms-ask-sick-time-err', false);
        };
    });
    $('#lipColor').blur(function() {
        if ($('#lipColor').val() == '') {
            regInputError('lipColor', 'healthms-ask-lip-color-err', true);
        } else {
            regInputError('lipColor', 'healthms-ask-lip-color-err', false);
        };
    });
    $('#bodyFeel').blur(function() {
        if ($('#bodyFeel').val() == '') {
            regInputError('bodyFeel', 'healthms-ask-body-feel-err', true);
        } else {
            regInputError('bodyFeel', 'healthms-ask-body-feel-err', false);
        };
    });
    $('#sweatingCondition').blur(function() {
        if ($('#sweatingCondition').val() == '') {
            regInputError('sweatingCondition', 'healthms-ask-sweating-condition-err', true);
        } else {
            regInputError('sweatingCondition', 'healthms-ask-sweating-condition-err', false);
        };
    });
    $('#drinkingCondition').blur(function() {
        if ($('#drinkingCondition').val() == '') {
            regInputError('drinkingCondition', 'healthms-ask-drinking-condition-err', true);
        } else {
            regInputError('drinkingCondition', 'healthms-ask-drinking-condition-err', false);
        };
    });
    $('#shitCondition').blur(function() {
        if ($('#shitCondition').val() == '') {
            regInputError('shitCondition', 'healthms-ask-shit-condition-err', true);
        } else {
            regInputError('shitCondition', 'healthms-ask-shit-condition-err', false);
        };
    });
    $('#urineCondition').blur(function() {
        if ($('#urineCondition').val() == '') {
            regInputError('urineCondition', 'healthms-ask-urine-condition-err', true);
        } else {
            regInputError('urineCondition', 'healthms-ask-urine-condition-err', false);
        };
    });
    $('#spiritSleepCondition').blur(function() {
        if ($('#spiritSleepCondition').val() == '') {
            regInputError('spiritSleepCondition', 'healthms-ask-spirit-sleep-condition-err', true);
        } else {
            regInputError('spiritSleepCondition', 'healthms-ask-spirit-sleep-condition-err', false);
        };
    });
    $('#moodCondition').blur(function() {
        if ($('#moodCondition').val() == '') {
            regInputError('moodCondition', 'healthms-ask-mood-condition-err', true);
        } else {
            regInputError('moodCondition', 'healthms-ask-mood-condition-err', false);
        };
    });
    $('#tonguePulseCondition').blur(function() {
        if ($('#tonguePulseCondition').val() == '') {
            regInputError('tonguePulseCondition', 'healthms-ask-tongue-pulse-condition-err', true);
        } else {
            regInputError('tonguePulseCondition', 'healthms-ask-tongue-pulse-condition-err', false);
        };
    });
    if ($("#pubesCondition").length > 0) {
        $('#pubesCondition').blur(function() {
            if ($('#pubesCondition').val() == '') {
                regInputError('pubesCondition', 'healthms-ask-pubes-condition-err', true);
            } else {
                regInputError('pubesCondition', 'healthms-ask-pubes-condition-err', false);
            };
        });
    };
    $('#briefHistory').blur(function() {
        if ($('#briefHistory').val() == '') {
            regInputError('briefHistory', 'healthms-ask-brief-history-err', true);
        } else {
            regInputError('briefHistory', 'healthms-ask-brief-history-err', false);
        };
    });

});

function ajaxSubmitAsk() {
    var flag = true;
    if ($('#cardinalSymptom').val() == '') {
        flag = false;
        regInputError('cardinalSymptom', 'healthms-ask-cardinal-symptom-err', true);
        $("#cardinalSymptom").focus();
    } else if ($('#sickTime').val() == '') {
        flag = false;
        regInputError('sickTime', 'healthms-ask-sick-time-err', true);
        $("#sickTime").focus();
    } else if ($('#lipColor').val() == '') {
        flag = false;
        regInputError('lipColor', 'healthms-ask-lip-color-err', true);
        $("#lipColor").focus();
    } else if ($('#bodyFeel').val() == '') {
        flag = false;
        regInputError('bodyFeel', 'healthms-ask-body-feel-err', true);
        $("#bodyFeel").focus();
    } else if ($('#sweatingCondition').val() == '') {
        flag = false;
        regInputError('sweatingCondition', 'healthms-ask-sweating-condition-err', true);
        $("#sweatingCondition").focus();
    } else if ($('#drinkingCondition').val() == '') {
        flag = false;
        regInputError('drinkingCondition', 'healthms-ask-drinking-condition-err', true);
        $("#drinkingCondition").focus();
    } else if ($('#shitCondition').val() == '') {
        flag = false;
        regInputError('shitCondition', 'healthms-ask-shit-condition-err', true);
        $("#shitCondition").focus();
    } else if ($('#urineCondition').val() == '') {
        flag = false;
        regInputError('urineCondition', 'healthms-ask-urine-condition-err', true);
        $("#urineCondition").focus();
    } else if ($('#spiritSleepCondition').val() == '') {
        flag = false;
        regInputError('spiritSleepCondition', 'healthms-ask-spirit-sleep-condition-err', true);
        $("#spiritSleepCondition").focus();
    } else if ($('#moodCondition').val() == '') {
        flag = false;
        regInputError('moodCondition', 'healthms-ask-mood-condition-err', true);
        $("#moodCondition").focus();
    } else if ($('#tonguePulseCondition').val() == '') {
        flag = false;
        regInputError('tonguePulseCondition', 'healthms-ask-tongue-pulse-condition-err', true);
        $("#tonguePulseCondition").focus();
    } else if ($("#pubesCondition").length > 0) {
        if ($('#pubesCondition').val() == '') {
            flag = false;
            regInputError('pubesCondition', 'healthms-ask-pubes-condition-err', true);
            $("#pubesCondition").focus();
        }
    } else if ($('#briefHistory').val() == '') {
        flag = false;
        regInputError('briefHistory', 'healthms-ask-brief-history-err', true);
        $("#briefHistory").focus();
    };
    if (flag){
        $("#askForm").submit();
    };
};

function regInputError(id, cla, error) {
    if (error) {
        $("#" + id).parents().filter(".form-group").removeClass('has-success has-feedback');
        $("#" + id).parents().filter(".form-group").addClass('has-error has-feedback');
        $("." + cla).remove();
        $("#" + id).after('<span class="' + cla + ' glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span><span class="' + cla + ' sr-only">(error)</span>');
        $("#" + id + "EMsg").html('对不起，您还未填写此字段！');
    } else {
        $("#" + id).parents().filter(".form-group").removeClass('has-error has-feedback');
        $("#" + id).parents().filter(".form-group").addClass('has-success has-feedback');
        $("." + cla).remove();
        $("#" + id).after('<span class="' + cla + ' glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span><span class="' + cla + ' sr-only">(success)</span>');
        $("#" + id + "EMsg").html('');
    }
}
