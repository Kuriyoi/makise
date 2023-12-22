let order_table;
const tbody_order = document.querySelector("#orders tbody");

async function get_orders(url) {
    // Calls the API to get all orders in database and returns a json

    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

function add_to_tbody_order(orders, tbody) {
    // Generates the tbody with the orders provided in the orders array

    orders.forEach(order => {
        tbody += `<tr id="order-${order.id_order}">`;
        tbody += `<td>${order.status}</td>`;
        tbody += `<td>${order.date}</td>`;
        tbody += `<td>${order.total_price}</td>`;
        tbody += `<td><button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#edit-order-modal"  id="edit-${order.id_order}" data-id="${order.id_order}">${edit_icon}</button>`;
        tbody += `<button type="button" class="btn btn-outline-danger" id="delete-${order.id_order}" data-id="${order.id_order}">${trash_icon}</button></td>`;
        tbody += `</tr>`;
    });

    return tbody;
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
