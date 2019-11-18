async function getDocTypes(){
    let response=await fetch('https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento');
    let doctypes=await response.json();
    return doctypes;
}

async function getLocalities(){
    let response=await fetch('https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad');
    let localities=await response.json();
    return localities;
}

function searchID(array, id) {
  return array.find(function(type) { return type.id == id; });
}

async function getDocumentTypeWithId(id) {
  let doctypes = await getDocTypes();
  let documentType = searchID(doctypes, id);
  return documentType.nombre
}

async function getLocalityWithId(id) {
  let localities = await getLocalities();
  let locality = searchID(localities, id);
  return locality.nombre
}
