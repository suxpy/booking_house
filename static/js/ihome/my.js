function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

function center_info() {
    $.get('/user/center_info/', function (data){
        if(data.code == '200'){
            $('#user-name').html(data.user_name)
            $('#user-mobile').html(data.user_phone)
        }
    })
}

$(document).ready(function(){
    center_info()
})