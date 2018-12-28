function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
     $("#form-avatar").submit(function(e){
         alert('12')
         e.preventDefault()
         $(this).ajaxSubmit({
            url: '/user/change_info/',
            dataType: 'json',
            type: 'PATCH',
            success: function (data) {
                if (data.code == '200') {
                    $('#user-avatar').attr('src', '/static/media/' + data.icon)
                }
            },
            error: function (data) {
                alert('上传失败')
            },
        })
     })
     $("#form-name").submit(function(e){
         e.preventDefault()
         var user_name = $('#user-name').val()
         $.ajax({
            url: '/user/change_info_name/',
            data: {'user_name': user_name},
            dataType: 'json',
            type: 'POST',
            success: function (data) {
                if (data.code == '200') {
                    alert('上传成功')
                }
            },
            error: function (data) {
                alert('上传失败')
            },
        })
     })
})