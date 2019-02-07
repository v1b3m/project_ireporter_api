

function initMap() {
    var myLatlng = {lat: 0.347596, lng: 32.582520};
  
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 8,
      center: myLatlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });
  
    var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: 'Click to zoom',
      draggable:true,
    });
  
    map.addListener('center_changed', function() {
      // 3 seconds after the center of the map has changed, pan back to the
      // marker.
      window.setTimeout(function() {
        map.panTo(marker.getPosition());
      }, 3000);
    });
  
    marker.addListener('click', function() {
      map.setZoom(8);
      map.setCenter(marker.getPosition());
    });

    google.maps.event.addListener(marker, 'dragend', function(evt){
        document.getElementById('xyz').innerHTML = '<h3>Marker dropped: Current Latitude: ' + evt.latLng.lat().toFixed(3) + ' Current Longitude: ' + evt.latLng.lng().toFixed(3) + '</h3>';
    });
    
    google.maps.event.addListener(marker, 'dragstart', function(evt){
        document.getElementById('xyz').innerHTML = '<h3>Currently dragging marker...</h3>';
    });
  }

window.onload = initMap;