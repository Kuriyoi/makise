document.addEventListener("DOMContentLoaded", function () {
    const error_cart = document.querySelector('#error_cart');

    function remove_from_cart(product_id) {
        fetch('/api/cart/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'product_id': product_id
            })
        }).then(response => {
            if (response.status === 302) {
                return response.json();
            } else if (response.ok) {
                location.reload();
            } else {
                form_alert('Error al eliminar el producto del carrito', 'danger', error_cart);
                throw new Error('Error al eliminar el producto del carrito');
            }
        }).then(data => {
            update_cart_ui(data, product_id);
        });
    }

    function update_cart_ui(data, product_id, delete_row=true) {
        if (delete_row) {
            const row_to_remove = document.querySelector(`tr[data-id="${product_id}"]`);

            if (row_to_remove) {
                row_to_remove.remove();
            }
        }

        const total_price = document.querySelector('#total_price');
        const total_price_shipment = document.querySelector('#total_price_shipment');
        const total_price_shipment_button = document.querySelector('#total_price_shipment_button');
        const cart_quantity = document.querySelector('#cart_quantity');

        const total_price_with_shipment = data['total_price'] + 2.99;

        total_price.innerHTML = data['total_price'].toFixed(2) + '&euro;';
        total_price_shipment.innerHTML = total_price_with_shipment.toFixed(2) + '&euro;';
        total_price_shipment_button.innerHTML = 'Pagar ' + total_price_with_shipment.toFixed(2) + '&euro;';
        cart_quantity.innerHTML = ' ' + data['cart_quantity'];
    }

    const remove_from_cart_buttons = document.querySelectorAll('.remove_from_cart');

    remove_from_cart_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();

            const product_id = button.dataset.id;
            remove_from_cart(product_id);
        });
    });

    const product_quantity_inputs = document.querySelectorAll('.product_quantity');

    product_quantity_inputs.forEach(input => {
        input.addEventListener('change', function (event) {
            event.preventDefault();
            event.stopPropagation();

            const product_id = input.dataset.id;
            const quantity = input.value;

            if (quantity <= 0) {
                remove_from_cart(product_id);
                return;
            } else {
                fetch('/api/cart/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        product_id,
                        quantity
                    })
                }).then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        form_alert('Error al actualizar la cantidad del producto', 'danger', error_cart);
                        throw new Error('Error al actualizar la cantidad del producto');
                    }
                }).then(data => {
                    if (data.error) {
                        form_alert('No hay suficiente stock de este producto', 'danger', error_cart);
                        input.value = data['stock'];
                        return;
                    } else {
                        update_cart_ui(data, product_id, delete_row=false);
                        input.value =quantity;
                    }
                });
            }
        });
    });

    const order_form = document.querySelector('#order_form');

    order_form.addEventListener('submit', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const holder_name = order_form['holder_name'].value;
        const expiration_date = order_form['expiration_date'].value;
        const credit_card = order_form['card_number'].value;
        const cvv = order_form['cvv'].value;
        const address = document.querySelector('#order_address').value;

        const holder_name_input = document.querySelector('#holder_name');
        const expiration_date_input = document.querySelector('#expiration_date');
        const credit_card_input = document.querySelector('#card_number');
        const cvv_input = document.querySelector('#cvv');

        let holder_name_valid, expiration_date_valid, credit_card_valid, cvv_valid = false;

        const credit_card_regex = /^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}| 222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12})$/;
        const expiration_date_regex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/g;

        if (holder_name === '') {
            holder_name_valid = false;
            holder_name_input.classList.remove('is-valid');
            holder_name_input.classList.add('is-invalid');
        } else {
            holder_name_valid = true;
            holder_name_input.classList.remove('is-invalid');
            holder_name_input.classList.add('is-valid');
        }

        if (expiration_date === '' || !expiration_date_regex.test(expiration_date)) {
            expiration_date_valid = false;
            expiration_date_input.classList.remove('is-valid');
            expiration_date_input.classList.add('is-invalid');
        } else {
            expiration_date_valid = true;
            expiration_date_input.classList.remove('is-invalid');
            expiration_date_input.classList.add('is-valid');
        }

        if (credit_card === '' || !credit_card_regex.test(credit_card)) {
            credit_card_valid = false;
            credit_card_input.classList.remove('is-valid');
            credit_card_input.classList.add('is-invalid');
        } else {
            credit_card_valid = true;
            credit_card_input.classList.remove('is-invalid');
            credit_card_input.classList.add('is-valid');
        }

        if (cvv === '' || cvv.length !== 3) {
            cvv_valid = false;
            cvv_input.classList.remove('is-valid');
            cvv_input.classList.add('is-invalid');
        } else {
            cvv_valid = true;
            cvv_input.classList.remove('is-invalid');
            cvv_input.classList.add('is-valid');
        }

        if (holder_name_valid && expiration_date_valid && credit_card_valid && cvv_valid) {
            await fetch('/api/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    address
                })
            }).then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    form_alert('Error al realizar el pago', 'danger', error_cart);
                    throw new Error('Error al realizar el pago');
                }
            }).then(data => {
                if (data.error) {
                    form_alert('Error al realizar el pago', 'danger', error_cart);
                    return;
                } else {
                    window.location.href = '/profile';
                }
            });
        }
    });
});
