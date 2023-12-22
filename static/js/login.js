document.addEventListener('DOMContentLoaded', function () {
    const alert_placeholder = document.querySelector('#error_login');
    const login_form = document.querySelector('#login_form');

    login_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const email = login_form['email'].value;
        const password = login_form['password'].value;

        const email_regex = /^[\w\.-]+\@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;

        let email_valid = false;
        let password_valid = false;

        if (email === '' || !email_regex.test(email)) {
            email_valid = false;
            document.querySelector('#login_email').classList.remove('is-valid');
            document.querySelector('#login_email').classList.add('is-invalid');
        } else {
            email_valid = true;
            document.querySelector('#login_email').classList.remove('is-invalid');
            document.querySelector('#login_email').classList.add('is-valid');
        }

        if (password === '') {
            password_valid = false;
            document.querySelector('#login_password').classList.remove('is-valid');
            document.querySelector('#login_password').classList.add('is-invalid');
        } else {
            password_valid = true;
            document.querySelector('#login_password').classList.remove('is-invalid');
            document.querySelector('#login_password').classList.add('is-valid');
        }

        if (email_valid && password_valid) {
            await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password
                }),
            }).then(response => {
                if (response.status === 200 || response.status === 302) {
                    form_alert(
                        'Inicio de sesión exitoso. Redireccionando... <div class="spinner-border spinner-border-sm text-success" role="status" aria-hidden="true"></div>',
                        'success', alert_placeholder
                        )
                    if (response.redirected) {
                        window.setTimeout(function () {
                            window.location.href = response.url;

                        }, 2000);
                    }
                }
                else {
                    form_alert('Usuario o contraseña incorrectos.', 'danger', alert_placeholder);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            });
        }
    });
});
