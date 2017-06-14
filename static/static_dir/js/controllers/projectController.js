angular_module.controller('projectController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.get('/api/').then(function(response) {
        console.log(response.data)
        $scope.projects = response.data
        // console.log($scope.projects)
    })
}]);
