// Creates an alert when there is an error in a form
function form_alert(message, type='secondary', alert_placeholder) {
    let wrapper = document.createElement('div');
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert" data-timeout="2000">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';

    alert_placeholder.append(wrapper);

    // Close alert after 5 seconds
    window.setTimeout(function () {
        wrapper.remove();
    }, 5000);
}
