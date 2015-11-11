// Executes the 'onLoad' function after loading the page
$(onLoadUserNav)



function onLoadUserNav() {
    $('#feed').click(showUserFeed)
    $('#friends').click(showFriends)
    $('#joined_groups').click(showJoinedGroups)
    $('#edit_user_modal').modal()
    $('#edit_user_a').click(showEditUserModal)
    $('#create_user_a').click(showCreateUserModal)
    $('#create_user_modal').modal()
    onLoadFriendsAjax()
}

function showUserFeed() {
    $('#user_menu a').removeClass('active')
    $('#feed').addClass('active')

    var student_id = $('#username').data('username')

    $.get('/students/'+student_id+'/feed/', function(response) {
        $('#user_content').html(response)
    })

}

function showFriends() {
    $('#user_menu a').removeClass('active')
    $('#friends').addClass('active')

    var student_id = $('#username').data('username')

    $.get('/students/'+student_id+'/friends/', function(response) {
        $('#user_content').html(response)
    })

}

function showJoinedGroups() {
    $('#user_menu a').removeClass('active')
    $('#joined_groups').addClass('active')

    var student_id = $('#username').data('username')

    $.get('/students/'+student_id+'/joined_groups/', function(response) {
        $('#user_content').html(response)
        $('.create_group').click(showNewGroupModal)
        $('.edit_group').click(editGroup)
        $('.ui.modal').modal()

        $('.ui.form')
            .form({
                fields: {
                    name     : 'empty',
                    description   : 'empty',
                    profile_pic : 'empty'
                }
            })

        $('.ui.fluid.search.dropdown')
            .dropdown({
                apiSettings: {
                    url: '/search_students_usernames/{query}/'
                }
            })

    })


}

function showNewGroupModal() {
    $('#create_group_modal').modal('show')
}

function showCreateUserModal() {
    $('#create_user_modal').modal('show')
}

function showEditUserModal() {
    $('#edit_user_modal').modal('show')
}

function editGroup() {
    var group_id = $(this).data('id')
    $.get('/groups/'+group_id+'/edit/', function(response) {
        $('#create_group_modal').after(response)

        $('#edit_group_modal').modal()

        $('#edit_group_form')
            .form({
                fields: {
                    name     : 'empty',
                    description   : 'empty'
                }
            })

        $('#edit_group_dropdown')
            .dropdown({
                apiSettings: {
                    url: '/search_students_not_in_group/'+group_id+'/{query}/'
                }
            })

        $('#edit_group_modal').modal('show')
    })

}