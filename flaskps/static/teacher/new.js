$(document).ready(() => {
    fillDocTypeSelect();
    fillLocalitiesSelect();
});

async function getDocTypes(){
    let response=await fetch('https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento');
    let doctypes=await response.json();
    return doctypes;
}

async function fillDocTypeSelect(){
    let doctypes=await getDocTypes();
    let select=$('#doctype-input');
    doctypes.forEach(function(doctype) {
        select.append($('<option />').val(doctype.id).text(doctype.nombre));
    })
}

async function getLocalities(){
    let response=await fetch('https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad');
    let localities=await response.json();
    return localities;
}

async function fillLocalitiesSelect(){
    let localities= await getLocalities();
    let select=$('#location-input');
    localities.forEach(function(locality) {
        select.append($('<option />').val(locality.partido_id).text(locality.nombre));
    })
}