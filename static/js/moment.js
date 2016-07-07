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

$(function(){
    $("#send-text").keyup(function(event){
        if(event.which == 13){
            submit();
        }
    });
});

function submit () {
    var text = $('#send-text').val();
    $('#send-text').val('');

    $.ajax({
        method: "POST",
        url: "/moment/",
        data: {'text': text, 'uid': uid}
    }).done(function(msg) {
        location.reload();
    });
}

// load friends events
$.ajax({
    method: "GET",
    url: "/moment?action=v&me="+uid+"&page="+"0", // do this later
}).done(function(msg) {
    var data = $.parseJSON(msg)['data'];
    $.each(data, function(k, v) {
        var id = v['id'];
        var uid = v['uid'];
        var text = v['text'];
        var time = v['time'];
        var name = v['name'];

        var time_now = Math.floor(Date.now() / 1000);
        var time_pass;
        if ((time_now - time) >= 60) {
            if ((time_now - time) / 60 >= 60) {
                if ((time_now - time) / 60 / 60 >= 24) {
                    time_pass = Math.round((time_now - time) / 60 / 60 / 24).toString() + ' 天前';
                } else {
                    time_pass = Math.round((time_now - time) / 60 / 60).toString() + ' 小时前';
                }

            } else {
                time_pass = Math.round((time_now - time) / 60).toString() + ' 分钟前';
            }

        } else {
            time_pass = Math.round(time_now - time).toString() + ' 秒前';
        }

        // load liked users
        $.ajax({
            method: "GET",
            url: "/moment/"+id+"?action=liked"
        }).done(function(msg) {
            var data = $.parseJSON(msg)['data'];
            var temp = [];
            $.each(data, function(k, v) {
                var name_liked = v['name'];
                temp.push(name_liked);
            });
            if (temp.length > 0) {
                var st_liked = `<div class="like-box">❤ `+temp.join(', ')+`</div>`;
            } else {
                var st_liked = '';
            }

            var st = `  <div class="moment-box">
                            <h1 onclick="view_user(`+uid+`)">`+name+`</h1><br>
                            <p>`+text+`</p><br>
                            <span>`+time_pass+`</span><span onclick="like('`+id+`')">赞</span><span onclick="comment('`+id+`')">评论</span>
                            `+st_liked+`
                        </div>`

            $('#view').append(st);
        });
        
    });

});

function like(moment_id) {
    $.ajax({
        method: "GET",
        url: "/moment/"+moment_id+"?me="+uid+"&action=like"
    }).done(function(msg) {
        location.reload();
    });
}

function comment(moment_id) {
    var text = window.prompt();

    $.ajax({
        method: "POST",
        url: "/moment/"+moment_id,
        data: {'text': text, 'uid': uid}
    }).done(function(msg) {
        location.reload();
    });
}