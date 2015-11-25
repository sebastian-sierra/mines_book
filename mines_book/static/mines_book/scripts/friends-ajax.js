/**
 * Created by sebastian on 11/9/15.
 */
function onLoadFriendsAjax() {
    // listener for 'add friend' icon
    $('#add_friend_a').click(addFriend)
    // listener for 'remove friend' icon
    $('#delete_friend_a').click(removeFriend)
}

function addFriend() {
    var friend_username = $('#username').data('username')
    $.ajax({
        url: "/students/" + friend_username + "/friend", // the endpoint
        type: "PUT", // http method
        success: function (response) {
            window.location.replace("/students/" + friend_username)
        }
    })
}

function removeFriend() {
    var friend_username = $('#username').data('username')
    $.ajax({
        url: "/students/" + friend_username + "/friend", // the endpoint
        type: "DELETE", // http method
        success: function (response) {
            window.location.replace("/students/" + friend_username)
        }
    })
}