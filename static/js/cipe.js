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
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: centerCords
    });
    addMarkers();
}