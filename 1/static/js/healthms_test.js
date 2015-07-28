$(document).ready(function(){
    // 当点击开始按钮时显示测试表格
    $('#testStartBtn').click(function(){
        testTableBtnChange("healthms-test-start", "healthms-test-table1");
    }); 
});

// 提交按钮
function testBtn (currentNum, sumNum) {
    // 若总组数和当前不同组数不同时显示下一个 table，否则提交表单
    if (currentNum != sumNum) {
        testTableBtnChange("healthms-test-table"+currentNum, "healthms-test-table"+(Number(currentNum)+1));
    } else {
        $('#patientTest').submit();
    };
    return false;
}

// 将 table1 隐藏，Table2 显示
function testTableBtnChange(table1, table2) {
    $('.' + table1).addClass('hidden');
    $('.' + table2).removeClass('hidden');
}
