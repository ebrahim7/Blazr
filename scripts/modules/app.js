var app = angular.module("myApp", ['ngAnimate']);

app.filter("trust", ['$sce', function($sce) {
  return function(htmlCode){
    return $sce.trustAsHtml(htmlCode);
  }
}]);

console.log('app.js loaded')