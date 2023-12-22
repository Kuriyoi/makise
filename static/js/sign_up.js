document.addEventListener('DOMContentLoaded', function () {
    const alert_placeholder = document.querySelector('#error_sign_up');
    const sign_up_form = document.querySelector('#sign_up_form');

    sign_up_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        // User
        const name = sign_up_form['name'].value;
        const surname = sign_up_form['surname'].value;
        const email = sign_up_form['email'].value;
        const password_1 = sign_up_form['password_1'].value;
        const password_2 = sign_up_form['password_2'].value;
        const phone_number = sign_up_form['phone_number'].value;

        const name_input = document.querySelector('#sign_up_name');
        const surname_input = document.querySelector('#sign_up_surname');
        const email_input = document.querySelector('#sign_up_email');
        const password_1_input = document.querySelector('#sign_up_password_1');
        const password_2_input = document.querySelector('#sign_up_password_2');
        const phone_number_input = document.querySelector('#sign_up_phone_number');

        const email_regex = /^[\w\.-]+\@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;
        const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[a-zA-Z\d\W_]{8,}$/;
        const phone_number_regex = /^[0-9]{9}$/;
        const zip_code_regex = /^[0-9]{5}$/;

        let name_valid, surname_valid, email_valid, password_1_valid, password_2_valid, phone_number_valid = false;

        // Address
        const address_name = sign_up_form['address_name'].value;
        const address_line = sign_up_form['address_line'].value;
        const town = sign_up_form['town'].value;
        const city = sign_up_form['city'].value;
        const zip_code = sign_up_form['zip_code'].value;

        const address_name_input = document.querySelector('#sign_up_address_name');
        const address_line_input = document.querySelector('#sign_up_address_line');
        const town_input = document.querySelector('#sign_up_town');
        const city_input = document.querySelector('#sign_up_city');
        const zip_code_input = document.querySelector('#sign_up_zip_code');

        let address_name_valid, address_line_valid, town_valid, city_valid, zip_code_valid = false;

        const terms_and_conditions = document.querySelector('#terms_and_conditions');

        if (name === '') {
            name_valid = false;
            name_input.classList.remove('is-valid');
            name_input.classList.add('is-invalid');
        } else {
            name_valid = true;
            name_input.classList.remove('is-invalid');
            name_input.classList.add('is-valid');
        }

        if (surname === '') {
            surname_valid = false;
            surname_input.classList.remove('is-valid');
            surname_input.classList.add('is-invalid');
        } else {
            surname_valid = true;
            surname_input.classList.remove('is-invalid');
            surname_input.classList.add('is-valid');
        }

        if (email === '' || !email_regex.test(email)) {
            email_valid = false;
            email_input.classList.remove('is-valid');
            email_input.classList.add('is-invalid');
        } else {
            email_valid = true;
            email_input.classList.remove('is-invalid');
            email_input.classList.add('is-valid');
        }

        if (password_1 === '' || !password_regex.test(password_1)) {
            password_1_valid = false;
            password_1_input.classList.remove('is-valid');
            password_1_input.classList.add('is-invalid');
            password_2_input.classList.add('is-invalid');
        } else {
            password_1_valid = true;
            password_1_input.classList.remove('is-invalid');
            password_1_input.classList.add('is-valid');
        }

        if (password_2 === '' || !password_regex.test(password_2) || password_1 !== password_2) {
            password_2_valid = false;
            password_2_input.classList.remove('is-valid');
            password_2_input.classList.add('is-invalid');
        } else {
            password_2_valid = true;
            password_2_input.classList.remove('is-invalid');
            password_2_input.classList.add('is-valid');
        }

        if (phone_number === '' || !phone_number_regex.test(phone_number)) {
            phone_number_valid = false;
            phone_number_input.classList.remove('is-valid');
            phone_number_input.classList.add('is-invalid');
        } else {
            phone_number_valid = true;
            phone_number_input.classList.remove('is-invalid');
            phone_number_input.classList.add('is-valid');
        }

        if (address_name === '') {
            address_name_valid = false;
            address_name_input.classList.remove('is-valid');
            address_name_input.classList.add('is-invalid');
        } else {
            address_name_valid = true;
            address_name_input.classList.remove('is-invalid');
            address_name_input.classList.add('is-valid');
        }

        if (address_line === '') {
            address_line_valid = false;
            address_line_input.classList.remove('is-valid');
            address_line_input.classList.add('is-invalid');
        } else {
            address_line_valid = true;
            address_line_input.classList.remove('is-invalid');
            address_line_input.classList.add('is-valid');
        }

        if (town === '') {
            town_valid = false;
            town_input.classList.remove('is-valid');
            town_input.classList.add('is-invalid');
        } else {
            town_valid = true;
            town_input.classList.remove('is-invalid');
            town_input.classList.add('is-valid');
        }

        if (city === '') {
            city_valid = false;
            city_input.classList.remove('is-valid');
            city_input.classList.add('is-invalid');
        } else {
            city_valid = true;
            city_input.classList.remove('is-invalid');
            city_input.classList.add('is-valid');
        }

        if (zip_code === '' || !zip_code_regex.test(zip_code)) {
            zip_code_valid = false;
            zip_code_input.classList.remove('is-valid');
            zip_code_input.classList.add('is-invalid');
        } else {
            zip_code_valid = true;
            zip_code_input.classList.remove('is-invalid');
            zip_code_input.classList.add('is-valid');
        }

        if (!terms_and_conditions.checked) {
            form_alert('Debes aceptar los términos y condiciones.', 'danger', alert_placeholder);
        }

        if (name_valid && surname_valid && email_valid && password_1_valid && password_2_valid && phone_number_valid &&
            address_name_valid && address_line_valid && town_valid && city_valid && zip_code_valid && terms_and_conditions.checked) {
            await fetch('/sign_up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name,
                    surname,
                    email,
                    password_1,
                    password_2,
                    phone_number,
                    address_name,
                    address_line,
                    town,
                    city,
                    zip_code
                }),
            }).then(response => {
                if (response.status === 200 || response.status === 302) {
                    form_alert(
                        'Registro realizado con éxito. Redireccionando... <div class="spinner-border spinner-border-sm text-success" role="status" aria-hidden="true"></div>',
                        'success', alert_placeholder
                        )
                    if (response.redirected) {
                        window.setTimeout(function () {
                            window.location.href = response.url;

                        }, 2000);
                    }
                } else if (response.status === 409) {
                    document.querySelector('#sign_up_email').classList.remove('is-valid');
                    document.querySelector('#sign_up_email').classList.add('is-invalid');
                    form_alert('El correo eléctronico ya está en uso.', 'danger', alert_placeholder);
                    throw new Error(`HTTP error: ${response.status}`);
                } else {
                    form_alert('Comprueba que todos los datos están introducidos de forma correcta.', 'danger', alert_placeholder);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            });
        }
    });
});
