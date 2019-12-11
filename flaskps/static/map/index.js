const centerLocation = [-34.8777, -57.8818]
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

var map = new Map(centerLocation, 15);
map.addRouting()
map.createMultipleMarkers(schools)

var control = map.routingControl

map.map.on('popupopen', function (e) {
    let btn = document.querySelector('.leaflet-popup-content > button')

    L.DomEvent.on(btn, 'click', function () {
        navigator.geolocation.getCurrentPosition(setUserLocation);
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.popup._latlng);
        map.map.closePopup();
    });
});

function setUserLocation(pos) {
    let current_coords = {
        lat: pos.coords.latitude,
        lng: pos.coords.longitude
    };
    control.spliceWaypoints(0, 1, current_coords);
}
