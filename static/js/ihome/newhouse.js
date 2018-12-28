function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.ajax({
        url: '/user/areas_facility/',
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            if (data.code == '200') {
                for ( var i=0; i<data.area_json.length; i++) {
                    var area_str = '<option value="' + data.area_json[i].id + '">' + data.area_json[i].name + '</option>'
                    $('#area-id').append(area_str)
                }
                for(var j=0; j<data.facility_json.length; j++){
                    var facility_str = '<li><div class="checkbox"><label>'
                    facility_str += '<input type="checkbox" name="facility" value="' + data.facility_json[j].id + '">' + data.facility_json[j].name
                    facility_str += '</label></div></li>'

                    $('.house-facility-list').append(facility_str)
                }

            }
        },
        error: function (data) {
            alert('注册失败')
        },
    })
    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/newhouse/',
            type:'POST',
            dataType:'json',
            success:function(data){
                if(data.code == '200'){
                    $('#form-house-image').show()
                    $('#form-house-info').hide()
                    $('#house-id').val(data.house_id)
                }
            },
            error:function(data){
                alert('失败')
            }
        });
    });
      $('#form-house-image').submit(function(e){
        e.preventDefault()
        $(this).ajaxSubmit({
            url:'/user/newhouse/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                if(data.code == '200'){
                    for(var x=0; x<data.images.length; x++){
                        var img_src = '<img src="/static/media/' + data.images[x]+ '">'
                        $('.house-image-cons').append(img_src)
                    }
                }
            },
            error:function(data){
                alert('请求失败')
            }
        })
    });

})
