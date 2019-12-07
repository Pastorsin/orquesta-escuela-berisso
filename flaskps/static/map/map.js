var map = L.map('map').setView([-34.8777, -57.8818], 15);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var marker1 = L.marker([-34.87641, -57.8929]).addTo(map);  //EP6
var marker2 = L.marker([-34.88386, -57.89844]).addTo(map);  //EP7
var marker3 = L.marker([-34.8766, -57.8828]).addTo(map);
var marker4 = L.marker([-34.8758, -57.8761]).addTo(map);
var marker5 = L.marker([-34.8698, -57.8727]).addTo(map);

marker1.bindPopup('<p>Escuela primaria Nº6</p><button>Ir aquí</button>');
marker2.bindPopup('<p>Escuela primaria Nº7</p><button>Ir aquí</button>');
marker3.bindPopup('<p>Escuela primaria Nº8</p><button>Ir aquí</button>');
marker4.bindPopup('<p>Escuela primaria Nº9</p><button>Ir aquí</button>');
marker5.bindPopup('<p>Escuela primaria Nº10</p><button>Ir aquí</button>');

var control = L.Routing.control({
    routeWhileDragging: true,
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

function setUserLocation(pos) {
    let current_coords = {
        lat: pos.coords.latitude,
        lng: pos.coords.longitude
    };
    control.spliceWaypoints(0, 1, current_coords);
}