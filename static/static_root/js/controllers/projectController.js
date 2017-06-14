angular_module.controller('projectController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.projects = []
    $http.get('/api/').then(result) - >
        angular.forEach result.data, (item) - >
        $scope.projects.push(item)



    // $scope.submit = function($event) {
    //     $event.preventDefault();
    //     var in_data = jQuery.param({
    //         'name': $scope.name,
    //     });

    //     $http({
    //         method: 'POST',
    //         url: '/todo/',
    //         data: in_data
    //     }).then(function success(response) {
    //         $mdToast.show(
    //             $mdToast.simple()
    //             .textContent(response.data.success)
    //             .position('right')
    //             .hideDelay(1000)
    //         );
    //     })
    // }
    console.log($scope.projects)
}]);
