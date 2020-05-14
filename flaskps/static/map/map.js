class Map {
    constructor(centerLocation, zoomLevel, options) {
        this.initMap(centerLocation, zoomLevel, options);
        this.routingControl = null
        this.geocoderControl = null
    }

    initMap(centerLocation, zoomLevel, options) {
        this.map = L.map('map', options).setView(centerLocation, zoomLevel);

        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);
    }

    addRouting() {
        this.routingControl = L.Routing.control({
            reverseWaypoints: true,
            routeWhileDragging: true,
            language: 'es',
            geocoder: L.Control.Geocoder.nominatim()
        }).addTo(this.map);
    }

    addGeocoder() {
        this.geocoderControl = L.Control.geocoder({
            defaultMarkGeocode: false,
        }).addTo(this.map);
    }

    createMultipleMarkers(markers) {
        for (let i = 0; i < markers.length; i++) {
            let mark = this.createMarker(markers[i].pos)
            mark.bindPopup(`<p>${markers[i].name}</p><button>Ir aquí</button>`);
        }
    }

    createMarker(location) {
        return L.marker(location).addTo(this.map);
    }

    static render() {
        const centerLocation = [-34.8777, -57.8818];

        var map = new Map(centerLocation, 14)

        map.addGeocoder()
        var control = map.geocoderControl
        var initialMark = map.createMarker(centerLocation)

        control.on('markgeocode', function (e) {
            let centerDest = e.geocode.center;

            map.map.setView(centerDest, 14);
            initialMark.setLatLng(centerDest);
            setInputsValues(centerDest)
        });

        map.map.on('click', function (e) {
            let clickPos = e.latlng;

            initialMark.setLatLng(clickPos);
            setInputsValues(clickPos)
        });

        function setInputsValues(latlng) {
            $('#lat').attr('value', latlng.lat)
            $('#lng').attr('value', latlng.lng)
        }
        return [map, initialMark]
    }

}
