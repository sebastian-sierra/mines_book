// Executes the 'onLoad' function after loading the page
$(onLoadGroupNav)


function onLoadGroupNav() {
    // listener for group feed tab
    $('#group_feed_a').click(showGroupFeed)
    // listener for group members tab
    $('#group_members_a').click(showMembers)
    // listener for group followers tab
    $('#group_followers_a').click(showFollowers)
    // listener for 'edit group' icon
    $('#edit_group_a').click(showEditGroupModal)
    $('#id_profile_pic').attr({accept:"image/*"})
    $('#edit_group_modal').modal()
    var group_id = $('#group_id').data('group_id')
    $('#edit_group_form')
        .form({
            fields: {
                name: 'empty',
                description: 'empty'
            }
        })

    $('#edit_group_dropdown')
        .dropdown({
            apiSettings: {
                url: '/search_students_not_in_group/' + group_id + '/{query}'
            }
        })

    $('#edit_group_dropdown_r')
        .dropdown({
            apiSettings: {
                url: '/search_students_in_group/' + group_id + '/{query}'
            }
        })


    onLoadFollowersAjax()
}

function showGroupFeed() {
    $('#group_menu a').removeClass('active')
    $('#group_feed_a').addClass('active')

    var group_id = $('#group_id').data('group_id')

    $.get('/groups/' + group_id + '/feed/', function (response) {
        $('#group_content').html(response)
    })

}

function showMembers() {
    $('#group_menu a').removeClass('active')
    $('#group_members_a').addClass('active')

    var group_id = $('#group_id').data('group_id')

    $.get('/groups/' + group_id + '/members/', function (response) {
        $('#group_content').html(response)
    })

}

function showFollowers() {
    $('#group_menu a').removeClass('active')
    $('#group_followers_a').addClass('active')

    var group_id = $('#group_id').data('group_id')

    $.get('/groups/' + group_id + '/followers/', function (response) {
        $('#group_content').html(response)
    })


}

function showEditGroupModal() {
    $('#edit_group_modal').modal('show')
}