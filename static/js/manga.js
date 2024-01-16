let manga_table;
const tbody_manga = document.querySelector("#mangas tbody");

async function get_mangas(url) {
    // Calls the API to get all mangas in database and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function get_suppliers(url) {
    // Calls the API to get all suppliers in database and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function get_manga(url) {
    // Calls the API to get the manga with the id provided in the url and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function add_manga(url, data) {
    // Calls the API to add a new manga to the database with the data provided in the form

    const response = await fetch(url, {
        method: 'POST',
        body: data
    });
    return response;
}

async function edit_manga(url, data) {
    // Calls the API to edit a manga in the database with the data provided in the form

    const response = await fetch(url, {
        method: 'PUT',
        body: data
    });
    return response;
}

async function delete_manga(url) {
    // Calls the API to delete the manga with the id provided in the url

    const response = await fetch(url, {
        method: 'DELETE'
    });
    return response;
}

function add_edit_eventListener_manga(manga, edit_button) {
    // Adds an event listener to the edit button when the manga is rendered

    edit_button.addEventListener('click', () => {
        get_manga(`/api/manga/${manga.id_manga}`).then(manga => {
            let edit_manga_form = document.querySelector("#edit_manga_form");
            let edit_manga_title_input = edit_manga_form.querySelector('#edit_manga_title');
            let edit_manga_image_input = edit_manga_form.querySelector('#edit_manga_image');
            let edit_manga_author_input = edit_manga_form.querySelector('#edit_manga_author');
            let edit_manga_stock_input = edit_manga_form.querySelector('#edit_manga_stock');
            let edit_manga_genre_input = edit_manga_form.querySelector('#edit_manga_genre');
            let edit_manga_publisher_input = edit_manga_form.querySelector('#edit_manga_publisher');
            let edit_manga_supplier_input = edit_manga_form.querySelector('#manga_supplier_select_edit');
            let edit_manga_description_input = edit_manga_form.querySelector('#edit_manga_description');

            render_manga_suppliers(true, manga);

            edit_manga_title_input.value = manga.title;
            edit_manga_author_input.value = manga.author;
            edit_manga_stock_input.value = manga.stock;
            edit_manga_genre_input.value = manga.genre;
            edit_manga_publisher_input.value = manga.publisher;
            edit_manga_description_input.value = manga.description;

            edit_manga_form.addEventListener('submit', (event) => {
                event.preventDefault();
                event.stopPropagation();

                const edit_manga_title = edit_manga_form['edit_manga_title'].value;
                const edit_manga_image = edit_manga_form['edit_manga_image'].value;
                const edit_manga_author = edit_manga_form['edit_manga_author'].value;
                const edit_manga_stock = edit_manga_form['edit_manga_stock'].value;
                const edit_manga_genre = edit_manga_form['edit_manga_genre'].value;
                const edit_manga_publisher = edit_manga_form['edit_manga_publisher'].value;
                const edit_manga_supplier = edit_manga_supplier_input.value;
                const edit_manga_description = edit_manga_form['edit_manga_description'].value;

                const error_edit_manga = document.querySelector("#error_edit_manga");

                data = {
                    "title": edit_manga_title,
                    "image": edit_manga_image === '' ? null : edit_manga_image_input.files[0],
                    "author": edit_manga_author,
                    "stock": edit_manga_stock === '' ? '' : parseInt(edit_manga_stock),
                    "genre": edit_manga_genre,
                    "publisher": edit_manga_publisher,
                    "supplier": edit_manga_supplier,
                    "description": edit_manga_description
                }

                inputs = {
                    "title": edit_manga_title_input,
                    "image": edit_manga_image_input,
                    "author": edit_manga_author_input,
                    "stock": edit_manga_stock_input,
                    "genre": edit_manga_genre_input,
                    "publisher": edit_manga_publisher_input,
                    "description": edit_manga_description_input
                }

                valid = validate_data_manga(data, inputs, true);

                if (!valid.includes(false)) {
                    const form_data = new FormData();

                    for (const key in data) {
                        form_data.append(key, data[key]);
                    }

                    edit_manga(`/api/manga/${manga.id_manga}`, form_data).then(response => {
                        if (response.status === 200) {
                            return response.json();
                        } else {
                            form_alert('Comprueba los datos introducidos.', 'error', error_edit_manga);
                            throw new Error(`HTTP error: ${response.status}`);
                        }
                    }).then(manga => {
                        form_alert('Manga editado correctamente.', 'success', error_edit_manga);
                        row_to_edit = document.querySelector(`#manga-${manga.id_manga}`);

                        btn_edit = `<button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-manga-modal"  id="edit-${manga.id_manga}" data-id="${manga.id_manga}">${edit_icon}</button>`;
                        btn_delete = `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-manga-modal" id="delete-${manga.id_manga}" data-id="${manga.id_manga}">${trash_icon}</button>`;

                        row = manga_table.row(row_to_edit).data();
                        edited_data = [manga.title, `<img src="${covers_folder}/${manga.image}" alt="${manga.title}">`, manga.stock, manga.price, manga.author, manga.genre, manga.publisher, manga.supplier_name, btn_edit.concat(btn_delete)]

                        for (let i = 0; i < edited_data.length; i++) {
                            row[i] = edited_data[i];
                        }

                        manga_table.row(row_to_edit).data(row).draw();
                    });
                }
            });
        });
    });
}

function add_delete_eventListener_manga(manga, delete_button) {
    // Adds an event listener to the delete button when the manga is rendered

    delete_button.addEventListener('click', () => {
        const error_delete_manga = document.querySelector("#error_delete_manga");
        const delete_manga_form = document.querySelector("#delete_manga_form");

        delete_manga_form.addEventListener('submit', (event) => {
            event.preventDefault();
            event.stopPropagation();

            delete_manga(`/api/manga/${manga.id_manga}`).then(response => {
                if (response.status === 200) {
                    return response.json();
                } else if (response.status === 409) {
                    form_alert('No puedes eliminar un manga en pedidos.', 'danger', error_delete_manga);
                    throw new Error(`HTTP error: ${response.status}`);
                } else {
                    form_alert('Error al eliminar el manga.', 'danger', error_delete_manga);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(() => {
                form_alert('Manga eliminado correctamente.', 'success', error_delete_manga);
                row_to_delete = document.querySelector(`#manga-${manga.id_manga}`);
                manga_table.row(row_to_delete).remove().draw(false);
            });
        });
    });
}

function add_to_tbody_manga(mangas, tbody) {
    // Generates the tbody with the mangas provided in the users array

    mangas.forEach(manga => {
        tbody += `<tr id="manga-${manga.id_manga}">`;
        tbody += `<td>${manga.title}</td>`;
        tbody += `<td><img src="${covers_folder}/${manga.image}" alt="${manga.title}"></td>`;
        tbody += `<td>${manga.stock}</td>`;
        tbody += `<td>${manga.price}</td>`;
        tbody += `<td>${manga.author}</td>`;
        tbody += `<td>${manga.genre}</td>`;
        tbody += `<td>${manga.publisher}</td>`;
        tbody += `<td>${manga.supplier_name}</td>`;
        tbody += `<td><button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-manga-modal"  id="edit-${manga.id_manga}" data-id="${manga.id_manga}">${edit_icon}</button>`;
        tbody += `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-manga-modal" id="delete-${manga.id_manga}" data-id="${manga.id_manga}">${trash_icon}</button></td>`;
        tbody += `</tr>`;
    });

    return tbody;
}

function edit_and_delete_listeners_manga(mangas) {
    // Adds an event listener to the edit and delete buttons when the mangas are rendered

    mangas.forEach(manga => {
        const edit_button = document.querySelector(`#edit-${manga.id_manga}`);
        const delete_button = document.querySelector(`#delete-${manga.id_manga}`);

        add_edit_eventListener_manga(manga, edit_button);
        add_delete_eventListener_manga(manga, delete_button);
    });
}

function hook_search_bar_manga() {
    // Adds an event listener to the search bar to filter the mangas. It waits until the search bar is rendered with
    // an interval

    let manga_filter;

    let interval = setInterval(() => {
        if (document.querySelector('#mangas_filter input') !== null) {
            manga_filter = document.querySelector('#mangas_filter input');
            manga_filter.addEventListener("keyup", function () {
                datatable.search(
                    jQuery.fn.DataTable.ext.type.search.string(this.value)
                ).draw();
            });
            clearInterval(interval);
        }
    }, 500);
}

function render_mangas() {
    // Renders all the mangas in the database in a table with the DataTable library

    get_mangas('/api/mangas_admin/simple').then(mangas => {
        let new_tbody_manga = '';
        new_tbody_manga = add_to_tbody_manga(mangas, new_tbody_manga);
        tbody_manga.innerHTML = new_tbody_manga;
        edit_and_delete_listeners_manga(mangas);
        manga_table = new DataTable('#mangas', {
            responsive: true,
            language: {
                "url": "static/datatable_spanish.json"
            },
            pagingType: 'full_numbers',
            stateSave: true,
            columnDefs: [{
                "targets": [1, 8],
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

function render_manga_suppliers(edit=false, manga=null) {
    // Renders all the suppliers in the database in a select

    if (edit) {
        get_suppliers('/api/supplier').then(suppliers => {
            const edit_manga_supplier_select = document.querySelector("#manga_supplier_select_edit");
            let edit_manga_supplier_select_options = '';
            suppliers.forEach(supplier => {
                if (supplier.id_supplier === manga.supplier) {
                    edit_manga_supplier_select_options += `<option value="${supplier.id_supplier}" selected>${supplier.name}</option>`;
                } else {
                    edit_manga_supplier_select_options += `<option value="${supplier.id_supplier}">${supplier.name}</option>`;
                }
            });
            edit_manga_supplier_select.innerHTML = edit_manga_supplier_select_options;
        });
    } else {
        get_suppliers('/api/supplier').then(suppliers => {
            const manga_supplier_select = document.querySelector("#manga_supplier_select");
            let manga_supplier_select_options = '';
            suppliers.forEach((supplier, index) => {
                if (index === 0) {
                    manga_supplier_select_options += `<option value="${supplier.id_supplier}" selected>${supplier.name}</option>`;
                } else {
                    manga_supplier_select_options += `<option value="${supplier.id_supplier}">${supplier.name}</option>`;
                }
            });
            manga_supplier_select.innerHTML = manga_supplier_select_options;
        });
    }
}

function validate_data_manga(data, input, edit=false) {
    // Validates the data provided in the add or edit manga form and returns an array with the errors

    let title_valid, image_valid, author_valid, stock_valid, price_valid, genre_valid, publisher_valid, description_valid = false;

    if (data.title === '') {
        title_valid = false;
        input.title.classList.remove('is-valid');
        input.title.classList.add('is-invalid');
    } else {
        title_valid = true;
        input.title.classList.remove('is-invalid');
        input.title.classList.add('is-valid');
    }

    if (data.author === '') {
        author_valid = false;
        input.author.classList.remove('is-valid');
        input.author.classList.add('is-invalid');
    } else {
        author_valid = true;
        input.author.classList.remove('is-invalid');
        input.author.classList.add('is-valid');
    }

    if (data.stock === '' || !Number.isInteger(data.stock)) {
        stock_valid = false;
        input.stock.classList.remove('is-valid');
        input.stock.classList.add('is-invalid');
    } else {
        stock_valid = true;
        input.stock.classList.remove('is-invalid');
        input.stock.classList.add('is-valid');
    }

    if (!edit) {
        if (data.price === '') {
            price_valid = false;
            input.price.classList.remove('is-valid');
            input.price.classList.add('is-invalid');
        }
        else {
            price_valid = true;
            input.price.classList.remove('is-invalid');
            input.price.classList.add('is-valid');
        }
    }

    if (data.genre === '') {
        genre_valid = false;
        input.genre.classList.remove('is-valid');
        input.genre.classList.add('is-invalid');
    } else {
        genre_valid = true;
        input.genre.classList.remove('is-invalid');
        input.genre.classList.add('is-valid');
    }

    if (data.publisher === '') {
        publisher_valid = false;
        input.publisher.classList.remove('is-valid');
        input.publisher.classList.add('is-invalid');
    } else {
        publisher_valid = true;
        input.publisher.classList.remove('is-invalid');
        input.publisher.classList.add('is-valid');
    }

    if (data.description === '') {
        description_valid = false;
        input.description.classList.remove('is-valid');
        input.description.classList.add('is-invalid');
    } else {
        description_valid = true;
        input.description.classList.remove('is-invalid');
        input.description.classList.add('is-valid');
    }

    if ((data.image === null && !edit) || (input.image.files.length === 0 && !edit)) {
        image_valid = false;
        input.image.classList.remove('is-valid');
        input.image.classList.add('is-invalid');
    } else {
        image_valid = true;
        input.image.classList.remove('is-invalid');
        input.image.classList.add('is-valid');
    }

    valid = [title_valid, author_valid, stock_valid, genre_valid, publisher_valid, image_valid];

    return valid;
}

document.addEventListener('DOMContentLoaded', function () {
    render_mangas();
    render_manga_suppliers();
    hook_search_bar_manga();

    const add_manga_form = document.querySelector("#add_manga_form");
    const error_add_manga = document.querySelector("#error_add_manga");

    add_manga_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const add_manga_title = add_manga_form['add_manga_title'].value;
        const add_manga_image = add_manga_form['add_manga_image'].value;
        const add_manga_author = add_manga_form['add_manga_author'].value;
        const add_manga_stock = add_manga_form['add_manga_stock'].value;
        const add_manga_price = add_manga_form['add_manga_price'].value;
        const add_manga_genre = add_manga_form['add_manga_genre'].value;
        const add_manga_publisher = add_manga_form['add_manga_publisher'].value;
        const add_manga_supplier = add_manga_form.querySelector('#manga_supplier_select').value;
        const add_manga_description = add_manga_form['add_manga_description'].value;

        const add_manga_title_input = add_manga_form.querySelector('#add_manga_title');
        const add_manga_image_input = add_manga_form.querySelector('#add_manga_image');
        const add_manga_author_input = add_manga_form.querySelector('#add_manga_author');
        const add_manga_stock_input = add_manga_form.querySelector('#add_manga_stock');
        const add_manga_price_input = add_manga_form.querySelector('#add_manga_price');
        const add_manga_genre_input = add_manga_form.querySelector('#add_manga_genre');
        const add_manga_publisher_input = add_manga_form.querySelector('#add_manga_publisher');
        const add_manga_description_input = add_manga_form.querySelector('#add_manga_description');

        data = {
            "title": add_manga_title,
            "image": add_manga_image === '' ? null : add_manga_image_input.files[0],
            "author": add_manga_author,
            "stock": add_manga_stock === '' ? '' : parseInt(add_manga_stock),
            "price": add_manga_price === '' ? '' : parseFloat(add_manga_price),
            "genre": add_manga_genre,
            "publisher": add_manga_publisher,
            "supplier": add_manga_supplier,
            "description": add_manga_description
        }

        inputs = {
            "title": add_manga_title_input,
            "image": add_manga_image_input,
            "author": add_manga_author_input,
            "stock": add_manga_stock_input,
            "price": add_manga_price_input,
            "genre": add_manga_genre_input,
            "publisher": add_manga_publisher_input,
            "description": add_manga_description_input
        }

        let valid = validate_data_manga(data, inputs);
        let invalid = valid.includes(false);

        if (!invalid) {
            const form_data = new FormData();

            for (const key in data) {
                form_data.append(key, data[key]);
            }

            add_manga('/api/manga', form_data).then(response => {
                if (response.status === 201) {
                    return response.json();
                } else if (response.status === 409) {
                    document.querySelector('#add_manga_image').classList.remove('is-valid');
                    document.querySelector('#add_manga_image').classList.add('is-invalid');
                    form_alert('Formato de imagen no permitido.', 'danger', error_add_manga);
                    throw new Error(`HTTP error: ${response.status}`);
                } else {
                    form_alert('Comprueba los datos introducidos.', 'error', error_add_manga);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(manga => {
                form_alert('Manga añadido correctamente.', 'success', error_add_manga);
                add_manga_form.reset();
                btn_edit = `<button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-manga-modal"  id="edit-${manga.id_manga}" data-id="${manga.id_manga}">${edit_icon}</button>`;
                btn_delete = `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-manga-modal" id="delete-${manga.id_manga}" data-id="${manga.id_manga}">${trash_icon}</button>`;

                manga_table.row.add(
                    [manga.title, `<img src="${covers_folder}/${manga.image}" alt="${manga.title}">`, manga.stock, manga.price, manga.author, manga.genre, manga.publisher, manga.supplier_name, btn_edit.concat(btn_delete)]
                ).draw(false);

                const edit_button = document.querySelector(`#edit-${manga.id_manga}`);
                const delete_button = document.querySelector(`#delete-${manga.id_manga}`);

                add_edit_eventListener_manga(manga, edit_button);
                add_delete_eventListener_manga(manga, delete_button);
            });
        }
    });
});
