angular_module.controller('projectController', function($scope, $http, $cookies, $mdToast) {
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.submit = function($event) {
        $event.preventDefault();
        var in_data = jQuery.param({
            'name': $scope.name,
            'csrfmiddlewaretoken': $cookies.csrftoken
        });

        $http({
            method: 'POST',
            url: 'url{% todo:home %}',
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
});
