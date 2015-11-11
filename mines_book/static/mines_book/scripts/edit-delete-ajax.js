$(onLoadEditDelete)

function onLoadEditDelete() {

    $('body').on('click', '.delete.icon.post', function () {
        var post_id = this.id
        console.log(post_id) // sanity check
        delete_post(post_id)
    })

    $('body').on('click', '.delete.icon.comment', function () {
        var comment_id = this.id
        console.log(comment_id) // sanity check
        delete_comment(comment_id)
    })

    $('#delete_account_b').on('click', deleteAccount)
    $('body').on('click', '.right.floated.delete.group', deleteGroup)
    $('body').on('click', '#delete_group_b', deleteGroup)

    $('body').on('click', '.edit.icon.post', function () {
        var post_id = this.id
        console.log(post_id) // sanity check
        edit_post(post_id)
    })
    $('body').on('click', '#edit-post-submit', complete_post_edit)

    $('body').on('click', '.edit.icon.comment', function () {
        var comment_id = this.id
        console.log(comment_id) // sanity check
        edit_comment(comment_id)
    })
    $('body').on('click', '#edit-comment-submit', complete_comment_edit)
}

function delete_post(post_primary_key) {
    if (confirm('Are you sure you want to remove this post?') == true) {
        $.ajax({
            url: "/delete_post/", // the endpoint
            type: "DELETE", // http method
            data: {postpk: post_primary_key}, // data sent with the delete request
            success: function (json) {
                // hide the post
                $('#post-' + post_primary_key).hide(); // hide the post on success
                console.log("post deletion successful");
            }
        });
    } else {
        return false;
    }
};

function delete_comment(comment_primary_key) {
    if (confirm('Are you sure you want to remove this comment?') == true) {
        $.ajax({
            url: "/delete_comment/", // the endpoint
            type: "DELETE", // http method
            data: {commentpk: comment_primary_key}, // data sent with the delete request
            success: function (json) {
                // hide the comment
                $('#comment-' + comment_primary_key).hide(); // hide the comment on success
                console.log("comment deletion successful");
            }
        });
    } else {
        return false;
    }
};

function deleteAccount() {
    if (confirm('Are you sure you want to delete your account?') == true) {
        $.ajax({
            url: "/students/delete/", // the endpoint
            type: "DELETE", // http method
            success: function (response) {
                window.location.replace("/login/")
            }
        })
    } else {
        return false;
    }
}

function deleteGroup() {
    var group_id = $(this).data('id')
    if (confirm('Are you sure you want to delete this group?') == true) {
        $.ajax({
            url: "/groups/" + group_id, // the endpoint
            type: "DELETE", // http method
            success: function (response) {
                if ($('#group-' + group_id).length > 0) {
                    $('#group-' + group_id).hide()
                } else {
                    window.location.replace("/groups/")
                }
            }
        })
    } else {
        return false;
    }
}

function edit_post(post_primary_key) {

    $('#post-content-' + post_primary_key).parent().next().hide()
    var replaceHTML =
        "<input name=\"content\" id=\"edit-post-input\" value=\""
        + $('#post-content-' + post_primary_key).get(0).innerHTML
        + "\">" +
        "<button class=\"ui button primary mini\" style=\"margin-left:3%\" id=\"edit-post-submit\" " +
        "data-id=\"" + post_primary_key + "\" type=\"submit\">Submit</button>"
    $('#post-content-' + post_primary_key).replaceWith(replaceHTML)
    console.log("opened post edit successfully");
};

function complete_post_edit() {

    var post_primary_key = $(this).data('id')
    var new_content = $('#edit-post-input').val()
    $.ajax({
        url: "/edit_post/" + post_primary_key + "/", // the endpoint
        type: "PUT", // http method
        data: {content: new_content}, // data sent with the put request
        success: function (json) {
            var replaceHTML = "<p id=\"post-content-" + post_primary_key + "\">" + json['content'] + "</p>"
            $('#edit-post-input').replaceWith(replaceHTML)
            $('#edit-post-submit').replaceWith()
            $('#post-content-' + post_primary_key).parent().next().show()
            console.log("post edit successful");
        }
    });
};

function edit_comment(comment_id) {

    $('#comment-content-' + comment_id).parent().next().hide()
    var replaceHTML =
        "<input name=\"content\" id=\"edit-comment-input\" value=\""
        + $('#comment-content-' + comment_id).get(0).innerHTML
        + "\">" +
        "<button class=\"ui button primary mini\" style=\"margin-left:3%\" id=\"edit-comment-submit\" " +
        "data-id=\"" + comment_id + "\" type=\"submit\">Submit</button>"
    $('#comment-content-' + comment_id).replaceWith(replaceHTML)
    console.log("opened comment edit successfully");
};

function complete_comment_edit() {

    var comment_id = $(this).data('id')
    var new_content = $('#edit-comment-input').val()
    $.ajax({
        url: "/edit_comment/" + comment_id + "/", // the endpoint
        type: "PUT", // http method
        data: {content: new_content}, // data sent with the put request
        success: function (json) {
            var replaceHTML = "<p id=\"comment-content-" + comment_id + "\">" + json['content'] + "</p>"
            $('#edit-comment-input').replaceWith(replaceHTML)
            $('#edit-comment-submit').replaceWith()
            $('#comment-content-' + comment_id).parent().next().show()
            console.log("comment edit successful");
        }
    });
};