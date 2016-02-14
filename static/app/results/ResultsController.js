'use strict';

angular.module('myApp.results', []).controller('ResultsController', ['Itinerary', function(Itinerary) {
	
	if (!Itinerary.searchedPlaces || !Itinerary.markers) {
		return;
	}

	console.log('present new info here');
	console.log(Itinerary.searchedPlaces, Itinerary.markers, Itinerary.tripLegs);
}]);