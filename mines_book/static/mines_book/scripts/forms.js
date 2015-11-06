$(onLoad)

function onLoad(){
    // Submit post on submit
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post()
    })

    // Submit comment on submit
    $('#comment-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_comment()
    })
}

// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    var user_id = $('#username').data('username')
    $.ajax({
        url : "/students/" + user_id + "/new_post/", // the endpoint
        type : "POST", // http method
        data : { content : $('#id_content').val() }, // data sent with the post request

        // handle a successful response
        success : function(html_response) {
            $('#new_post_form').after(html_response)
        }
    });
};

// AJAX for commenting
function create_comment() {
    console.log("create comment is working!") // sanity check
    var post_id = $('#postid').data('postid')
    $.ajax({
        url : "/new_comment/" + post_id + "/", // the endpoint
        type : "POST", // http method
        data : { content : $("#id_content").val() }, // data sent with the post request

        // handle a successful response
        success : function(html_response) {
            $('#new_comment_form').after(html_response)
        }
    });
};

// **** Everything below here is for crsf verification *****

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});