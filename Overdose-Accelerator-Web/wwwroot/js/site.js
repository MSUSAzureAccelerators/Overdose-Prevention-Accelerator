
function OpenDetails(name) {
    CloseAllDetails();
    var el = document.getElementById(name)
    el.setAttribute('open', 'true');
}

function CloseAllDetails()
{
    $('details').removeAttr('open');
}

function ShowHideDetails(name, isTrue) {

    var el = document.getElementById(name);
    if (isTrue) {
        el.setAttribute('open', 'true');
    } else {
        el.removeAttribute('open');
    }
}