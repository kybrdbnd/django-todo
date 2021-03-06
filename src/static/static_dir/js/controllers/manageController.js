angular_module.controller('manageController', ['$scope', '$http', '$cookies', '$q', function($scope, $http, $cookies, $q) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.new_project_member_id = ""
    $scope.dragged_project_id = ""

    $scope.init = function() {
        $scope.company_request = $http.get('/api/company');
        $scope.project_request = $http.get('/api/company-projects');
        $q.all([$scope.company_request, $scope.project_request]).then(function(values) {
            $scope.company = values[0].data[0];
            $scope.projects = values[1].data;
        })
    }
    $scope.refreshProjects = function() {
        $http.get('/api/company-projects').then(function(response) {
            $scope.projects = response.data;
        })
    }
    $scope.addProject = function(projectName) {
        if (projectName != undefined) {
            url = '/todo/add_project/'
            data = $.param({ project_name: projectName })
            $http.post(url, data).then(function(response) {
                $scope.name = "";
                $('.modal').modal('close');
                Materialize.toast('Project Added Successfully', 2000, 'rounded')
                $http.get('/api').then(function(project) {
                    $scope.projects = project.data
                });
            })
        }
    }
    $scope.sendInvite = function(email) {
        if (email != undefined) {
            url = '/todo/send_invite/'
            data = $.param({ email: email })
            $http.post(url, data).then(function(response) {
                $scope.email = ""
                $('.modal').modal('close');
                Materialize.toast('Mail Send Successfully', 2000, 'rounded')
            })
        }
    }
    $scope.memberDragging = function(event) {
        $scope.new_project_member_id = event.target.id
    }
    $scope.addMember = function(event) {
        $scope.dragged_project_id = event.target.id
        url = '/todo/add_member/'
        data = $.param({
            project_id: $scope.dragged_project_id,
            member_id: $scope.new_project_member_id
        })
        $http.post(url, data).then(function(response) {
            Materialize.toast(response.data.message, 2000, 'rounded')
            $scope.refreshProjects();
        })
    }
    $scope.deleteProject = function(project_id) {
        var project_delete_url = '/todo/delete_project/' + project_id + "/"
        $http.post(project_delete_url).then(function(response) {
            Materialize.toast(response.data.message, 2000, 'rounded')
            if (response.data.status) {
                $scope.refreshProjects();
            }
        })
    }
    $scope.init();

}]);