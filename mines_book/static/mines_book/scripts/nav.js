// Executes the 'onLoad' function after loading the page
$(onLoad)

function onLoad() {
    $('#feed').click(showFeed)
    $('#friends').click(showFriends)
    $('#joined_groups').click(showJoinedGroups)
}

function showFeed() {
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
    })

}