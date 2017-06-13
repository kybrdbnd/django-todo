angular_module.controller('projectController', ['$scope', '$http', '$cookies', '$mdToast', function($scope, $http, $cookies, $mdToast) {
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.submit = function($event) {
        $event.preventDefault();
        var in_data = jQuery.param({
            'name': $scope.name,
        });

        $http({
            method: 'POST',
            url: '/todo/',
            data: in_data
        }).then(function success(response) {
            $mdToast.show(
                $mdToast.simple()
                .textContent(response.data.success)
                .position('right')
                .hideDelay(1000)
            );
        })
    }
}]);
