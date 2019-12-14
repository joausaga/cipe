// Initialize and add the map
var InforObj = [];
var centerCords = {
    lat: 41.389633,
    lng: 2.116217
};
var markers = [];
var markerCluster = null;
var twitter_icon = '/static/img/icons/twitter.png';
var gscholar_icon = '/static/img/icons/google-scholar.png';
var facebook_icon = '/static/img/icons/facebook.png';
var scopus_icon = '/static/img/icons/scopus.png';
var instws_icon = '/static/img/icons/globe.png';
var persws_icon = '/static/img/icons/home.png';
var orcid_icon = '/static/img/icons/orcid.png';
var linkedin_icon = '/static/img/icons/linkedin.png';
var researchgate_icon = '/static/img/icons/researchgate.png';
var academia_icon = '/static/img/icons/academia.svg';


function closeInfoWindow() {
    if (InforObj.length > 0) {
        /* detach the info-window from the marker */
        InforObj[0].set("marker", null);
        /* and close it */
        InforObj[0].close();
        /* blank the array */
        InforObj.length = 0;
    }
}

function generateInfoWindowContent(scientist_info) {
    let content = "";
    let position_class = '';
    if (scientist_info.position == 'Estudiante de Doctorado') {
        position_class = 'badge-primary';
    } else {
        if (scientist_info.position == 'Estudiante de Máster Académico') {
            position_class = 'badge-secondary';
        } else {
            if (scientist_info.position == 'Post-doc') {
                position_class = 'badge-warning';
            } else {
                if (scientist_info.position == 'Profesor') {
                    position_class = 'badge-danger';
                } else {
                    position_class = 'badge-info';
                }
            }
        }
    }
    content += "<br>";
    content += "<div>";
    if (scientist_info.sex == 'masculino') {
        content += "<img src='/static/img/man_avatar.svg' alt='avatar_masculino' height='60' width='60' style='display: inline-block; vertical-align: middle; margin-right: 8px;'>";
    } else {
        content += "<img src='/static/img/woman_avatar.svg' alt='avatar_femenino' height='60' width='60' style='display: inline-block; vertical-align: middle; margin-right: 8px;'>";
    }
    content += "<span style='display: inline-block; vertical-align: middle;'><b>" + scientist_info.name + "</b>";
    content += "<br><span class='badge " + position_class + "' float='right'>" + scientist_info.position + "</span><br>";
    content += scientist_info.institution_name + "<br>";
    if (scientist_info.institution_country_iso2 != '') {
        content += "<i class='flag-icon flag-icon-" + scientist_info.institution_country_iso2 + "'></i></span>";

    } else {
        content += scientist_info.institution_country + "</span>";
    }
    content += "</div>";
    content += "<div class='text-left'>"
    content += "<br>Área de investigación<br><b>" + scientist_info.scientific_area + "</b>";
    if (scientist_info.twitter_handler != null || scientist_info.gscholar_profile != null ||
        scientist_info.facebook_profile != null || scientist_info.scopus_profile != null ||
        scientist_info.institutional_website != null || scientist_info.personal_website != null ||
        scientist_info.orcid_profile != null || scientist_info.linkedin_profile != null ||
        scientist_info.researchgate_profile != null || scientist_info.academia_profile != null)
    {
        content = content + "</br><br>";
        if (scientist_info.linkedin_profile != null) {
            content = content + "<a href='" + scientist_info.linkedin_profile +
                               "' target='_blank'><img src='" + linkedin_icon +"' width='32' height='32' title='Perfil Linkedin' alt='Linkedin Logo'></a>";
        }
        if (scientist_info.gscholar_profile != null) {
            content = content + "<a href='" + scientist_info.gscholar_profile +
                               "' target='_blank'><img src='" + gscholar_icon +"' width='32' height='32' title='Perfil Google Scholar' alt='Scholar Logo'></a>";
        }
        if (scientist_info.scopus_profile != null) {
            content = content + "<a href='" + scientist_info.scopus_profile +
                               "' target='_blank'><img src='" + scopus_icon +"' width='32' height='32' title='Perfil Scopus' alt='Scopus Logo'></a>";
        }
        if (scientist_info.researchgate_profile != null) {
            content = content + "<a href='" + scientist_info.researchgate_profile +
                               "' target='_blank'><img src='" + researchgate_icon +"' width='32' height='32' title='Perfil Research Gate' alt='Research Gate Logo'></a>";
        }
        if (scientist_info.academia_profile != null) {
            content = content + "<a href='" + scientist_info.academia_profile +
                               "' target='_blank'><img src='" + academia_icon +"' width='30' height='30' title='Perfil Academia' alt='Academia Logo'></a>";
        }
        if (scientist_info.orcid_profile != null) {
            content = content + "<a href='" + scientist_info.orcid_profile +
                               "' target='_blank'><img src='" + orcid_icon +"' width='32' height='32' title='Perfil ORCID' alt='ORCID Logo'></a>";
        }
        if (scientist_info.institutional_website != null) {
            content = content + "<a href='" + scientist_info.institutional_website +
                               "' target='_blank'><img src='" + instws_icon +"' width='32' height='32' title='Perfil Web Institucional' alt='Scopus Logo'></a>";
        }
        if (scientist_info.personal_website != null) {
            content = content + "<a href='" + scientist_info.personal_website +
                               "' target='_blank'><img src='" + persws_icon +"' width='32' height='32' title='Página Web Personal' alt='Scopus Logo'></a>";
        }
        if (scientist_info.twitter_handler != null) {
            content = content + "<a href='https://twitter.com/" + scientist_info.twitter_handler +
                                "' target='_blank'><img src='" + twitter_icon +"' width='32' height='32' title='Perfil Twitter' alt='Twitter Logo'></a>";
        }
        if (scientist_info.facebook_profile != null) {
            content = content + "<a href='" + scientist_info.facebook_profile +
                               "' target='_blank'><img src='" + facebook_icon +"' width='31' height='31' title='Perfil Facebook' alt='Facebook Logo'></a>";
        }
    }

    content = content + "</div>";
    return content
}

function addMarkers(scientists, isIndex) {
    // Create markers
    let inst_lat, inst_lng, str_info_window;
    let infowindow = new google.maps.InfoWindow();
    let marker;
    let arr_pos = [];
    let new_lat, new_lng;
    markers = [];

    for (i=0; i < scientists.length; i++) {
        inst_lat = scientists[i].institution_latitude;
        inst_lng = scientists[i].institution_longitude;
        pos = {lat: inst_lat, lng: inst_lng};

        // check if a marker with the position pos was already included in the map, if so,
        // modify a bit the position
        for (j = 0; j < arr_pos.length; j++) {
            if (arr_pos[j].lat == pos.lat && arr_pos[j].lng == pos.lng) {
                console.log('Found identifical position');
                new_lat = pos.lat + (Math.random() -.5) / 1500;
                new_lng = pos.lng + (Math.random() -.5) / 1500;
                pos = {lat: new_lat, lng: new_lng};
            }
        }

        marker = new google.maps.Marker({
            position: pos,
            map: map
        });

        if (!isIndex) {
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    //closeInfoWindow();
                    infowindow.setContent(generateInfoWindowContent(scientists[i]));
                    infowindow.open(map, marker);
                }
            })(marker, i));
        }
        markers.push(marker);
        arr_pos.push(pos);
    }
    // Add a marker clusterer to manage the markers.
    markerCluster = new MarkerClusterer(map, markers, {imagePath: '/static/img/markercluster/m'});
}

function removeMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    markerCluster.clearMarkers();
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: centerCords
    });
}

function addMarker(map, latitude, longitude, place_name) {
    latitude = parseInt(latitude);
    longitude = parseInt(longitude);
    var infowindow = new google.maps.InfoWindow({
        content: place_name
    });
    var marker = new google.maps.Marker({
        position: {lat: latitude, lng: longitude},
        map: map
    });
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}

function showCommunicationField() {
    if(document.getElementById('id_communication_channel').options[document.getElementById('id_communication_channel').selectedIndex].value == "telegram") {
        document.getElementById('id_phone_number').style.display = '';
        document.getElementById('id_facebook_profile').style.display = 'none';
    }
    if(document.getElementById('id_communication_channel').options[document.getElementById('id_communication_channel').selectedIndex].value == "whatsapp") {
        document.getElementById('id_phone_number').style.display = '';
        document.getElementById('id_facebook_profile').style.display = 'none';
    }
    if(document.getElementById('id_communication_channel').options[document.getElementById('id_communication_channel').selectedIndex].value == "slack") {
        document.getElementById('id_phone_number').style.display = 'none';
        document.getElementById('id_facebook_profile').style.display = 'none';
    }
    if(document.getElementById('id_communication_channel').options[document.getElementById('id_communication_channel').selectedIndex].value == "lista_correo") {
        document.getElementById('id_phone_number').style.display = 'none';
        document.getElementById('id_facebook_profile').style.display = 'none';
    }
    if(document.getElementById('id_communication_channel').options[document.getElementById('id_communication_channel').selectedIndex].value == "facebook") {
        document.getElementById('id_phone_number').style.display = 'none';
        document.getElementById('id_facebook_profile').style.display = '';
    }
}

function showBecalEndDate() {
    if(document.getElementById('id_has_becal_scholarship').options[document.getElementById('id_has_becal_scholarship').selectedIndex].value == "True") {
        document.getElementById('id_end_becal_scholarship').style.display = '';
        document.querySelector('label[for=id_end_becal_scholarship]').style.display = '';
    } else {
        document.getElementById('id_end_becal_scholarship').style.display = 'none';
        document.querySelector('label[for=id_end_becal_scholarship]').style.display = 'none';
    }

}

function initAutocomplete() {
    var map = new google.maps.Map(document.getElementById('map-registration'), {
      center: {lat: 41.389633, lng: 40.116217},
      zoom: 2,
      mapTypeId: 'roadmap'
    });

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function(marker) {
            marker.setMap(null);
        });

        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            // Set the value of the hidden fields
            document.getElementById("id_location_name").value = place.name;
            document.getElementById("id_location_lat").value = place.geometry.location.lat();
            document.getElementById("id_location_lng").value = place.geometry.location.lng();

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            }));

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });
    return map;
}