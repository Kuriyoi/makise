let table;
const tbody = document.querySelector("#users tbody");
const trash_icon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
<path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/>
</svg`;
const edit_icon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
<path d="M12.742 0a.75.75 0 0 1 .53.22l2.78 2.78a.75.75 0 0 1 0 1.06L2.53 15.47a.75.75 0 0 1-1.06 0L.22 14.22a.75.75 0 0 1 0-1.06l12.78-12.78a.75.75 0 0 1 1.06 0l2.78 2.78c.146.147.22.337.22.53v.75c0 .414-.336.75-.75.75h-.75c-.193 0-.383-.074-.53-.22l-1.56-1.56a.75.75 0 0 1 0-1.06L11.28.22a.75.75 0 0 1 .47-.22h.75zm-1.47 1.72L1.94 13.47l-1.72-1.72L10.57 0h.75L11.27.22zM1.22 13.28l11.25-11.25 1.51 1.51L2.72 14.78l-1.5-1.5z"/>
</svg>`;

async function get_users(url) {
    // Calls the API to get all users in database and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function get_user(url) {
    // Calls the API to get the user with the id provided in the url and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function add_user(url, data) {
    // Calls the API to add a new user to the database with the data provided in the form

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return response;
}

async function edit_user(url, data) {
    // Calls the API to edit a user in the database with the data provided in the form

    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return response;
}

async function delete_user(url) {
    // Calls the API to delete the user with the id provided in the url

    const response = await fetch(url, {
        method: 'DELETE'
    });
    return response;
}

function add_edit_eventListener(user, edit_button) {
    // Adds an event listener to the edit button when the user is rendered

    edit_button.addEventListener('click', () => {
        get_user(`/api/user/${user.id_user}`).then(user => {
            let edit_user_form = document.querySelector("#edit_user_form");
            let edit_user_email_input = edit_user_form.querySelector('#edit_user_email');
            let edit_user_name_input = edit_user_form.querySelector('#edit_user_name');
            let edit_user_surname_input = edit_user_form.querySelector('#edit_user_surname');
            let edit_user_phone_number_input = edit_user_form.querySelector('#edit_user_phone_number');

            if (user.admin) {
                user.admin = "Administrador";
            } else {
                user.admin = "Usuario";
            }

            let edit_user_admin_input = edit_user_form.querySelector('input[name="edit_user_admin"][value="' + user.admin + '"]');

            if (edit_user_admin_input) {
                edit_user_admin_input.checked = true;
            }

            edit_user_email_input.value = user.email;
            edit_user_name_input.value = user.name;
            edit_user_surname_input.value = user.surname;
            edit_user_phone_number_input.value = user.phone_number;
            edit_user_admin_input.value = user.admin;

            edit_user_form.addEventListener('submit', (event) => {
                event.preventDefault();
                event.stopPropagation();

                const edit_user_email = edit_user_form['edit_user_email'];
                const edit_user_name = edit_user_form['edit_user_name'];
                const edit_user_surname = edit_user_form['edit_user_surname'];
                const edit_user_phone_number = edit_user_form['edit_user_phone_number'];
                let edit_user_admin = edit_user_form['edit_user_admin'];

                const error_edit_user = document.querySelector("#error_edit_user");

                if (edit_user_admin.value === 'Administrador') {
                    edit_user_admin = true;
                } else {
                    edit_user_admin = false;
                }

                data = {
                    "email": edit_user_email.value,
                    "name": edit_user_name.value,
                    "surname": edit_user_surname.value,
                    "phone_number": edit_user_phone_number.value,
                    "admin": edit_user_admin
                }

                inputs = {
                    "email": edit_user_email_input,
                    "name": edit_user_name_input,
                    "surname": edit_user_surname_input,
                    "phone_number": edit_user_phone_number_input
                }

                valid = validate_data(data, inputs, true);

                if (!valid.includes(false)) {
                    edit_user(`/api/user/${user.id_user}`, data).then(response => {
                        if (response.status === 200) {
                            return response.json();
                        } else {
                            form_alert('Comprueba los datos introducidos.', 'error', error_edit_user);
                            throw new Error(`HTTP error: ${response.status}`);
                        }
                    }).then(user => {
                        form_alert('Usuario editado correctamente.', 'success', error_edit_user);
                        row_to_edit = document.querySelector(`#user-${user.id_user}`);
                        if (user.admin) {
                            user.admin = "Administrador";
                        } else {
                            user.admin = "Usuario";
                        }

                        btn_edit = `<button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-user-modal"  id="edit-${user.id_user}" data-id="${user.id_user}">${edit_icon}</button>`;
                        btn_delete = `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-user-modal" id="delete-${user.id_user}" data-id="${user.id_user}">${trash_icon}</button>`;

                        row = table.row(row_to_edit).data();
                        edited_data = [user.email, user.name, user.surname, user.phone_number, user.admin, btn_edit.concat(btn_delete)];

                        for (let i = 0; i < edited_data.length; i++) {
                            row[i] = edited_data[i];
                        }

                        table.row(row_to_edit).data(row).draw();
                    });
                }
            });
        });
    });
}

function add_delete_eventListener(user, delete_button) {
    // Adds an event listener to the delete button when the user is rendered

    delete_button.addEventListener('click', () => {
        const error_delete_user = document.querySelector("#error_delete_user");
        const delete_user_form = document.querySelector("#delete_user_form");

        delete_user_form.addEventListener('submit', (event) => {
            event.preventDefault();
            event.stopPropagation();

            delete_user(`/api/user/${user.id_user}`).then(response => {
                if (response.status === 200) {
                    return response.json();
                } else if (response.status === 409) {
                    form_alert('No puedes eliminar un usuario con pedidos.', 'danger', error_delete_user);
                    throw new Error(`HTTP error: ${response.status}`);
                } else {
                    form_alert('Error al eliminar el usuario.', 'danger', error_delete_user);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(() => {
                form_alert('Usuario eliminado correctamente.', 'success', error_delete_user);
                row_to_delete = document.querySelector(`#user-${user.id_user}`);
                table.row(row_to_delete).remove().draw(false);
            });
        });
    });
}

function add_to_tbody(users, tbody) {
    // Generates the tbody with the users provided in the users array

    users.forEach(user => {
        if (user.admin) {
            user.admin = "Administrador";
        } else {
            user.admin = "Usuario";
        }
        tbody += `<tr id="user-${user.id_user}">`;
        tbody += `<td>${user.email}</td>`;
        tbody += `<td>${user.name}</td>`;
        tbody += `<td>${user.surname}</td>`;
        tbody += `<td>${user.phone_number}</td>`;
        tbody += `<td>${user.admin}</td>`;
        tbody += `<td><button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-user-modal"  id="edit-${user.id_user}" data-id="${user.id_user}">${edit_icon}</button>`;
        tbody += `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-user-modal" id="delete-${user.id_user}" data-id="${user.id_user}">${trash_icon}</button></td>`;
        tbody += `</tr>`;
    });

    return tbody;
}

function edit_and_delete_listeners(users) {
    // Adds an event listener to the edit and delete buttons when the users are rendered

    users.forEach(user => {
        const edit_button = document.querySelector(`#edit-${user.id_user}`);
        const delete_button = document.querySelector(`#delete-${user.id_user}`);

        add_edit_eventListener(user, edit_button);
        add_delete_eventListener(user, delete_button);
    });
}

function hook_search_bar() {
    // Adds an event listener to the search bar to filter the users. It waits until the search bar is rendered with
    // an interval

    let user_filter;

    let interval = setInterval(() => {
        if (document.querySelector('#users_filter input') !== null) {
            user_filter = document.querySelector('#users_filter input');
            user_filter.addEventListener("keyup", function () {
                datatable.search(
                    jQuery.fn.DataTable.ext.type.search.string(this.value)
                ).draw();
            });
            clearInterval(interval);
        }
    }, 500);
}

function render_users() {
    // Renders all the users in the database in a table with the DataTable library

    get_users('/api/user').then(users => {
        let new_tbody = '';
        new_tbody = add_to_tbody(users, new_tbody);
        tbody.innerHTML = new_tbody;
        edit_and_delete_listeners(users);
        table = new DataTable('#users', {
            responsive: true,
            language: {
                "url": "static/datatable_spanish.json"
            },
            pagingType: 'full_numbers',
            stateSave: true,
            columnDefs: [{
                "targets": [3, 4, 5],
                "orderable": false
            }],
            pageLength: 10,
            lengthMenu: [
                [10, 20, 30, -1],
                [10, 20, 30, 'Todos']
            ],
        });
    });
}

function validate_data(data, input, edit=false) {
    // Validates the data provided in the add or edit user form and returns an array with the errors

    const email_regex = /^[\w\.-]+\@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/;
    const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[a-zA-Z\d\W_]{8,}$/;
    const phone_number_regex = /^[0-9]{9}$/;

    let name_valid, surname_valid, email_valid, password_1_valid, password_2_valid, phone_number_valid = false;

    if (data.name === '') {
        name_valid = false;
        input.name.classList.remove('is-valid');
        input.name.classList.add('is-invalid');
    } else {
        name_valid = true;
        input.name.classList.remove('is-invalid');
        input.name.classList.add('is-valid');
    }

    if (data.surname === '') {
        surname_valid = false;
        input.surname.classList.remove('is-valid');
        input.surname.classList.add('is-invalid');
    } else {
        surname_valid = true;
        input.surname.classList.remove('is-invalid');
        input.surname.classList.add('is-valid');
    }

    if (data.email === '' || !email_regex.test(data.email)) {
        email_valid = false;
        input.email.classList.remove('is-valid');
        input.email.classList.add('is-invalid');
    } else {
        email_valid = true;
        input.email.classList.remove('is-invalid');
        input.email.classList.add('is-valid');
    }

    if (!edit) {
        if (data.password_1 === '' || !password_regex.test(data.password_1)) {
            password_1_valid = false;
            input.password_1.classList.remove('is-valid');
            input.password_1.classList.add('is-invalid');
            input.password_2.classList.add('is-invalid');
        } else {
            password_1_valid = true;
            input.password_1.classList.remove('is-invalid');
            input.password_1.classList.add('is-valid');
        }

        if (data.password_2 === '' || !password_regex.test(data.password_2) || data.password_1 !== data.password_2) {
            password_2_valid = false;
            input.password_2.classList.remove('is-valid');
            input.password_2.classList.add('is-invalid');
        } else {
            password_2_valid = true;
            input.password_2.classList.remove('is-invalid');
            input.password_2.classList.add('is-valid');
        }
    }

    if (data.phone_number === '' || !phone_number_regex.test(data.phone_number)) {
        phone_number_valid = false;
        input.phone_number.classList.remove('is-valid');
        input.phone_number.classList.add('is-invalid');
    } else {
        phone_number_valid = true;
        input.phone_number.classList.remove('is-invalid');
        input.phone_number.classList.add('is-valid');
    }

    valid = [name_valid, surname_valid, email_valid, password_1_valid, password_2_valid, phone_number_valid];

    return valid;
}

document.addEventListener('DOMContentLoaded', function () {
    render_users();
    hook_search_bar();

    const add_user_form = document.querySelector("#add_user_form");
    const error_add_user = document.querySelector("#error_add_user");

    add_user_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const add_user_email = add_user_form['add_user_email'].value;
        const add_user_password_1 = add_user_form['add_user_password_1'].value;
        const add_user_password_2 = add_user_form['add_user_password_2'].value;
        const add_user_name = add_user_form['add_user_name'].value;
        const add_user_surname = add_user_form['add_user_surname'].value;
        const add_user_phone_number = add_user_form['add_user_phone_number'].value;
        let add_user_admin = add_user_form['add_user_admin'].value;

        const add_user_email_input = add_user_form.querySelector('#add_user_email');
        const add_user_password_1_input = add_user_form.querySelector('#add_user_password_1');
        const add_user_password_2_input = add_user_form.querySelector('#add_user_password_2');
        const add_user_name_input = add_user_form.querySelector('#add_user_name');
        const add_user_surname_input = add_user_form.querySelector('#add_user_surname');
        const add_user_phone_number_input = add_user_form.querySelector('#add_user_phone_number');

        if (add_user_admin === 'Administrador') {
            add_user_admin = true;
        } else {
            add_user_admin = false;
        }

        data = {
            "email": add_user_email,
            "password_1": add_user_password_1,
            "password_2": add_user_password_2,
            "name": add_user_name,
            "surname": add_user_surname,
            "phone_number": add_user_phone_number,
            "admin": add_user_admin
        }

        inputs = {
            "email": add_user_email_input,
            "password_1": add_user_password_1_input,
            "password_2": add_user_password_2_input,
            "name": add_user_name_input,
            "surname": add_user_surname_input,
            "phone_number": add_user_phone_number_input
        }

        let valid = validate_data(data, inputs);
        let invalid = valid.includes(false);

        if (!invalid) {
            add_user('/api/user', data).then(response => {
                if (response.status === 201) {
                    return response.json();
                } else if (response.status === 409) {
                    document.querySelector('#add_user_email').classList.remove('is-valid');
                    document.querySelector('#add_user_email').classList.add('is-invalid');
                    form_alert('El correo eléctronico ya está en uso.', 'danger', error_add_user);
                    throw new Error(`HTTP error: ${response.status}`);
                } else {
                    form_alert('Comprueba los datos introducidos.', 'error', error_add_user);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(user => {
                form_alert('Usuario añadido correctamente.', 'success', error_add_user);
                add_user_form.reset();
                btn_edit = `<button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#add-user-modal"  id="edit-${user.id_user}" data-id="${user.id_user}">${edit_icon}</button>`;
                btn_delete = `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-user-modal" id="delete-${user.id_user}" data-id="${user.id_user}">${trash_icon}</button>`;

                if (user.admin) {
                    user.admin = "Administrador";
                } else {
                    user.admin = "Usuario";
                }

                table.row.add(
                    [user.email, user.name, user.surname, user.phone_number, user.admin, btn_edit.concat(btn_delete)]
                ).draw(false);

                const edit_button = document.querySelector(`#edit-${user.id_user}`);
                const delete_button = document.querySelector(`#delete-${user.id_user}`);

                add_edit_eventListener(user, edit_button);
                add_delete_eventListener(user, delete_button);
            });
        }
    });
});
