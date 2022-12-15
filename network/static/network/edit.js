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

function likeHandler(id) {
    // Set like icon handler
    let iconHandler = document.querySelector(`#icon${id}`);
    let countHandler = document.querySelector(`#likenum${id}`);
    // Update likes by calling like_handler function
    fetch('/like_handler', {
        method: 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(response => {
        if (response.status === 200) {
            // Toggle like icon
            iconHandler.className = (iconHandler.className == "fa fa-heart") ? "fa fa-heart-o" : "fa fa-heart"
            // Update like count
            countHandler.innerHTML = response.likecount;
            setTimeout(function() {alert("Likes successfully updated!")}, 500);
        } else {
            console.log("No response");
        }
    });
}

function followHandler(profile_id) {
    // Set button handler
    let buttonHandler = document.querySelector('#follow');
    // Update followers by calling follow_handler function
    fetch('/follow_handler', {
        method: 'POST',
        body: JSON.stringify({
            profile_id: profile_id
        })
    })
    .then(response => response.json())
    .then(response => {
        if (response.status === 200) {
            // Toggle button
            buttonHandler.innerText = (buttonHandler.innerText == "Follow") ? "Unfollow" : "Follow";
            // Message on following
            setTimeout(function() {alert(`Now you follow ${response.profile}!`)}, 500);
        } else {
            console.log('No response');
        }
    })
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button.btn-dark').forEach(button => {
        button.onclick = function() {
            showEditForm(parseInt(this.dataset.id));
        }
    })
})