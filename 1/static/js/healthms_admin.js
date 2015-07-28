$(document).ready(function() {
    $(".navmenu").click(function() {
        $(this).children("ul").slideToggle();
    });
    $("#doctorListTyp").click(function() {
        if ($("#doctorListNowTyp").val() != $(this).val()) {
            $("#userIframe").attr("src", doctorUrl + "?doctorListTyp=" + $(this).val());
            $("#doctorListNowTyp").val($(this).val());
        };
    });
});

function doctorCheckReason(result) {
    $("#doctorCheckResultContainer").slideDown(300); 
    if (result) {
        $("#doctorCheckResultWord").val("审核通过");
    } else {
        $("#doctorCheckResultWord").val("审核未通过");
    };
    $("#doctorCheckResult").val(result);
    setTimeout("$('html,body').animate({scrollTop:$('#doctorCheckResultWord').offset().top}, 500);", 300);
};

function addLink(url) {
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {
            'friendLinkTitle': $('#addFriendLinkTitle').val(),
            'friendLinkUrl': $('#addFriendLinkUrl').val(),
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            if (data == 'success') {
                    location.reload();
            } else{
                    alert("对不起，后台数据错误！");
            };
        }
    });
};

function editLink(url, id) {
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: {
            'friendLinkId': id,
            'friendLinkTitle': $('#editFriendLinkTitle'+id).val(),
            'friendLinkUrl': $('#editFriendLinkUrl'+id).val(),
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        },
        success: function(data, textStatus){
            if (data == 'success') {
                    location.reload();
            } else{
                    alert("对不起，后台数据错误！");
            };
        }
    });
};

function delLink(url, id) {
    var r=confirm("您确定要删除此链接吗？")
    if (r==true) {
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {
                'friendLinkId': id,
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            },
            success: function(data, textStatus){
                if (data == 'success') {
                    location.reload();
                } else{
                    alert("对不起，后台数据错误！");
                };
            }
        });
    };  
};

function delInfo(url, id) {
    var r=confirm("您确定要删除吗？")
    if (r==true) {
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {
                'infoId': id,
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            },
            success: function(data, textStatus){
                if (data == 'success') {
                    location.reload();
                } else{
                    alert("对不起，后台数据错误！");
                };
            }
        });
    };  
};

function delCarousel(url, id) {
    var r=confirm("您确定要删除吗？")
    if (r==true) {
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {
                'imgId': id,
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            },
            success: function(data, textStatus){
                if (data == 'success') {
                    location.reload();
                } else{
                    alert("对不起，后台数据错误！");
                };
            }
        });
    };  
};