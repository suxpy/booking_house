// var sd=0
// var ed=0
// var amount=0
// var days=0
// var price=0
function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function myBooking(){
    var begin_date = $('#start-date').val()
    var end_date = $('#end-date').val()
    $.ajax({
        url: '/house/booking/',
        data: {'begin_date': begin_date, 'end_date': end_date, 'amount': amount, 'days': days, 'price':price},
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            if (data.code == '200') {
                location.href='/user/my_orders/'
            }
        },
        error: function (data) {
            alert('注册失败')
        },
    })
}


$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            sd = new Date(startDate);
            ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            price = $(".house-text>p>span").html();
            amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

})
