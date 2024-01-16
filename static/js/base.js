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

const pyToJSDateFormats = Object.freeze({
    '%A': 'dddd',
    '%a': 'ddd',
    '%B': 'MMMM',
    '%b': 'MMM',
    '%c': 'ddd MMM DD HH:mm:ss YYYY',
    '%d': 'DD',
    '%f': 'SSS',
    '%H': 'HH',
    '%I': 'hh',
    '%j': 'DDDD',
    '%M': 'mm',
    '%m': 'MM',
    '%p': 'A',
    '%S': 'ss',
    '%U': 'ww',
    '%W': 'ww',
    '%w': 'd',
    '%X': 'HH:mm:ss',
    '%x': 'MM/DD/YYYY',
    '%Y': 'YYYY',
    '%y': 'YY',
    '%Z': 'z',
    '%z': 'ZZ',
    '%%': '%'
  });

function convertPYDateFormatToJS(formatStr){
    for(let key in pyToJSDateFormats){
        formatStr = formatStr.split(key).join(pyToJSDateFormats[key]);
    }
    return formatStr;
}
