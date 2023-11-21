document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  // Event listeners for inbox, sent, archived, and compose buttons
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox when the DOM is loaded
  load_mailbox("inbox");

  // Post method for sending emails
  document
    .getElementById("compose-form")
    .addEventListener("submit", ($event) => {
      sendEmail($event);
    });
});

function compose_email() {
  // Show compose view and hide other views
  // Clear out fields when composing a new email
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

// Function to load mailbox (inbox, sent, archived)
function load_mailbox(mailbox) {
  // Show the selected mailbox and hide other views
  // Show the mailbox name (Inbox, Sent, Archive)
  const emailsView = document.querySelector("#emails-view");
  emailsView.style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  emailsView.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // Fetch emails based on the selected mailbox and display them
  const inbox = document.getElementById("emails-view");
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Display fetched emails
      console.log(emails);

      emails.forEach((element) => {
        // Create email elements based on mailbox type (inbox/sent)
        const email = document.createElement("div");
        if (mailbox === "inbox") {
          // Display inbox emails with sender, subject, and timestamp
          email.innerHTML = `<p class='sender-recipient'>${element.sender}</p>
          <p class='subject'>${element.subject}</p>
          <p class='timestamp'>${element.timestamp}</p>`;
          if (element.read === true) {
            email.style.backgroundColor = "gray";
          }
        } else {
          // Display sent emails with recipients, subject, and timestamp
          email.innerHTML = `<p class='sender-recipient'>${element.recipients}</p>
          <p class='subject'>${element.subject}</p>
          <p class='timestamp'>${element.timestamp}</p>`;
        }

        // Event listener for email detail view and marking as read (for inbox)
        email.addEventListener("click", () => {
          detailEmail(element.id);

          // Update read status
          fetch(`/emails/${element.id}`, {
            method: "PUT",
            body: JSON.stringify({
              read: true,
            }),
          });
        });

        // Add class and append email elements
        email.classList.add("single-email");
        inbox.appendChild(email);
      });
    });
}

// Function to send an email
function sendEmail($event) {
  $event.preventDefault();
  const recipients = document.querySelector("#compose-recipients");
  const subject = document.querySelector("#compose-subject");
  const body = document.querySelector("#compose-body");

  // Post method to send the email
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients.value,
      subject: subject.value,
      body: body.value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      // Log the result and load sent mailbox
      console.log(result);
      load_mailbox("sent");
    });
}

// Function to display email details
function detailEmail(email_id) {
  const idNum = email_id;
  const container = document.getElementById("emails-view");

  fetch(`/emails/${idNum}`)
    .then((response) => response.json())
    .then((email) => {
      // Log the fetched email
      console.log(email);

      // Create email detail elements and set 'Archive'/'Unarchive' button text
      const mailcontainer = document.createElement("div");
      let textArchived = "";
      if (email.archived === true) {
        textArchived = "Unarchive";
      } else {
        textArchived = "Archive";
      }

      mailcontainer.innerHTML = `<p><strong>From:</strong>${email.sender}</p>
      <p><strong>To:</strong>${email.recipients}</p>
      <p><strong>Subject:</strong>${email.subject}</p>
      <p><strong>date:</strong>${email.timestamp}</p>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <button class="btn btn-sm btn-outline-primary" id="put-archived">${textArchived}</button>
      <hr>
      <p>${email.body}</p>`;

      // Clear the container and display the email details
      container.innerHTML = "";
      container.appendChild(mailcontainer);

      // Event listener for reply button to compose a reply email
      const replyBTN = document.getElementById("reply");
      replyBTN.addEventListener("click", () => {
        // Fetch email details to create a reply
        fetch(`/emails/${email_id}`)
          .then((response) => response.json())
          .then((email) => {
            // Log the fetched email
            console.log(email);

            // Show compose view, hide other views, and populate fields for reply
            document.querySelector("#emails-view").style.display = "none";
            document.querySelector("#compose-view").style.display = "block";
            document.querySelector(
              "#compose-recipients"
            ).value = `${email.sender}`;
            document.querySelector(
              "#compose-subject"
            ).value = `Re:${email.subject}`;
            document.querySelector(
              "#compose-body"
            ).value = `${email.timestamp} ${email.sender} wrote: ${email.body}`;
          });
      });

      // Event listener for 'Archive'/'Unarchive' button
      const archived = document.querySelector("#put-archived");
      archived.archived.innerHTML = archived.addEventListener(
        "click",
        ($event) => {
          if ($event.target.innerHTML === "Archive") {
            $event.target.innerText = "Unarchive";
            fetch(`/emails/${email_id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: true,
              }),
            });
          } else {
            $event.target.innerText = "Archive";
            fetch(`/emails/${email_id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: false,
              }),
            });
          }
        }
      );
    });
}
