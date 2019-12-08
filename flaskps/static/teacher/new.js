$(document).ready(() => {
    fillDocTypeSelect();
    fillLocalitiesSelect();


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

    const ceneterLocation = [-34.8777, -57.8818];
    var map = L.map('map').setView(ceneterLocation, 14);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var geocoderControl = L.Control.geocoder({
        defaultMarkGeocode: false,
    }).addTo(map);

    var initialMark = L.marker(ceneterLocation).addTo(map);
    setInputsValues(initialMark.getLatLng());

    geocoderControl.on('markgeocode', function (e) {
        let centerDest = e.geocode.center;

        map.setView(centerDest, 14);
        initialMark.setLatLng(centerDest);
        setInputsValues(centerDest)
    });

    map.on('click', function (e) {
        let clickPos = e.latlng;

        initialMark.setLatLng(clickPos);
        setInputsValues(clickPos)
    });

    function setInputsValues(latlng) {
        $('#lat').attr('value', latlng.lat)
        $('#lng').attr('value', latlng.lng)
    }
});