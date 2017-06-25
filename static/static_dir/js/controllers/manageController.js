angular_module.controller('manageController', ['$scope', '$http', '$cookies', '$q', function($scope, $http, $cookies, $q) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.company_request = $http.get('/api/company');
    $scope.project_request = $http.get('/api');


    $q.all([$scope.company_request, $scope.project_request]).then(function(values) {
        $scope.company = values[0].data[0];
        $scope.projects = values[1].data;
    })
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

}]);
