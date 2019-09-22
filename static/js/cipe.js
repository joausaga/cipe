// Initialize and add the map
var InforObj = [];
var centerCords = {
    lat: 41.389633,
    lng: 2.116217
};
//window.onload = function () {
//    initMap();
//};
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

function addMarkers(scientists) {
    // Create markers
    //var scientists = {{ scientists|safe }};
    console.log(scientists);
    var inst_lat, inst_lng, str_info_window;
    for (i=0; i < scientists.length; i++) {
        inst_lat = scientists[i].institution_latitude;
        inst_lng = scientists[i].institution_longitude;
        const marker = new google.maps.Marker({position: {lat: inst_lat, lng: inst_lng}, map: map});
        infoWindowContent = "<div class='text-body text-left'><b>" + scientists[i].name + "</b><br>" + scientists[i].institution_name + "</div>";
        const infowindow = new google.maps.InfoWindow({
            content: infoWindowContent
        });
        marker.addListener('click', function () {
            closeInfoWindow();
            infowindow.open(marker.get('map'), marker);
            InforObj[0] = infowindow;
        });
    }
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: centerCords
    });
}