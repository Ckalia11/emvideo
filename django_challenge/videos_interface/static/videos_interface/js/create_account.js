const username = document.querySelector('#username');
const email = document.querySelector('#email');
const usernameFeedback = document.querySelector('.invalid-username');
const emailFeedback = document.querySelector('.invalid-email');


username.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;

    username.classList.remove("is-invalid");
    usernameFeedback.style.display = "none";

    if (usernameVal.length > 0) {
        fetch('validate_username/', {
            body: JSON.stringify({username : usernameVal}),
            method: "POST",
        })
        .then(response => response.json())
        .then(data => {
            if (data.username_invalid) {
                username.classList.add("is-invalid");
                usernameFeedback.style.display = "block";
                usernameFeedback.innerHTML = `<p>${data.username_invalid}</p>`
            }
        });
    }

});

email.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;

    email.classList.remove("is-invalid");
    emailFeedback.style.display = "none";

    if (emailVal.length > 0) {
        fetch('validate_email/', {
            body: JSON.stringify({email : emailVal}),
            method: "POST",
        })
        .then(response => response.json())
        .then(data => {
            if (data.email_invalid) {
                email.classList.add("is-invalid");
                emailFeedback.style.display = "block";
                emailFeedback.innerHTML = `<p>${data.email_invalid}</p>`
            }
        });
    }

});
