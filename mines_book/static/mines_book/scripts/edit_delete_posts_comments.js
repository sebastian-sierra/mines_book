$(onLoadEditDelete)

function onLoadEditDelete(){

    $('.delete.icon.post').on('click', function(){
        var post_id = this.id
        console.log(post_id) // sanity check
        delete_post(post_id)
    })

    $('.delete.icon.comment').on('click', function(){
        var comment_id = this.id
        console.log(comment_id) // sanity check
        delete_comment(comment_id)
    })
}

function delete_post(post_primary_key){
    if (confirm('Are you sure you want to remove this post?')==true){
        $.ajax({
            url : "/delete_post/", // the endpoint
            type : "DELETE", // http method
            data : { postpk : post_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
              $('#post-'+post_primary_key).hide(); // hide the post on success
              console.log("post deletion successful");
            }
        });
    } else {
        return false;
    }
};

function delete_comment(comment_primary_key){
    if (confirm('Are you sure you want to remove this comment?')==true){
        $.ajax({
            url : "/delete_comment/", // the endpoint
            type : "DELETE", // http method
            data : { commentpk : comment_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the comment
              $('#comment-'+comment_primary_key).hide(); // hide the comment on success
              console.log("comment deletion successful");
            }
        });
    } else {
        return false;
    }
};
