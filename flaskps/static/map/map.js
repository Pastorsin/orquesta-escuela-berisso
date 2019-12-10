class Map {
    constructor(centerLocation, zoomLevel) {
        this.centerLocation = centerLocation;
        this.zoomLevel = zoomLevel;
        this.initMap();
    }

    initMap() {
        this.map = L.map('map').setView(this.centerLocation, this.zoomLevel);

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

}
