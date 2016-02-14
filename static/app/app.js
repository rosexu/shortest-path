'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', ['ngRoute','myApp.main', 'myApp.results', 'myApp.services'])
  .config(['$routeProvider',
    function($routeProvider) {
      $routeProvider
        .when('/', {
          templateUrl: 'static/app/main/mainView.html',
          controller: 'MainController'
        })
        .when('/results', {
          templateUrl: 'static/app/results/resultsView.html',
          controller: 'ResultsController'
        })
        .otherwise({
          redirectTo: '/'
        });
    }
  ]
);
