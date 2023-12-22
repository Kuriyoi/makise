document.addEventListener("DOMContentLoaded", function () {
    const add_to_cart_form = document.querySelector('#add_to_cart_form');
    const error_add_to_cart = document.querySelector('#error_add_to_cart');

    add_to_cart_form.addEventListener('submit', function (event) {
        event.preventDefault();
        event.stopPropagation();

        const product_id = add_to_cart_form['product_id'].value;
        const quantity = add_to_cart_form['quantity'].value;

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
                const add_to_cart = document.querySelector('#add_to_cart');

                add_to_cart.innerHTML = 'Añadido al carrito';
                add_to_cart.disabled = true;

                cart_quantity.innerHTML = ' ' + data.cart_quantity;
                form_alert('Producto añadido al carrito', 'success', error_add_to_cart);
            }
        });
    });
});
