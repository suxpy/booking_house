function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var url = location.search
    $(".book-house").show();
    $.get('/house/house_detail/' + url.split('=')[1] + '/', function(data){
        for(var i=0; i<data.house[0]['images'].length; i++){
            var image = '<li class="swiper-slide"><img src="/static/images/' + data.house[0]['images'][i] + '"></li>'
            $('.swiper-wrapper').append(image)
        }
        $('.house-price').html('￥<span>' + data.house[0].price+ '</span>/晚')
        if (data.make_order) {
        }else {
            $('.book-house').hide()
        }
        // attr('text', '￥<span>' + data.house[0]['price']+ '</span>/晚')
        //下面这个不行

        var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    })


})