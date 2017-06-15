angular_module.controller('projectController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.summary_project = {};
    $scope.summary_project['name'] = 'All Projects'
    $http.get('/api/').then(function(response) {
        $scope.projects = response.data
            // console.log($scope.projects)
        $scope.summary_project['projects'] = response.data
    })
    $scope.current_project = function() {
        $scope.selected_project = event.currentTarget.innerHTML
        console.log(event.currentTarget.innerHTML)
    }
}]);
