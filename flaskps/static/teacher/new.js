$(document).ready(() => {
    fillDocTypeSelect();
    fillLocalitiesSelect();
});

async function fillDocTypeSelect() {
    let doctypes = await getDocTypes();
    let select = $('.doctype-input');
    let selectVal = select.attr('value');
    doctypes.forEach(function (doctype) {
        element = $('<option />').val(doctype.id).text(doctype.nombre);
        if (doctype.id == selectVal) {
            element.attr('selected', 'selected');
        }
        select.append(element);
    })
}

async function fillLocalitiesSelect() {
    let localities = await getLocalities();
    let select = $('.location-input');
    let selectVal = select.attr('value');
    localities.forEach(function (locality) {
        element = $('<option />').val(locality.partido_id).text(locality.nombre);
        if (locality.id == selectVal) {
            element.attr('selected', 'selected');
        }
        select.append(element);
    })
}