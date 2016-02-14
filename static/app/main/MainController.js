'use strict';

angular.module('myApp.main', []).controller('MainController', ['$scope', '$timeout', function($scope, $timeout) {
  var markers = [];
  $scope.places = [];
  $scope.selectMode = 'driving';
  $scope.travelOptions = [{
    name: 'driving',
    prettyName: 'Driving'
  }, {
    name: 'walking',
    prettyName: 'Walking'
  }, {
    name: 'bicycling',
    prettyName: 'Bicycling'
  }, {
    name: 'transit',
    prettyName: 'Transit'
  }];

  retryInit();

  function retryInit () {
    if (!window.google || !window.map) {
      $timeout(retryInit, 500);
    } else {
      initController();
    }
  }

  function initController () {
    var input = document.getElementById('pac-input');
    var types = document.getElementById('type-selector');

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    var infowindow = new google.maps.InfoWindow();

    autocomplete.addListener('place_changed', function() {
      infowindow.close();

      var place = autocomplete.getPlace();
      if (!place.geometry) {
        return;
      }

      $scope.places.push(place);
      $scope.$apply();

      //Marker
      var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        animation: google.maps.Animation.DROP
      });
      marker.setIcon(/** @type {google.maps.Icon} */({
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(35, 35)
      }));
      markers.push(marker);

      //Infowindow
      var address = '';
      if (place.address_components) {
        address = [
          (place.address_components[0] && place.address_components[0].short_name || ''),
          (place.address_components[1] && place.address_components[1].short_name || ''),
          (place.address_components[2] && place.address_components[2].short_name || '')
        ].join(' ');
      }

      infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
      infowindow.open(map, marker);

      showAllMarkersOnMap();
      input.value = '';
    });
  }

  function showAllMarkersOnMap() {
    var bounds = new google.maps.LatLngBounds();

    // Create bounds from markers
    for( var index in markers ) {
        var latlng = markers[index].getPosition();
        bounds.extend(latlng);
    }

    // Don't zoom in too far on only one marker
    if (bounds.getNorthEast().equals(bounds.getSouthWest())) {
       var extendPoint1 = new google.maps.LatLng(bounds.getNorthEast().lat() + 0.01, bounds.getNorthEast().lng() + 0.01);
       var extendPoint2 = new google.maps.LatLng(bounds.getNorthEast().lat() - 0.01, bounds.getNorthEast().lng() - 0.01);
       bounds.extend(extendPoint1);
       bounds.extend(extendPoint2);
    }

    map.fitBounds(bounds);
  }


  $scope.removePlace = function (idx) {
    markers[idx].setMap(null);
    markers[idx] = null;
    markers.splice(idx, 1);

    $scope.places.splice(idx, 1);
  };

  $scope.updateMode = function (option) {
    $scope.selectMode = option;
  };
}]);