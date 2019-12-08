$(document).ready(() => {
    
    // Esto se debe al doble llamado de super() en el HTML
    $('#tutor-section #map').attr('id', 'map2')
    $('#tutor-section #lat').attr('id', 'lat2')
    $('#tutor-section #lng').attr('id', 'lng2')

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

    // Me siento mal

    var tutorMap = L.map('map2').setView(ceneterLocation, 14);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(tutorMap);

    var geocoderControlTutor = L.Control.geocoder({
        defaultMarkGeocode: false,
    }).addTo(tutorMap);

    var initialMarkTutor = L.marker(ceneterLocation).addTo(tutorMap);
    setInputsValues(initialMarkTutor.getLatLng());

    geocoderControlTutor.on('markgeocode', function (e) {
        let centerDest = e.geocode.center;

        tutorMap.setView(centerDest, 14);
        initialMarkTutor.setLatLng(centerDest);
        setInputsValues(centerDest)
    });

    tutorMap.on('click', function (e) {
        let clickPos = e.latlng;

        initialMarkTutor.setLatLng(clickPos);
        setInputsValues(clickPos)
    });

    function setInputsValues(latlng) {
        $('#lat2').attr('value', latlng.lat)
        $('#lng2').attr('value', latlng.lng)
    }
});