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

// load friendship requests
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

// load friends
$.ajax({
    method: "GET",
    url: "/user/friend?action=v&me="+uid,
}).done(function(msg) {
    var data = $.parseJSON(msg)['data'];
    $.each(data, function(k, v) {
        var id = v['uid'];
        var name = v['name'];
        var st = '<span>'+name+'</span><button onclick="friend_delete('+id.toString()+')" style="margin-left:30px;">删除</button><br><br>'
        $('#friend-list').append(st);
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

function friend_delete (init_user) {
    var recv_user = uid;
    $.ajax({
        method: "POST",
        url: "/user/friend?action=del",
        data: {'init_user': init_user, 'recv_user': recv_user}
    }).done(function(msg) {
        location.reload();
    });
}

$.ajax({
    method: "GET",
    url: "/user/"+uid+"?action=n"
}).done(function(msg) {
    var data = $.parseJSON(msg)['data'];
    var temp = [];
    var st_reply = '';
    $.each(data, function(k, v) {
        var event_type = v['event_type'];
        var event_text = v['event_text'];
        var target_text = v['target_text'];
        var owner = v['owner'];
        var user = v['user'];

        var type;
        if (event_type == 'LIKE') {
            type = '赞了';
        } else if (event_type == 'Event') {
            type = '回复了';
        }

        st_reply += `<div class="comment-box"><h2>`+user+`</h2>`+type+`<h2>`+owner+`</h2></div>`;
        $('#notif').append(st_reply);
    });
});