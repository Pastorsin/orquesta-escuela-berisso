const ceneter_location = [-34.8777, -57.8818]
const schools = [
    {
        pos: [-34.87641, -57.8929],
        name: 'Escuela primaria Nº6'
    },
    {
        pos: [-34.88386, -57.89844],
        name: 'Escuela primaria Nº7'
    },
    {
        pos: [-34.8766, -57.8828],
        name: 'Escuela primaria Nº8'
    },
    {
        pos: [-34.8758, -57.8761],
        name: 'Escuela primaria Nº9'
    },
    {
        pos: [-34.8698, -57.8727],
        name: 'Escuela primaria Nº10'
    },
]

var map = L.map('map').setView(ceneter_location, 15);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

createMarkers(schools);

var control = L.Routing.control({
    reverseWaypoints: true,
    routeWhileDragging: true,
    language: 'es',
    geocoder: L.Control.Geocoder.nominatim()
}).addTo(map);

map.on('popupopen', function (e) {
    let btn = document.querySelector('.leaflet-popup-content > button')

    L.DomEvent.on(btn, 'click', function () {
        navigator.geolocation.getCurrentPosition(setUserLocation);
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.popup._latlng);
        map.closePopup();
    });
});

function createMarkers() {
    for (let i = 0; i < schools.length; i++) {
        let x = L.marker(schools[i].pos).addTo(map);
        x.bindPopup(`<p>${schools[i].name}</p><button>Ir aquí</button>`);
    }
}

function setUserLocation(pos) {
    let current_coords = {
        lat: pos.coords.latitude,
        lng: pos.coords.longitude
    };
    control.spliceWaypoints(0, 1, current_coords);
}