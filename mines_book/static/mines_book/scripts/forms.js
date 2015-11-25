$(onLoadForms)

function onLoadForms() {
    // listener for submit button of new post
    $('body').on('submit', '#post-form', function (event) {
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post(this)
    })

    // listener for reply button of new comment
    $('body').on('submit', '.ui.reply.form.comment.form', function (event) {
        event.preventDefault();
        console.log("form submitted!") // sanity check
        var comment_id = this.id
        create_comment(comment_id)
    })

    // listener for close icon of error message
    $('body').on('click', '.message .close', function () {
        $(this)
            .closest('.message')
            .transition('fade')
        ;
    })
}

// AJAX for posting
function create_post(form) {
    console.log("create post is working!") // sanity check
    var recipient_type = $(form).data('recipient_type')
    var url
    if (recipient_type == "group") {
        var group_id = $('#group_id').data('group_id')
        url = "/groups/" + group_id + "/new_post/"
    }
    if (recipient_type == "student") {
        var user_id = $('#username').data('username')
        url = "/students/" + user_id + "/new_post/"
    }
    $.ajax({
        url: url, // the endpoint
        type: "POST", // http method
        data: {content: $('#id_content').val()}, // data sent with the post request

        // handle a successful response
        success: function (html_response) {
            $('#new_post_form').after(html_response)
            $('#id_content').val('')
        },
        // handle unsuccessful response
        error: function (response) {
            console.log(response)
            var message = "<div class=\"ui fluid negative message\">" +
                "<i class=\"close icon\"></i>" +
                "<div class=\"header\">" +
                "Post cannot be empty." +
                "</div>" +
                "</div>"
            $('.ui.cards').before(message)
        }
    });
};

// AJAX for commenting
function create_comment(comment_form_id) {
    console.log("create comment is working!") // sanity check
    var content_id = "#id_comment_content_for_" + comment_form_id
    $.ajax({
        url: "/new_comment/" + comment_form_id + "/", // the endpoint
        type: "POST", // http method
        data: {content: $(content_id).val()}, // data sent with the post request

        // handle a successful response
        success: function (html_response) {
            $('#new_comment_form_for_' + comment_form_id).before(html_response)
            $(content_id).val('')
        },
        // handle unsuccessful response
        error: function (response) {
            console.log(response)
            var message = "<div class=\"ui fluid negative message\">" +
                "<i class=\"close icon\"></i>" +
                "<div class=\"header\">" +
                "Comment cannot be empty." +
                "</div>" +
                "</div>"
            $('.ui.cards').before(message)

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
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});