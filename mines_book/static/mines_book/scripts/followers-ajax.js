/**
 * Created by sebastian on 11/9/15.
 */
function onLoadFollowersAjax() {
    // listener for 'follow group' icon
    $('#follow_group_a').click(followGroup)
    // listener for 'unfollow group' icon
    $('#unfollow_group_a').click(unfollowGroup)
    // listener for 'leave group' icon
    $('#leave_group_a').click(leaveGroup)
}

function followGroup() {
    var group_id = $('#group_id').data('group_id')
    $.ajax({
        url: "/groups/" + group_id + "/follow", // the endpoint
        type: "PUT", // http method
        success: function (response) {
            window.location.replace("/groups/" + group_id)
        }
    })
}

function unfollowGroup() {
    var group_id = $('#group_id').data('group_id')
    $.ajax({
        url: "/groups/" + group_id + "/follow", // the endpoint
        type: "DELETE", // http method
        success: function (response) {
            window.location.replace("/groups/" + group_id)
        }
    })
}

function leaveGroup() {
    var group_id = $('#group_id').data('group_id')
    $.ajax({
        url: "/groups/" + group_id + "/leave", // the endpoint
        type: "DELETE", // http method
        success: function (response) {
            window.location.replace("/groups/" + group_id)
        }
    })
}