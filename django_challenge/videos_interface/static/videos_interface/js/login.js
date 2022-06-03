const loginSubmit = document.querySelector('#login-form');
loginSubmit.addEventListener('submit', (e) => {
    e.preventDefault();
    const usernameOrEmailVal = e.target.elements.username_or_email.value;
    const passwordVal = e.target.elements.password.value;
    if (usernameOrEmailVal.length > 0 && passwordVal.length > 0) {
        console.log('eeh')
        fetch('validate_login/', {
            body: JSON.stringify({username_or_email : usernameOrEmailVal, password: passwordVal}),
            method: "POST",
        })
        .then(response => response.json())
        .then(data => {
            if (data.login_invalid) {
                console.log("invlaid", data.login_invalid)
            }
        });
    }
})
