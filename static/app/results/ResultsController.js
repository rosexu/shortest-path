'use strict';

angular.module('myApp.results', []).controller('ResultsController', ['Itinerary', '$scope',
	function(Itinerary, $scope) {

		if (!Itinerary.searchedPlaces || !Itinerary.markers) {
			return;
		}

		$scope.places = Itinerary.searchedPlaces;
		sortPlaces();
		$scope.tripLegs = Itinerary.tripLegs;
		sanitizeTime();

		function sortPlaces() {
			if(!$scope.tripLegs) return;
			var sortedPlaces = [];
			var firstPlace = places.filter(function(pl) {
				return pl.formatted_address === tripLegs[0].start_loc;
			});
			sortedPlaces.push(firstPlace);
			tripLegs.forEach(function(leg) {
				var place = places.filter(function(pl) {
					return pl.formatted_address === leg.end_loc;
				});
				sortedPlaces.push(place);
			});
			$scope.places = sortedPlaces;
		}

		function sanitizeTime() {
			$scope.tripLegs.forEach(function(leg) {
				var hour = leg.travel_duration / 3600;
				var temp_min = leg.travel_duration % 3600;
				var min = temp_min / 60;
				leg.travel_duration = {
					hour: Math.floor(hour),
					min: Math.floor(min),
				}

				var startTimeMin = leg.start_time.minute;
				debugger;
				leg.start_time.minute = ('0' + startTimeMin).slice(-2);
			})
		}

    var directionsDisplay;
    var directionsService = new google.maps.DirectionsService();

    initialize();
    function initialize () {
      directionsDisplay = new google.maps.DirectionsRenderer();
      directionsDisplay.setMap(map);

      calcRoute();
    }

    function calcRoute () {
      var request = {};
      var currentLeg, waypoints = [];
      var travelMode = (Itinerary.travelMode || google.maps.TravelMode.DRIVING).toUpperCase();
      var startTime = Itinerary.startTime;

      for (var leg = 0; leg < Itinerary.tripLegs.length; leg++) {
        currentLeg = Itinerary.tripLegs[leg];
        if (leg === 0) {
          request.origin = currentLeg.start_loc;
          if (leg === Itinerary.tripLegs.length - 1) {
            request.destination = currentLeg.end_loc;
          }
        } else if (leg === Itinerary.tripLegs.length - 1) {
          request.destination = currentLeg.end_loc;
          waypoints.push({ location: currentLeg.start_loc });
        } else {
          waypoints.push({ location: currentLeg.start_loc });
        }
      }

      if (travelMode === google.maps.TravelMode.DRIVING) {
        request.drivingOptions = {
          departureTime: new Date('2016', '01', '14', startTime.hour, startTime.minute, 0, 0)
        }; 
      } else if (travelMode === google.maps.TravelMode.TRANSIT) {
        request.transitOptions = {
          departureTime: new Date('2016', '01', '14', startTime.hour, startTime.minute, 0, 0)
        }; 
      }
      
      _.extend(request, {
        waypoints: waypoints,
        travelMode: travelMode
      });

      directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(result);
        }
      });
    }
}]);