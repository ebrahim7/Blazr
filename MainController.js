app.controller('MainController', ['$scope', function($scope) {
  $scope.title = 'Top Jobs in Your Area:';
  $scope.jobs = [
  	{
    	title: 'Software Engineer',
    	company: 'Apple',
    	deadline: new Date('2016', '12', '08')
  	},
    {
    	title: 'CEO',
    	company: 'Google',
    	deadline: new Date('2016', '11', '28')
  	}
  ];
  $scope.like = function(index) {
  	$scope.jobs[index].like = true;
	};
  $scope.dislike = function(index) {
  	$scope.jobs[index].dislike = true;
	};
}]);
