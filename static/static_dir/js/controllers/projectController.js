angular_module.controller('projectController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.selected_date = "";
    $scope.selected_project = 'all_projects';
    $scope.projects = "";
    $scope.project_id = "";
    $scope.summary_project = {};
    $scope.summary_project['name'] = 'All Projects';

    $scope.init = function() {
        $http.get('/api/').then(function(response) {
            $scope.projects = response.data
            projects = $scope.projects
            $scope.summary_project['projects'] = response.data
            $scope.summary_project['project_count'] = $scope.projects.length
            $scope.summary_project['task_count'] = 0
            angular.forEach($scope.projects, function(project) {
                $scope.summary_project['task_count'] += project.tasks.length
            })
        })
    }
    $scope.current_project = function(selected_project, selected_project_id) {
        $scope.selected_project = selected_project
        if (selected_project_id != 0) {
            $scope.project_id = selected_project_id
            if ($scope.selected_project != 'all_projects') {
                project_detail_url = "/api/project/" + $scope.project_id
                $http.get(project_detail_url).then(function(response) {
                    temp_tasks = response.data.tasks;
                    display_tasks = [];
                    angular.forEach(temp_tasks, function(task) {
                        if (task.assigned_to == null) {
                            display_tasks.push(task)
                        }
                    })
                    $scope.tasks = display_tasks;
                    $scope.members = response.data.members
                })
            }
        }
    }
    $scope.addtask = function() {
        if ($scope.task != "") {
            url = '/todo/add_task/'
            data = $.param({ project_id: $scope.project_id, task_name: $scope.task })
            $http.post(url, data).then(function(response) {
                $scope.task = "";
                project_detail_url = "/api/project/" + $scope.project_id
                $http.get(project_detail_url).then(function(response) {
                    temp_tasks = response.data.tasks;
                    display_tasks = [];
                    angular.forEach(temp_tasks, function(task) {
                        if (task.assigned_to == null) {
                            display_tasks.push(task)
                        }
                    })
                    $scope.tasks = display_tasks;

                })
                Materialize.toast('Task Added', 2000, 'rounded')
            })
            $scope.update_task_count();
        }
    }
    $scope.update_task_count = function() {
        var projects;
        // just for update
        $http.get('/api/').then(function(response) {})
            //actual updation
        $http.get('/api/').then(function(response) {
            $scope.summary_project['task_count'] = 0
            projects = response.data
            angular.forEach(projects, function(project) {
                $scope.summary_project['task_count'] += project.tasks.length
            })
        })
    }
    $scope.selectedDate = function(click) {
        $scope.selected_date = click.currentTarget.innerText
        console.log($scope.selected_date)

    }
    $scope.assignYourself = function(task_id) {
        console.log(task_id)
    }
    $scope.init();
}]);
