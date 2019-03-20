$('#spinner').spinner('hide');

function confirmDeletion(e) {
    if (!confirm("Are you sure you want to delete?")) {
        e.preventDefault();
    } else {
        $('#form-delete').submit();
    }
};

setTimeout(function () {
    $('#opened').hide()
}, 3500);

let getUrlParameter = function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};