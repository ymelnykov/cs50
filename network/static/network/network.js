function showEditForm(id) {
    // Set content and button handlers
    const contentHandler = document.querySelector(`#content${id}`);
    const buttonHandler = document.querySelector(`#btn${id}`);
    // Show edit text area
    contentHandler.innerHTML = `<textarea id="content" rows="3" cols="100">${contentHandler.textContent}</textarea>`
    // Toggle button
    buttonHandler.setAttribute('onclick', `editPost('${id}')`);
    buttonHandler.className = "btn btn-success";
    buttonHandler.innerText = "Save"

}


function editPost(id) {
    // Set content and button handlers
    const contentHandler = document.querySelector(`#content${id}`);
    const buttonHandler = document.querySelector(`#btn${id}`);
    // Get text area content
    const edited = document.querySelector('#content').value;
    // Edit post content by calling Edit function
    fetch('/edit', {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            edited: edited
        })
    })
    .then(response => response.json())
    .then(response => {
        // Show edited post content
        contentHandler.textContent = response.content;
        // Toggle button
        buttonHandler.setAttribute('onclick', `showEditForm('${id}')`);
        buttonHandler.className = "btn btn-dark";
        buttonHandler.innerText = "Edit";
        setTimeout(function() {alert("Post successfully edited!")}, 500);
    })
}


function likeHandler(id) {
    // Set like icon and count handler
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
        // Toggle like icon
        iconHandler.className = (iconHandler.className == "fa fa-heart") ? "fa fa-heart-o" : "fa fa-heart"
        // Update like count
        countHandler.innerText = response.likecount;
        setTimeout(function() {alert("Likes successfully updated!")}, 500);
    });
}


function followHandler(profile_id) {
    // Set button and count handler
    let buttonHandler = document.querySelector('#follow');
    let countHandler = document.querySelector('#followers');
    // Update followers by calling follow_handler function
    fetch('/follow_handler', {
        method: 'POST',
        body: JSON.stringify({
            profile_id: profile_id
        })
    })
    .then(response => response.json())
    .then(response => {
            // Update Followers count
            countHandler.innerText = response.followercount
            // Toggle button and raise an alert
            if (buttonHandler.innerText == "Follow") {
                buttonHandler.innerText = "Unfollow";
                setTimeout(function() {alert(`Now you follow ${response.profilename}!`)}, 500);
            } else {
                buttonHandler.innerText = "Follow";
                setTimeout(function() {alert(`You don't follow ${response.profilename} any more!`)}, 500);
            }
    });
}
