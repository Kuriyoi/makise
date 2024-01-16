let order_table;
const tbody_order = document.querySelector("#orders tbody");

async function get_orders(url) {
    // Calls the API to get all orders in database and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function get_order(url) {
    // Calls the API to get the order with the id provided in the url and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

async function edit_order(url, data) {
    // Calls the API to edit an order in the database with the data provided in the form

    const response = await fetch(url, {
        method: 'PUT',
        body: data
    });
    return response;
}

function add_cancel_eventListener(order, delete_button) {
    // Adds an event listener to the cancel button when the order is rendered

    delete_button.addEventListener('click', () => {
        const error_delete_order = document.querySelector("#error_delete_order");
        const delete_order_form = document.querySelector("#delete_order_form");

        delete_order_form.addEventListener('submit', (event) => {
            event.preventDefault();
            event.stopPropagation();

            edit_order(`/api/order/cancel/${order.id_order}`).then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    form_alert('Error al cancelar el pedido.', 'danger', error_delete_order);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(data => {
                form_alert('Pedido cancelado correctamente.', 'success', error_delete_order);
                let date = new Date(convertPYDateFormatToJS(data.date));
                date = date.toLocaleString('es-ES', { timeZone: 'UTC' });
                row_to_cancel = document.querySelector(`#order-${data.id_order}`);
                row = order_table.row(row_to_cancel).data();
                edited_data = ['Cancelado', date, data.total_price, '<td></td>'];

                for (let i = 0; i < edited_data.length; i++) {
                    row[i] = edited_data[i];
                }

                order_table.row(row_to_cancel).data(row).draw();
            });
        });
    });
}

function add_to_tbody_order(orders, tbody) {
    // Generates the tbody with the orders provided in the orders array
    orders.forEach(order => {
        let date = new Date(convertPYDateFormatToJS(order.date));
        date = date.toLocaleString('es-ES', { timeZone: 'UTC' });

        tbody += `<tr id="order-${order.id_order}">`;
        tbody += `<td>${order.status}</td>`;
        tbody += `<td>${date}</td>`;
        tbody += `<td>${order.total_price}</td>`;
        if (order.status !== 'Cancelado' && order.status !== 'Enviado') {
            tbody += `<td><button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-order-modal" id="edit-${order.id_order}" data-id="${order.id_order}">${edit_icon}</button>`;
            tbody += `<button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#delete-order-modal" id="delete-${order.id_order}" data-id="${order.id_order}">${trash_icon}</button></td>`;
        } else {
            tbody += `<td></td>`;
        }
        tbody += `</tr>`;
    });

    return tbody;
}

function edit_and_delete_listeners_order(orders) {
    // Adds an event listener to the edit and delete buttons when the orders are rendered

    orders.forEach(order => {
        const edit_button = document.querySelector(`#edit-${order.id_order}`);
        const delete_button = document.querySelector(`#delete-${order.id_order}`);

        // add_edit_eventListener(order, edit_button);
        if (delete_button) {
            add_cancel_eventListener(order, delete_button);
        }
    });
}

function hook_search_bar_order() {
    // Adds an event listener to the search bar to filter the orders. It waits until the search bar is rendered with
    // an interval

    let order_filter;

    let interval = setInterval(() => {
        if (document.querySelector('#orders_filter input') !== null) {
            order_filter = document.querySelector('#orders_filter input');
            order_filter.addEventListener("keyup", function () {
                datatable.search(
                    jQuery.fn.DataTable.ext.type.search.string(this.value)
                ).draw();
            });
            clearInterval(interval);
        }
    }, 500);
}

function render_orders() {
    // Renders all the orders in the database in a table with the DataTable library

    get_orders('/api/order').then(orders => {
        let new_tbody_order = '';
        new_tbody_order = add_to_tbody_order(orders, new_tbody_order);
        tbody_order.innerHTML = new_tbody_order;
        edit_and_delete_listeners_order(orders);
        order_table = new DataTable('#orders', {
            responsive: true,
            language: {
                "url": "static/datatable_spanish.json"
            },
            pagingType: 'full_numbers',
            stateSave: true,
            columnDefs: [{
                "targets": [3],
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

document.addEventListener("DOMContentLoaded", function () {
    render_orders();
    hook_search_bar_order();
});
