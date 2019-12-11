function render_map() {
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

}