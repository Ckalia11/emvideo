

const loginSubmit = document.querySelector('#login-form');
const loginFeedback = document.querySelector('.invalid-login');

// const messages = document.querySelector('.messages');
loginSubmit.addEventListener('submit', (e) => {
    console.log('e', e);
    e.preventDefault();
    const usernameOrEmailVal = e.target.elements.username_or_email.value;
    const passwordVal = e.target.elements.password.value;

    loginFeedback.style.display = 'none';

    if (usernameOrEmailVal.length > 0 && passwordVal.length > 0) {
        fetch('validate_login/', {
            body: JSON.stringify({username_or_email : usernameOrEmailVal, password: passwordVal}),
            method: "POST",
        })        
        .then(response => response.json())
        .then(data => {
            if (!(data.login_valid)) {
                loginFeedback.style.display = 'block';
                loginFeedback.innerHTML = `<p>Username or password is incorrect</p>`;
            }
            else {
                window.location.href = '/videos/';
            }
        });
    }

    else {
        loginFeedback.style.display = 'block';
        loginFeedback.innerHTML = `<p>Please enter a username and password</p>`;
    }
})
