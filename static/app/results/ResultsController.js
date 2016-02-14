'use strict';

angular.module('myApp.results', []).controller('ResultsController', ['Itinerary', '$scope',
	function(Itinerary, $scope) {

		if (!Itinerary.searchedPlaces || !Itinerary.markers) {
			return;
		}

		$scope.places = Itinerary.searchedPlaces;
		$scope.tripLegs = Itinerary.tripLegs;
		sortPlaces();
		sanitizeTime();

		function sortPlaces() {
			var map = new Object();
			for (var i = 0; i < $scope.places.length; i++){
				var pl = $scope.places[i];
				map[pl.formatted_address] = pl;
			}

			var sortedPlaces = [];
			sortedPlaces.push(map[$scope.tripLegs[0].start_loc]);
			for (var j = 0; j < $scope.tripLegs.length; j++) {
				var place =  $scope.tripLegs[j].end_loc;
				sortedPlaces.push(map[place]);
			}

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
			})
		}

		console.log('present new info here');
		console.log(Itinerary.searchedPlaces, Itinerary.markers, Itinerary.tripLegs);
}]);