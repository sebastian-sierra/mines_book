// Executes the 'onLoad' function after loading the page
$(onLoadGroupNav)


function onLoadGroupNav() {
    $('#group_feed_a').click(showGroupFeed)
    $('#group_members_a').click(showMembers)
    $('#group_followers_a').click(showFollowers)
    $('#edit_group_a').click(showEditGroupModal)
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