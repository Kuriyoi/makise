async function get_user(url) {
    // Calls the API to get the user with the id provided in the url and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

document.addEventListener('DOMContentLoaded', function () {
    const alert_placeholder_user = document.querySelector('#error_profile');
    const profile_form = document.querySelector('#profile_form');

    get_user('/api/user/me').then(user => {
        profile_form['name'].value = user.name;
        profile_form['surname'].value = user.surname;
        profile_form['email'].value = user.email;
        profile_form['phone_number'].value = user.phone_number;
    });

    const name_input = document.querySelector('#profile_name');
    const surname_input = document.querySelector('#profile_surname');
    const email_input = document.querySelector('#profile_email');
    const phone_number_input = document.querySelector('#profile_phone_number');
    const profile_edit = document.querySelector('#profile_edit');
    const profile_save = document.querySelector('#profile_save');

    profile_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const name = profile_form['name'].value;
        const surname = profile_form['surname'].value;
        const email = profile_form['email'].value;
        const phone_number = profile_form['phone_number'].value;

        let name_valid, surname_valid, email_valid, phone_number_valid = false;

        const email_regex = /^[\w\.-]+\@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;
        const phone_number_regex = /^[0-9]{9}$/;

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

        if (phone_number === '' || !phone_number_regex.test(phone_number)) {
            phone_number_valid = false;
            phone_number_input.classList.remove('is-valid');
            phone_number_input.classList.add('is-invalid');
        } else {
            phone_number_valid = true;
            phone_number_input.classList.remove('is-invalid');
            phone_number_input.classList.add('is-valid');
        }

        if (name_valid && surname_valid && email_valid && phone_number_valid) {
            await fetch('/api/user/me', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name,
                    surname,
                    email,
                    phone_number
                }),
            }).then(response => {
                if (response.status === 200) {
                    form_alert('Cambios guardados correctamente.', 'success', alert_placeholder_user);
                    name_input.readOnly = true;
                    surname_input.readOnly = true;
                    email_input.readOnly = true;
                    phone_number_input.readOnly = true;
                    profile_save.setAttribute('disabled', 'disabled');
                    profile_edit.removeAttribute('disabled');

                    name_input.classList.remove('is-valid');
                    surname_input.classList.remove('is-valid');
                    email_input.classList.remove('is-valid');
                    phone_number_input.classList.remove('is-valid');
                }
                else {
                    form_alert('Comprueba los datos introducidos.', 'danger', alert_placeholder_user);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            });
        }
    });

    profile_edit.addEventListener('click', function (event) {
        event.preventDefault();
        event.stopPropagation();

        name_input.readOnly = false;
        surname_input.readOnly = false;
        email_input.readOnly = false;
        phone_number_input.readOnly = false;
        profile_edit.setAttribute('disabled', 'disabled');
        profile_save.removeAttribute('disabled');
    });

    const addresses_table = document.querySelectorAll('.profile_addresses');

    addresses_table.forEach(function(address_form) {
        const profile_address_edit = address_form.querySelector('.edit_address');
        const profile_address_save = address_form.querySelector('.save_address');

        const address_id = address_form['profile_address_id'].value;

        const address_name_input = document.querySelector(`#profile_address_name_${address_id}`);
        const address_line_input = document.querySelector(`#profile_address_line_${address_id}`);
        const town_input = document.querySelector(`#profile_town_${address_id}`);
        const city_input = document.querySelector(`#profile_city_${address_id}`);
        const zip_code_input = document.querySelector(`#profile_zip_code_${address_id}`);

        const alert_placeholder_address = document.querySelector(`#error_address_${address_id}`);

        address_form.addEventListener('submit', async function (event) {
            event.preventDefault();
            event.stopPropagation();

            const address_name = address_form['address_name'].value;
            const address_line = address_form['address_line'].value;
            const town = address_form['town'].value;
            const city = address_form['city'].value;
            const zip_code = address_form['zip_code'].value;

            let address_name_valid, address_line_valid, town_valid, city_valid, zip_code_valid = false;

            const zip_code_regex = /^[0-9]{5}$/;

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

            if (address_name_valid && address_line_valid && town_valid && city_valid && zip_code_valid) {
                await fetch(`/api/address/${address_id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        address_name,
                        address_line,
                        town,
                        city,
                        zip_code
                    }),
                }).then(response => {
                    if (response.status === 200) {
                        form_alert('Cambios guardados correctamente.', 'success', alert_placeholder_address);
                        address_name_input.readOnly = true;
                        address_line_input.readOnly = true;
                        town_input.readOnly = true;
                        city_input.readOnly = true;
                        zip_code_input.readOnly = true;
                        profile_address_save.setAttribute('disabled', 'disabled');
                        profile_address_edit.removeAttribute('disabled');

                        address_name_input.classList.remove('is-valid');
                        address_line_input.classList.remove('is-valid');
                        town_input.classList.remove('is-valid');
                        city_input.classList.remove('is-valid');
                        zip_code_input.classList.remove('is-valid');
                    }
                    else {
                        form_alert('Comprueba los datos introducidos.', 'danger', alert_placeholder_address);
                        throw new Error(`HTTP error: ${response.status}`);
                    }
                });
            }
        });

        profile_address_edit.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();

            address_name_input.readOnly = false;
            address_line_input.readOnly = false;
            town_input.readOnly = false;
            city_input.readOnly = false;
            zip_code_input.readOnly = false;
            profile_address_edit.setAttribute('disabled', 'disabled');
            profile_address_save.removeAttribute('disabled');
        });
    });

    const add_address_form = document.querySelector('#profile_add_address_form');

    add_address_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const address_name = add_address_form['address_name'].value;
        const address_line = add_address_form['address_line'].value;
        const town = add_address_form['town'].value;
        const city = add_address_form['city'].value;
        const zip_code = add_address_form['zip_code'].value;

        let address_name_valid, address_line_valid, town_valid, city_valid, zip_code_valid = false;

        const zip_code_regex = /^[0-9]{5}$/;

        const address_name_input = document.querySelector('#profile_address_name');
        const address_line_input = document.querySelector('#profile_address_line');
        const town_input = document.querySelector('#profile_town');
        const city_input = document.querySelector('#profile_city');
        const zip_code_input = document.querySelector('#profile_zip_code');

        const error_add_address = document.querySelector('#error_add_address');

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
        }
        else {
            zip_code_valid = true;
            zip_code_input.classList.remove('is-invalid');
            zip_code_input.classList.add('is-valid');
        }

        if (address_name_valid && address_line_valid && town_valid && city_valid && zip_code_valid) {
            await fetch('/api/address', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    address_name,
                    address_line,
                    town,
                    city,
                    zip_code
                }),
            }).then(response => {
                if (response.status === 201) {
                    return response.json();
                } else {
                    form_alert('Comprueba los datos introducidos.', 'danger', error_add_address);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(data => {
                form_alert('Dirección añadida correctamente.', 'success', error_add_address);
                    const new_address = data;
                    const container_add_addresses = document.querySelector('#container_add_addresses');
                    let new_address_div = document.createElement('div');

                    add_address_form.reset();
                    add_address_form.classList.remove('was-validated');
                    add_address_form.classList.add('needs-validation');

                    new_address_div.innerHTML = `<div class="addresses-body p-2 mt-2">
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="accordion_address_${new_address.id_address}">
                                <button class="accordion-button" type="button" data-bs-toggle="collapse"
                                    data-bs-target="#accordion_address_${new_address.id_address}_collapse"
                                    aria-expanded="true"
                                    aria-controls="accordion_address_${new_address.id_address}_collapse">
                                    ${new_address.address_name}
                                </button>
                            </h2>
                            <div id="accordion_address_${new_address.id_address}_collapse" class="accordion-collapse collapse fm-semibold"
                                aria-labelledby="accordion_address_${new_address.id_address}" data-bs-parent="#addresses_accordion">
                                <div class="accordion-body">
                                    <form id="profile_edit_address_form_${new_address.id_address}" class="needs-validation profile_addresses" novalidate>
                                        <div id="error_address_${new_address.id_address}" class="container" role="alert"></div>
                                        <input type="hidden" name="profile_address_id" id="profile_address_id_${new_address.id_address}" value="${new_address.id_address}">
                                        <div class="mb-4 pb-2">
                                            <div class="form-floating">
                                                <input type="text" id="profile_address_name_${new_address.id_address}" name="address_name" class="form-control form-control-lg"
                                                    required placeholder="Mi Dirección" readonly value="${new_address.address_name}">
                                                <label for="profile_name">Nombre de la dirección</label>
                                                <div class="form-text">
                                                    Ej.: Mi dirección, Mi casa, etc.
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mb-4 pb-2">
                                            <div class="form-floating">
                                                <input type="text" id="profile_address_line_${new_address.id_address}" name="address_line" class="form-control form-control-lg"
                                                    required placeholder="Calle del Sol 1" readonly value="${new_address.address_line}">
                                                <label for="profile_address_line">Calle y número</label>
                                                <div class="form-text">
                                                    Introduce la calle, el número y, si fuera necesario, portal, puerta, etc.
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mb-4 pb-2">
                                            <div class="form-floating">
                                                <input type="text" id="profile_town_${new_address.id_address}" name="town" class="form-control form-control-lg"
                                                    required placeholder="Camas" readonly value="${new_address.town}">
                                                <label for="profile_town">Localidad</label>
                                            </div>
                                        </div>
                                        <div class="mb-4 pb-2">
                                            <div class="form-floating">
                                                <input type="text" id="profile_city_${new_address.id_address}" name="city"
                                                    class="form-control form-control-lg" required placeholder="Sevilla" readonly value="${new_address.city}">
                                                <label for="profile_city">Provincia</label>
                                            </div>
                                        </div>
                                        <div class="mb-4 pb-2">
                                            <div class="form-floating">
                                                <input type="number" id="profile_zip_code_${new_address.id_address}" name="zip_code"
                                                    class="form-control form-control-lg" required placeholder="41110" readonly value="${new_address.zip_code}">
                                                <label for="sign_up_zip_code">Código postal</label>
                                            </div>
                                        </div>
                                        <div class="d-grid gap-2">
                                            <button id="profile_address_${new_address.id_address}_edit" type="button" class="btn btn-outline-secondary mt-2 edit_address">Editar</button>
                                            <button id="profile_address_${new_address.id_address}_save" type="submit" class="btn btn-success save_address" disabled>Guardar cambios</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>`;

                    container_add_addresses.append(new_address_div);
            });
        }
    });

    const profile_edit_password_form = document.querySelector('#profile_edit_password_form');

    profile_edit_password_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const current_password = profile_edit_password_form['current_password'].value;
        const password_1 = profile_edit_password_form['profile_new_password_1'].value;
        const password_2 = profile_edit_password_form['profile_new_password_2'].value;

        let current_password_valid, password_1_valid, password_2_valid = false;

        const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[a-zA-Z\d\W_]{8,}$/;

        const current_password_input = document.querySelector('#profile_current_password');
        const password_1_input = document.querySelector('#profile_new_password_1');
        const password_2_input = document.querySelector('#profile_new_password_2');

        const error_edit_password = document.querySelector('#error_edit_password');

        if (current_password === '') {
            current_password_valid = false;
            current_password_input.classList.remove('is-valid');
            current_password_input.classList.add('is-invalid');
        } else {
            current_password_valid = true;
            current_password_input.classList.remove('is-invalid');
            current_password_input.classList.add('is-valid');
        }

        if (password_1 === '' || !password_regex.test(password_1) || password_1 === current_password) {
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

        if (current_password_valid && password_1_valid && password_2_valid) {
            await fetch('/api/user/me', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    current_password,
                    password_1,
                    password_2
                }),
            }).then(response => {
                if (response.status === 200) {
                    form_alert('Contraseña actualizada correctamente.', 'success', error_edit_password);
                    profile_edit_password_form.reset();
                    profile_edit_password_form.classList.remove('was-validated');
                    profile_edit_password_form.classList.add('needs-validation');

                    password_1_input.classList.remove('is-valid');
                    password_2_input.classList.remove('is-valid');
                }
                else {
                    form_alert('Comprueba que la contraseña actual sea correcta y que la nueva contraseña sea diferente a la actual', 'danger', error_edit_password);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            });
        }
    });
});
