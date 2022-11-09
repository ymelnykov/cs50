document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // Send email when email form is submitted
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
  
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id, mailbox) {

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // Show email content and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-content-view').style.display = 'block';
      document.querySelector('#compose-view').style.display = 'none';
      
      // Show email content
      document.querySelector('#email-content-view').innerHTML = `
      <div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Timestamp:</strong> ${email.timestamp}</div>
      <hr>
      <div>${email.body}</div>
      <hr>
      `
      // Mark email as read
      if (!email.read) {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }
      // Add Archive and  Reply buttons for Inbox and Archived emails
      if (mailbox != 'sent') {
        // Archive/Unarchive email 
        const archiver = document.createElement('button');
        archiver.innerHTML = email.archived ? "Unarchive" : "Archive";
        archiver.className = "btn btn-sm btn-outline-primary";
        archiver.addEventListener('click', () => {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email.archived
            })
          })
          .then(() => {load_mailbox('inbox')});
        });
        document.querySelector('#email-content-view').append(archiver);

        // Reply to email
        const reply = document.createElement('button');
        reply.innerHTML = "Reply";
        reply.className = "btn btn-sm btn-outline-primary ml-1";
        reply.addEventListener('click', () => {
          compose_email();
          // Prefill composition fields
          document.querySelector('#compose-recipients').value = email.sender;
          let subject = email.subject;
          if (subject.split(" ")[0] != "Re:") {subject = "Re: " + email.subject};
          document.querySelector('#compose-subject').value = subject;
          document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
        });
        document.querySelector('#email-content-view').append(reply);
      }
  });
} 

function send_email(event) {
  // Prevent Inbox from loading by default after Sent mailbox
  event.preventDefault();
  // Get email data from form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  // Send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      //Print result
      console.log(result);
      // Load Sent mailbox
      load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Fetch emails from mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Loop through emails
    emails.forEach(email => {
      const email_div = document.createElement('div');
      email_div.className = email.read ? "row entry read" : "row entry unread";
      email_div.innerHTML = `
      <div class="col-3">${email.sender}</div>
      <div class="col-6">${email.subject}</div>
      <div class="col-3">${email.timestamp}</div>
      `;
      email_div.addEventListener('click', () => {view_email(email.id, mailbox)});
      document.querySelector('#emails-view').append(email_div);
    })
  }); 
}



