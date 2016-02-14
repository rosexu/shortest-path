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

		console.log('present new info here');
		console.log(Itinerary.searchedPlaces, Itinerary.markers, Itinerary.tripLegs);
}]);