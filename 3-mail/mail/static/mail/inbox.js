document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
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

  // By default, load the inbox
  load_mailbox("inbox");

  // Post method
  document
    .getElementById("compose-form")
    .addEventListener("submit", ($event) => {
      sendEmail($event);
    });
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

// Request inbox, sent and archived
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // Show all the emails
  const inbox = document.getElementById("emails-view");

  // API to get all the emails
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
      console.log(emails);

      emails.forEach((element) => {
        const email = document.createElement("div");
        if (mailbox === "inbox") {
          email.innerHTML = `<p class='sender-recipient'>${element.sender}</p>
          <p class='subject'>${element.subject}</p>
          <p class='timestamp'>${element.timestamp}</p>`;
          if (element.read === true) {
            email.style.backgroundColor = "gray";
          }
        } else {
          email.innerHTML = `<p class='sender-recipient'>${element.recipients}</p>
          <p class='subject'>${element.subject}</p>
          <p class='timestamp'>${element.timestamp}</p>`;
        }
        email.addEventListener("click", () => {
          detailEmail(element.id);

          // Update read
          fetch(`/emails/${element.id}`, {
            method: "PUT",
            body: JSON.stringify({
              read: true,
            }),
          });
        });
        email.classList.add("single-email");
        inbox.appendChild(email);
      });
    });
}

// Send Email
function sendEmail($event) {
  $event.preventDefault();
  const recipients = document.querySelector("#compose-recipients");
  const subject = document.querySelector("#compose-subject");
  const body = document.querySelector("#compose-body");

  // POST method
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
      // Print result
      console.log(result);
      load_mailbox("sent");
    });
}

function detailEmail(email_id) {
  const idNum = email_id;
  const container = document.getElementById("emails-view");

  fetch(`/emails/${idNum}`)
    .then((response) => response.json())
    .then((email) => {
      // Print email
      console.log(email);

      const mailcontainer = document.createElement("div");
      mailcontainer.innerHTML = `<p><strong>From:</strong>${email.sender}</p>
      <p><strong>To:</strong>${email.recipients}</p>
      <p><strong>Subject:</strong>${email.subject}</p>
      <p><strong>date:</strong>${email.timestamp}</p>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <hr>
      <p>${email.body}</p>`;

      container.innerHTML = "";
      container.appendChild(mailcontainer);

      const replyBTN = document.getElementById("reply");
      replyBTN.addEventListener("click", () => {
        fetch(`/emails/${email_id}`)
          .then((response) => response.json())
          .then((email) => {
            // Print email
            console.log(email);

            // Show compose view and hide other views
            document.querySelector("#emails-view").style.display = "none";
            document.querySelector("#compose-view").style.display = "block";

            // Clear out composition fields
            document.querySelector(
              "#compose-recipients"
            ).value = `${email.sender}`;
            document.querySelector(
              "#compose-subject"
            ).value = `Re:${email.subject}`;
            document.querySelector(
              "#compose-body"
            ).value = `${email.timestamp} ${email.sender}wrote: ${email.body}`;
          });
      });
    });
}
