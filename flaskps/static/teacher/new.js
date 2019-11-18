$(document).ready(() => {
    fillDocTypeSelect();
    fillLocalitiesSelect();
});

async function fillDocTypeSelect(){
    let doctypes=await getDocTypes();
    let select=$('#doctype-input');
    doctypes.forEach(function(doctype) {
        select.append($('<option />').val(doctype.id).text(doctype.nombre));
    })
}

async function fillLocalitiesSelect(){
    let localities= await getLocalities();
    let select=$('#location-input');
    localities.forEach(function(locality) {
        select.append($('<option />').val(locality.partido_id).text(locality.nombre));
    })
}
