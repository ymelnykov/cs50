// Open Login webpage
function logIn() {
    window.location.href = 'login';
}

// Giveaway (add to)/(remove from ) collection
function collectHandler(id) {
    // If user is anonymous, log in
    if (userIsAnonymous) {logIn();}
    // Select Collect Button
    const collectButton = document.querySelectorAll(`#collectButton${id}`);
    const sign = document.querySelectorAll(`#sign${id}`);
    // Select number of collectors
    const collectorCount1 = document.querySelector(`#collected${id}`);
    const collectorCount2 = document.querySelector('#givCollected');
    // Request database
    fetch('/collect', {
        method: 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response=> response.json())
    .then(response => {
        // Toggle Collect Button
        if (collectButton[0].title == 'Remove From Collection'){
            collectButton.forEach(btn => {
            btn.setAttribute('aria-label', 'Add To Collection');
            btn.title = 'Add To Collection';
            btn.className = 'btn btn-outline-secondary position-relative';})
            sign.forEach(s =>{
            s.innerText = '+';})
            setTimeout(function() {alert("Removed from collection successfully!")}, 500);
        } else {
            collectButton.forEach(btn => {
            btn.setAttribute('aria-label', 'Remove From Collection');
            btn.title = 'Remove From Collection';
            btn.className = 'btn btn-secondary position-relative';})
            sign.forEach(s =>{
                s.innerText = '-';})
                setTimeout(function() {alert("Added to collection successfully!")}, 500);
        }
        // Change number of collectors shown
        collectorCount1.innerText = response.count;
        collectorCount2.innerText = response.count;
    })
}

// Process expired giveaways
function processExpired() {
    // Get current date
    const today = new Date();
    // Select and enlist all Expiry Date elements
    const expiryDates = Array.from(document.querySelectorAll('[id^="expiry_date"]'))
    expiryDates.forEach(expiryDate => {
        // Set expiry date ending on the last second of it
        var date = expiryDate.innerText + ' 23:59:59';
        // If Expiry Date is specified..
        if (date != 'N/A') {
            date = new Date(date);
            // ...and less than current date 
            if (today > date) {
                // Get Giveaway id
                let id = expiryDate.getAttribute('id').replace('expiry_date', '');
                // Make Giveaway card image black and white
                document.querySelector(`#image${id}`).classList.add('bw');
                // Make Giveaway card title black and white
                document.querySelector(`#title_container${id}`).classList.add('bw');
                // Apply Expired Stamp
                document.querySelector(`#expired${id}`).classList.add('d-block');
                // Disable all Giveaway card buttons
                document.querySelector(`#view${id}`).classList.add('disabled');
                document.querySelector(`#view${id}`).removeAttribute('href');
                document.querySelector(`#collectButton${id}`).classList.add('disabled');
            }
        }
    })
}

// Correct pagination links by adding current query parameters, if any
function correctPageLinks() {
    // Get current URL
    const currentURL = window.location.href;
    // Check if any query parameters are provided via URL
    if (currentURL.includes('?')) {
        // Select and enlist all pagination links
        const pageLinks = Array.from(document.querySelectorAll('.page-link'));
        // Iterate over all pagination links
        pageLinks.forEach(pageLink => {
            // Get href attribute of current link
            var rawLink = pageLink.getAttribute('href');
            // If it equals #, leave unchanged
            if (rawLink === '#') {
                pageLink.setAttribute('href', rawLink)
            // else if current URL includes page parameter,    
            } else if (currentURL.includes('page')) {
                // cut it out and add the rest to the current link href
                pageLink.setAttribute('href', (currentURL.slice(0, currentURL.lastIndexOf('page')) + rawLink.replace('?', '')))
            } else {
                // add current URL to the current link href
                pageLink.setAttribute('href', (currentURL + rawLink.replace('?', '&')))
            }
        })
    }
}

// Show Giveaway View modal
function viewGiveaway(id) {
    // Get all Giveaway View modal elements
    const title = document.getElementById('givTitle');
    const image = document.getElementById('givImage');
    const worth = document.getElementById('givWorth');
    const type = document.getElementById('givType');
    const platforms = document.getElementById('givPlatforms');
    const description = document.getElementById('givDescription');
    const instructions = document.getElementById('givInstructions');
    const url = document.getElementById('givUrl');
    const author = document.getElementById('givAuthor');
    const collector = document.getElementById('givCollector');
    const collected = document.getElementById('givCollected');
    const expiryDate = document.getElementById('givExpiryDate');
    // Get available platform icons
    const platformIcons = {'PC': 'windows', 'Steam': 'steam-symbol', 'Itch.io': 'itch-io', 'Battle.net': 'battle-net', 'Playstation': 'playstation', 'Xbox': 'xbox', 'Android': 'google-play', 'iOS': 'apple'}
    const platformsArray = document.getElementById(`platforms${id}`).innerText.split(', ');
    const icons = Object.keys(platformIcons);
    // Populate Giveaway View modal elements with chosen Giveaway card contents
    title.innerText = document.getElementById(`title${id}`).innerText;
    image.src = document.getElementById(`image${id}`).src;
    image.alt = document.getElementById(`image${id}`).alt;
    worth.innerText = document.getElementById(`worth${id}`).innerText;
    type.innerText = document.getElementById(`type${id}`).innerText;
    platforms.innerHTML = '';
    for (let platform of platformsArray) {
        console.log(platform);
        const badge = document.createElement('span');
        badge.className = "badge bg-secondary me-1 mb-1";
        const iconExists = icons.filter(icon => platform.includes(icon));
        console.log(iconExists);
        if (iconExists) {
                badge.innerHTML = `<i class="fab fa-${platformIcons[iconExists[0]]}"></i> ${platform}`;
            } else {
                badge.innerHTML = platform;
        }
        platforms.appendChild(badge);
    }
    description.innerText = document.getElementById(`description${id}`).innerText;
    instructions.innerText = document.getElementById(`instructions${id}`).innerText;
    url.href = document.getElementById(`url${id}`).innerText;
    author.innerText = document.getElementById(`author${id}`).innerText;
    collector.innerHTML = document.getElementById(`collector${id}`).innerHTML;
    collected.innerText = document.getElementById(`collected${id}`).innerText;
    expiryDate.innerText = document.getElementById(`expiry_date${id}`).innerText;
}

// Upon document loading...
document.addEventListener('DOMContentLoaded', function() {
    // ...correct pagination links by adding current query parameters, if any,
    correctPageLinks();
    // process expired giveaways,
    processExpired();
    // show action result message, if any
    actMessage = document.getElementById('actMessage').innerText;
    if (actMessage) {
        setTimeout(function() {alert(actMessage)}, 500);
    }
})