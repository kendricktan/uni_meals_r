// Variables for storing location data
var address, country = {}, state = {}, city, suburb, postal_code, coordinates_latitude, coordinates_longitude; 

// Getters
function getAddress(){
    return address;
}

function getCountry(isLongName){
    if (isLongName || isLongName == null){
        return country['long_name'];
    }
    return country['short_name'];
}

function getState(isLongName){
    if (isLongName || isLongName == null){
        return state['long_name'];
    }
    return state['short_name'];
}

function getCity(){
    return city;
}

function getSuburb(){
    return suburb;
}

function getPostal_code(){
    return postal_code;
}

function getCoordinates_latitude(){
    return coordinates_latitude;
}

function getCoordinates_longitude(){
    return coordinates_longitude;
}

// Settings for getting user location

// Options for geolocation
var options = {
	enableHighAccuracy: true,
	timeout: 5000,
	maximumAge: 0
};

// If geolocator is able to get coordinates from IP
function success(pos){
	var crd = pos.coords;

	coordinates_latitude = crd.latitude;
	coordinates_longitude = crd.longitude;
	
	console.log("Latitude: " + coordinates_latitude);
	console.log("Longitude: " + coordinates_longitude);
	
	latlng_getDetails(crd.latitude, crd.longitude);
}

// Logs error
function error(err){
	console.log('Error(' + err.code +'): ' + err.message);
}        

// Gets details for location data (if success)
function latlng_getDetails(lat, lng) {
	var latlng = new google.maps.LatLng(lat, lng);
	var geocoder = new google.maps.Geocoder();
	
	geocoder.geocode({
		'latLng' : latlng
	}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			if (results[1]) {

				var arrAddress = results;
				//console.log(results);
				// iterate through address_component array
				$.each(
					arrAddress,
					function(i, address_component) {
						// Address
						if(address_component.types[0] == "street_address"){
							address = address_component.formatted_address;
							console.log("Address: " + address);
						}
						
						// Country, State, & City
						if (address_component.types[0] == "colloquial_area") {
							city = address_component.address_components[0].long_name;
							console.log("City: " + city);              
							
							state['long_name'] = address_component.address_components[1].long_name; // Queensland
							state['short_name'] = address_component.address_components[1].short_name; // QLD
							console.log("State: " + JSON.stringify(state));
							
							country['long_name'] = address_component.address_components[2].long_name; // Australia
							country['short_name'] = address_component.address_components[2].short_name; // AU
							console.log("Country: " + JSON.stringify(country));
						}
						
						// Suburb
						if (address_component.types[0] == "locality"){
							suburb = address_component.address_components[0].long_name;
							console.log("Suburb: " + suburb);
						}
						
						// Postal code
						if (address_component.types[0] == "postal_code"){
							postal_code = address_component.address_components[0].long_name;
							console.log("Postal Code: " + postal_code);
						}
					});

			} else {
				console.log("No results found");
			}
		} else {
			console.log("Geocoder failed due to: " + status);
		}
	});
}

function initialize() {        
    // Gets current latitude + longitude
	navigator.geolocation.getCurrentPosition(success, error, options);
}