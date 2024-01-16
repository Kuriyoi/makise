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

    const review_form_edit = document.querySelector('#review_form_edit');
    const edit_review_form = document.querySelector('#edit_review_form');
    const edit_review_form_submit = document.querySelector('#edit_review_form_submit');

    if (edit_review_form) {
        edit_review_form.addEventListener('click', function () {
            edit_review_form.style.display = 'none';
            edit_review_form_submit.style.display = 'block';

            review_form_edit['comment'].disabled = false;
            review_form_edit['rating'].disabled = false;
        });
    }

    if (review_form_edit) {
        review_form_edit.addEventListener('submit', function () {
            edit_review_form.style.display = 'block';
            edit_review_form_submit.style.display = 'none';

            review_form_edit['comment'].disabled = true;
            review_form_edit['rating'].disabled = true;

            const manga = review_form_edit['product_id'].value;
            const comment = review_form_edit['comment'].value;
            const rating = parseFloat(review_form_edit['rating'].value);

            fetch(`/api/review/${manga}`, {
                method: 'PUT',
                body: JSON.stringify({
                    comment,
                    rating,
                    manga
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    form_alert('Error al editar la reseña.', 'danger', error_review);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(data => {
                form_alert('Reseña editada correctamente', 'success', error_review);
                const review_comment = document.querySelector('#review_comment');
                const review_rating = document.querySelector('#review_rating');

                review_comment.innerHTML = data.comment;
                review_rating.innerHTML = data.rating;
            });
        });
    }

    const add_review_form = document.querySelector('#add_review_form');
    console.log(add_review_form);

    if (add_review_form) {
        add_review_form.addEventListener('submit', function () {
            console.log('submit');
            const manga = add_review_form['product_id'].value;
            const comment = add_review_form['comment'].value;
            const rating = parseFloat(add_review_form['rating'].value);

            fetch(`/api/review`, {
                method: 'POST',
                body: JSON.stringify({
                    comment,
                    rating,
                    manga
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    form_alert('Error al añadir la reseña.', 'danger', error_review);
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(data => {
                form_alert('Reseña añadida correctamente', 'success', error_review);
                const review_comment = document.querySelector('#review_comment');
                const review_rating = document.querySelector('#review_rating');

                review_comment.innerHTML = data.comment;
                review_rating.innerHTML = data.rating;
            });
        });
    }
});
