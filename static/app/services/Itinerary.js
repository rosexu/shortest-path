'use strict';

angular.module('myApp.services', []).service('Itinerary', ['$q', '$http', function($q, $http) {
  var that = this;

  function parseTime(str) {
    var parts = str.split(' ');
    var time = parts[0];
    var ampm = parts[1];
    var timeParts = time.split(':');

    return {
      hours: parseInt(timeParts[0]) + (ampm === 'PM' ? 12 : 0),
      minutes: parseInt(timeParts[1])
    };
  }

  function parsePlaces(places) {
    var dict = {};
    places.forEach(function (place) {
      dict[place.formatted_address] = place.duration * 60;
    });

    return dict;
  }

  this.getItinerary = function (start, places, mode) {
    var startTime = parseTime(start);
    var locations = parsePlaces(places);
    var deferred = $q.defer();

    $http.post('/api/itinerary', {
      start_time: startTime,
      locations: locations,
      mode: mode,
      transit_mode: 'bus',
      transit_preferences: 'less_walking',
      avoid: 'tolls'
    }).then(function(res) {
      var data = res.data.data;
      that.tripLegs = [];
      data.forEach(function (item) {
        that.tripLegs.push(JSON.parse(item));
      });
      deferred.resolve(this.tripLegs);
    }, function (err) {
      deferred.reject(err);
    });
    return deferred.promise;
  };

  this.searchedPlaces = [];
  this.tripLegs = [];
}]);