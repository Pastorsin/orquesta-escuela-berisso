$(document).ready(() => {

    getLocalityWithId(location_id).then(function(result) {
        $('#location').text(result)
    });

    getDocumentTypeWithId(doc_type_id).then(function(result) {
        $('#doc-type').text(result)
    });

    var map = new Map(latlng, 14, { scrollWheelZoom: false })
    map.addRouting();
    var control = map.routingControl;

    var initialMark = map.createMarker(latlng)

    initialMark.on('click', function(e) {
        navigator.geolocation.getCurrentPosition(setUserLocation);
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
    });

    function setUserLocation(pos) {
        let current_coords = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
        };
        control.spliceWaypoints(0, 1, current_coords);
    }
});
