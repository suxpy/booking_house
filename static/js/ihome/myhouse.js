$(document).ready(function(){
    show()
})

function show() {
    $.get('/user/show_myhouse/',function (data) {
        $(".auth-warn").show();
        if (data.id_name){
            $(".auth-warn").hide();
            $(".new-house").show();
            for(var i=0; i<data.houses_list.length; i++){
                var house_li = ''
                house_li += '<li><a href="/house/detail/?house_id=' + data.houses_list[i].id + '"><div class="house-title">'
                house_li += '<h3>房屋ID:'+ data.houses_list[i].id +' —— ' + data.houses_list[i].title + '</h3></div>'
                house_li += '<div class="house-content">'
                house_li += '<img src="/static/media/' + data.houses_list[i].image + '" alt="">'
                house_li += '<div class="house-text"><ul>'
                house_li += '<li>位于：' + data.houses_list[i].area + '</li>'
                house_li += '<li>价格：￥' + data.houses_list[i].price + '/晚</li>'
                house_li += '<li>发布时间：' + data.houses_list[i].create_time + '</li>'
                house_li += '</ul></div></div></a></li>'
                $('#houses-list').append(house_li)
            }
        }


    })


}