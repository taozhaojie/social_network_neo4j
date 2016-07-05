function getQueryParams() {
    qs = document.location.search;
    qs = qs.split('+').join(' ');
    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

var args = getQueryParams();
var uid = args['me'];

$.ajax({
    method: "GET",
    url: "/user/friend?action=req&me="+uid,
}).done(function(msg) {
    var data = $.parseJSON(msg)['data'];
    $.each(data, function(k, v) {
        var id = v['uid'];
        var name = v['name'];
        var st = '<span>'+name+'</span><button onclick="accept_request('+id.toString()+')" style="margin-left:30px;">接受</button><br><br>'
        $('#friend-req').append(st);
    });

});

$(function(){
    $("#send-text").keyup(function(event){
        if(event.which == 13){
            submit();
        }
    });
});

function submit_request () {
    var text = $('#friend-add-id').val();
    $('#friend-add-id').val('');

    $.ajax({
        method: "POST",
        url: "/user/friend?action=req",
        data: {'init_user': uid, 'recv_user': text}
    }).done(function(msg) {
        location.reload();
    });
}

function accept_request (init_user) {
    var recv_user = uid;
    $.ajax({
        method: "POST",
        url: "/user/friend?action=ack",
        data: {'init_user': init_user, 'recv_user': recv_user}
    }).done(function(msg) {
        location.reload();
    });
}