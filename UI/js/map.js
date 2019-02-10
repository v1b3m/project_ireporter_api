/* global document, window, google */

function initMap() {
  const myLatlng = { lat: 0.347596, lng: 32.582520 };
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
  const marker = new google.maps.Marker({
    position: myLatlng,
    map,
    title: 'Click to zoom',
    draggable: true,
  });

  map.addListener('center_changed', () => {
    // 3 seconds after the center of the map has changed, pan back to the
    // marker.
    window.setTimeout(() => {
      map.panTo(marker.getPosition());
    }, 3000);
  });

  marker.addListener('click', () => {
    map.setZoom(8);
    map.setCenter(marker.getPosition());
  });

  google.maps.event.addListener(marker, 'dragend', (evt) => {
    document.getElementById('location').value = `Lat: ${evt.latLng.lat().toFixed(3)}, Long: ${evt.latLng.lng().toFixed(3)}`;
    document.getElementById('xyz').innerHTML = 'Move the marker to get longitude and latitude of location';
  });

  google.maps.event.addListener(marker, 'dragstart', () => {
    document.getElementById('xyz').innerHTML = 'Currently dragging marker...';
  });
}

window.onload = initMap;
