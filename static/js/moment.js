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

