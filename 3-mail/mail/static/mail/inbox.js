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
  let senderOrRecipients = document.createElement("p"); //Sender or recipients
  let subject = document.createElement("p");
  let receivedDate = document.createElement("p");
  let email = document.createElement("div");

  // API to get all the emails
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
      console.log(emails);

      emails.forEach((element) => {
        if (mailbox === "inbox") {
          senderOrRecipients.innerText = element.sender;
          if (element.read === true) {
            email.style.backgroundColor = "gray";
          }
        } else {
          senderOrRecipients.innerText = element.recipients;
        }
        subject.innerText = element.subject;
        receivedDate.innerText = element.timestamp;

        // Style for each element
        email.style.border = "solid 2px black";
        email.style.display = "flex";
        email.style.justifyContent = "space-between";
        email.style.marginLeft = "auto";
        email.style.height = "30px";

        senderOrRecipients.style.fontWeight = "bold";
        receivedDate.style.fontWeight = "600";
        receivedDate.style.color = "#c5baba";
        email.setAttribute("name", `/emails/${element.id}`);
        email.classList.add("single-email");

        // Add elements to inbox
        email.appendChild(senderOrRecipients);
        email.appendChild(subject);
        email.appendChild(receivedDate);
        inbox.appendChild(email);

        // Reset elements
        senderOrRecipients = document.createElement("p"); //Sender or recipients
        subject = document.createElement("p");
        receivedDate = document.createElement("p");
        email = document.createElement("div");
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
      target;
      load_mailbox("sent");
    });
}

// Function to create individual email elements
function createEmailElement(emailData) {
  const senderOrRecipients = document.createElement("p");
  const subject = document.createElement("p");
  const receivedDate = document.createElement("p");
  const emailDiv = document.createElement("div");

  // Set content and styles for each email element
  // ...

  // Add event listener to the email element
  emailDiv.addEventListener("click", () => {
    // Perform actions when an email is clicked
    console.log(emailData); // Access email data for the clicked email
    // Additional logic here...
  });

  return emailDiv;
}

// Function to display emails in the mailbox
function displayEmails(emails, mailbox) {
  const inbox = document.getElementById("emails-view");
  inbox.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  emails.forEach((email) => {
    const emailElement = createEmailElement(email);
    inbox.appendChild(emailElement);
  });
}

// Modify the fetch block in load_mailbox function to use displayEmails
fetch(`/emails/${mailbox}`)
  .then((response) => response.json())
  .then((emails) => {
    // Display emails in the mailbox
    displayEmails(emails, mailbox);
  });

// ... [rest of your code] ...
