app.controller('MainController', ['$scope', function($scope) {
	$scope.title = 'Top Jobs in Your Area:';
	$scope.like = function(index) {
		$scope.jobs[index].like = true;
	};
	$scope.dislike = function(index) {
		$scope.jobs[index].dislike = true;
	};
  
  $scope.toggle = [];
  $scope.jobDescToggle = function(index) {
    console.log('toggled: '+index +' to: '+!$scope.toggle[index])
    $scope.toggle[index] = !$scope.toggle[index];
  };
  
  console.log('MainController.js loaded')
}]);
