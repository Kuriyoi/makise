document.addEventListener("DOMContentLoaded", function () {
    async function get_products(url) {
        // Calls the API to get all products in database and returns a json
    
        const response = await fetch(url, {
            method: 'GET'
        });
        return response.json()
    }

    function render_products(sort_by='title_asc', page=1) {
        // Renders all the products in the database
        url = `/api/mangas/${sort_by}/${page}`;
    
        get_products(url).then(data => {
            let product_container = document.querySelector('#products_list');
            product_container.innerHTML = '';

            data.products.forEach(product => {
                let in_cart = false;

                if (product.in_cart) {
                    in_cart = true;
                }

                if (in_cart) {
                    button_cart = '<button type="submit" class="btn btn-secondary add_to_cart" disabled>Añadido al carrito</button>'
                } else {
                    button_cart = '<button type="submit" class="btn btn-secondary add_to_cart">Añadir al carrito</button>'
                }

                let product_html = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body text-center d-flex flex-column justify-content-between">
                                <a href="${self_link}product/${product.id_manga}" class="img-link"><img src="${covers_folder}/${product.image}" class="card-img-top" alt="${product.title}"></a>
                                <div>
                                    <a href=${self_link}product/${product.id_manga} class="link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover"><h5 class="card-title">${product.title}</h5></a>
                                    <p class="card-text fw-bold">${product.price}&euro;</p>
                                    <form class="add_to_cart_form">
                                        <input type="hidden" name="quantity" value="1">
                                        <input type="hidden" name="product_id" value="${product.id_manga }">
                                        ${button_cart}
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                product_container.innerHTML += product_html;
            });
            const products_cart_forms = document.querySelectorAll('.add_to_cart_form');

            products_cart_forms.forEach(function(product_form) {
                const error_add_to_cart = document.querySelector('#error_add_to_cart');

                product_form.addEventListener('submit', function (event) {
                    event.preventDefault();
                    event.stopPropagation();

                    const product_id = product_form['product_id'].value;
                    const quantity = product_form['quantity'].value;

                    fetch('/api/cart/add', {
                        method: 'POST',
                        body: JSON.stringify({
                            product_id,
                            quantity
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }).then(response => {
                        if (response.status === 200) {
                            return response.json();
                        } else {
                            form_alert('Error al añadir el producto al carrito.', 'danger', error_add_to_cart);
                            throw new Error(`HTTP error: ${response.status}`);
                        }
                    }).then(data => {
                        if (data.error) {
                            form_alert('No hay suficiente stock de este producto', 'danger', error_add_to_cart);
                            return;
                        } else {
                            const cart_quantity = document.querySelector('#cart_quantity');
                            const add_to_cart = product_form.querySelector('.add_to_cart');

                            add_to_cart.innerHTML = 'Añadido al carrito';
                            add_to_cart.disabled = true;

                            cart_quantity.innerHTML = ' ' + data.cart_quantity;
                            form_alert('Producto añadido al carrito', 'success', error_add_to_cart);
                        }
                    });
                });
            });

            render_pagination_controls(data.pagination);
        });
    }

    function change_page(page) {
        // Changes the page of the products list using the pagination controls and the select to order the products
        let sort_by = document.querySelector('#order_by').value;
        render_products(sort_by, page);
    }

    function render_pagination_controls(pagination_data) {
        // Renders the pagination controls to change the page of the products list
        let pagination_container = document.querySelector('#pagination_controls');
        pagination_container.innerHTML = '';

        if (pagination_data.has_prev) {
            add_button('Anterior', () => change_page(pagination_data.current_page - 1));
        }

        for (let i = 1; i <= pagination_data.total_pages; i++) {
            add_button(i, () => change_page(i), i === pagination_data.current_page);
        }

        if (pagination_data.has_next) {
            add_button('Siguiente', () => change_page(pagination_data.current_page + 1));
        }
    }

    function add_button(label, clickHandler, isDisabled = false) {
        // Adds buttons to the pagination controls container to be able to change the page of the products list
        let button = document.createElement('button');
        button.textContent = label;
        button.addEventListener('click', clickHandler);
        button.classList.add('btn', 'btn-outline-secondary', 'mx-1'); // Agrega clases de Bootstrap

        if (isDisabled) {
            button.setAttribute('disabled', true);
        }

        document.querySelector('#pagination_controls').appendChild(button);
    }

    // Event of change in the select to order the products
    document.querySelector('#order_by').addEventListener('change', function () {
        let sort_by = this.value;

        // Renders the products list again
        render_products(sort_by, 1);
    });

    render_products();
});
