function showEditForm(post_id) {
    // Hide all Edit class divs
    document.querySelectorAll('div.edit').forEach(div => {
        div.style.display = 'none';
    })
    // Show Edit form
    document.querySelector(`#edit${post_id}`).style.display = 'block';
    // Show all posts
    document.querySelectorAll('div.show').forEach(div => {
        div.style.display = 'block';
    })
    // Hide the post to be edited
    document.querySelector(`#show${post_id}`).style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            showEditForm(this.id);
        }
    })
})