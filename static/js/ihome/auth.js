function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function confirm() {
     $.get('/user/confirm/', function (data){
        if(data.code == '200'){
                if(data.real_name){
                    $('.btn-success').hide()
                    $('#real-name').val(data.real_name).attr('disabled', 'disabled')
                    $('#id-card').val(data.id_card).attr('disabled', 'disabled')
                }
        }
     })
}

$(document).ready(function() {
    confirm()
    $("#form-auth").submit(function (e) {
        e.preventDefault()
        var real_name = $('#real-name').val()
        var id_card = $('#id-card').val()
        $.ajax({
            url: '/user/auth/',
            data: {'real_name': real_name, 'id_card': id_card},
            dataType: 'json',
            type: 'POST',
            success: function (data) {
                if (data.code == '200') {
                    alert('认证成功')
                }
                if (data.code == '500') {
                    alert('姓名或身份证不符合格式')
                }
            },
            error: function (data) {
                alert('注册失败')
            },
        })
    })
})