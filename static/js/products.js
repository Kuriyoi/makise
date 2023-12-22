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
                let product_html = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body text-center">
                                <a href=${self_link}product/${product.id_manga}><img src="${covers_folder}/${product.image}" class="card-img-top" alt="${product.title}"></a>
                                <a href=${self_link}product/${product.id_manga} class="link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover"><h5 class="card-title">${product.title}</h5></a>
                                <p class="card-text fw-bold">${product.price}&euro;</p>
                                <p class="card-text">Fecha de salida: ${product.added_date}</p>
                            </div>
                        </div>
                    </div>
                `;
                product_container.innerHTML += product_html;
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

    // Evento de cambio en el select para ordenar los productos
    document.querySelector('#order_by').addEventListener('change', function () {
        let sort_by = this.value;

        // Volver a renderizar la lista de productos
        render_products(sort_by, 1);
    });

    render_products();
});
