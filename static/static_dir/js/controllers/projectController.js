angular_module.controller('projectController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.selected_project = 'all_projects';
    $scope.summary_project = {};
    $scope.summary_project['name'] = 'All Projects'
    $http.get('/api/').then(function(response) {
        $scope.projects = response.data
        projects = $scope.projects
            // console.log($scope.projects)
        $scope.summary_project['projects'] = response.data
        $scope.summary_project['project_count'] = $scope.projects.length
        $scope.summary_project['task_count'] = 0
        angular.forEach($scope.projects, function(project) {
            $scope.summary_project['task_count'] += project.tasks.length
        })
        console.log($scope.summary_project)
    })
    $scope.current_project = function(selected_project) {
        $scope.selected_project = selected_project
        if ($scope.selected_project != 'all_projects') {
            angular.forEach($scope.projects, function(project) {
                if ($scope.selected_project == project.name) {
                    $scope.tasks = project.tasks
                    $scope.members = project.members
                }
            })
        }
    }
}]);
