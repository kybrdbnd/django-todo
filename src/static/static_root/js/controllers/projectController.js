angular_module.controller('projectController', ['$scope', '$http', '$cookies', '$q', function($scope, $http, $cookies, $q) {

    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $scope.selected_date = "";
    $scope.selected_project = 'all_projects';
    $scope.projects = "";
    $scope.project_id = "";
    $scope.summary_project = {};
    $scope.summary_project['name'] = 'All Projects';
    $scope.taskAssignDate = "";
    $scope.members = {};
    $scope.otherMember = "";
    $scope.showPutBack = false;
    $scope.reason = "";

    $scope.init = function() {
        $scope.unformat_date = new Date();

        function pad(s) {
            return (s < 10) ? '0' + s : s;
        }
        $scope.selected_date = [$scope.unformat_date.getFullYear(), pad($scope.unformat_date.getMonth() + 1), pad($scope.unformat_date.getDate())].join('-');
        $scope.selected_project_request = $http.get('/api/');
        $scope.today_tasks_request = $http.get('/api/tasks/');
        $q.all([$scope.selected_project_request, $scope.today_tasks_request]).then(function(value) {
            $scope.projects = value[0].data;
            $scope.summary_project['project_count'] = value[0].data.length;
            $scope.summary_project['tasks'] = value[1].data;
            $scope.summary_project['task_count'] = value[1].data.length;
        })
    }
    $scope.updateSummary = function() {
        $http.get('/api/tasks/').then(function(response) {
            $scope.summary_project['tasks'] = response.data;
            $scope.summary_project['task_count'] = response.data.length;
        })
    }
    $scope.updateQueue = function() {
        temp_queue = [];
        project_detail_url = "/api/project/" + $scope.project_id;
        $http.get(project_detail_url).then(function(response) {
            angular.forEach(response.data.tasks, function(task) {
                if (task.assigned_to == null) {
                    temp_queue.push(task);
                }
            })
            $scope.queue = temp_queue;
            $scope.members = response.data.members
        })
    }
    $scope.current_project = function(selected_project, selected_project_id) {
        $scope.tasks = "";
        $scope.selected_project = selected_project
        $('#showongoing').attr('checked', false);
        if (selected_project == 'all_projects') {
            $scope.updateSummary();
        }
        if (selected_project_id != 0) {
            $scope.project_id = selected_project_id
            if ($scope.selected_project != 'all_projects') {
                $scope.updateQueue();
            }
            if ($scope.selected_date != "") {
                project_date_url = "/api/project/" + $scope.project_id + "/task/date/" + $scope.selected_date
                $http.get(project_date_url).then(function(response) {
                    $scope.tasks = response.data
                })
            }
        }
    }
    $scope.addtask = function() {
        if ($scope.task != "") {
            url = '/todo/add_task/';
            data = $.param({ project_id: $scope.project_id, task_name: $scope.task });
            $http.post(url, data).then(function(response) {
                $scope.task = "";
                $scope.updateQueue();
                Materialize.toast('Task Added', 2000, 'rounded');
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
    $scope.selectedDate = function() {
        x = new Date($scope.project_date)

        function pad(s) {
            return (s < 10) ? '0' + s : s;
        }
        $scope.selected_date = [x.getFullYear(), pad(x.getMonth() + 1), pad(x.getDate())].join('-');
        console.log($scope.selected_date)
        project_date_url = "/api/project/" + $scope.project_id + "/task/date/" + $scope.selected_date
        $http.get(project_date_url).then(function(response) {
            $scope.tasks = response.data
        })

    }
    $scope.assignYourself = function(task_id) {
        url = '/todo/assign_yourself/'
        if ($scope.taskAssignDate != "") {
            data = $.param({ task_id: task_id, task_date: $scope.taskAssignDate })
            $http.post(url, data).then(function(response) {
                Materialize.toast(response.data.message, 2000, 'rounded')
                $scope.updateQueue();
                x = new Date($scope.taskAssignDate)

                function pad(s) {
                    return (s < 10) ? '0' + s : s;
                }
                $scope.taskAssignDate = [x.getFullYear(), pad(x.getMonth() + 1), pad(x.getDate())].join('-');
                if ($scope.selected_date == $scope.taskAssignDate) {
                    project_date_url = "/api/project/" + $scope.project_id + "/task/date/" + $scope.taskAssignDate
                    $http.get(project_date_url).then(function(response) {
                        $scope.tasks = response.data
                    })
                }
                $scope.taskDate = false;
            })
        } else {
            Materialize.toast('Choose Task Date', 2000, 'rounded')
        }

    }
    $scope.selectMember = function(member_id) {
        console.log(member_id)
    }
    $scope.assignDate = function(context, task_id) {
        var date_element = "#your_date" + task_id
        $(date_element).pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15, // Creates a dropdown of 15 years to control year
            min: true
        });
        $(date_element).on("change", function() {
            $scope.taskAssignDate = $(date_element).val();
        });

        context.taskDate = !context.taskDate;
        context.taskToOther = false;
    }
    $scope.assignTask = function(context, task_id) {
        context.taskToOther = !context.taskToOther;
        context.otherMember = ""
        context.taskDate = false;
        var other_task_date = "#other_task" + task_id
        var project_detail_url = "/api/project/" + $scope.project_id
        $http.get(project_detail_url).then(function(response) {
            angular.forEach(response.data.members, function(member) {
                $scope.members[member.user.username] = null
            })
        })
        $('input.autocomplete').autocomplete({
            data: $scope.members,
            limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
            onAutocomplete: function(val) {
                $scope.otherMember = val
            },
            minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
        });
        $(other_task_date).pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15, // Creates a dropdown of 15 years to control year
            min: true
        });
        $(other_task_date).on("change", function() {
            $scope.taskAssignDate = $(other_task_date).val();
        });
    }
    $scope.assignToOther = function(task_id) {
        if ($scope.otherMember != "" && $scope.taskAssignDate != "") {
            data = $.param({
                task_id: task_id,
                task_date: $scope.taskAssignDate,
                task_member: $scope.otherMember
            })
            url = '/todo/assign_other/'
            $http.post(url, data).then(function(response) {
                Materialize.toast(response.data.message, 2000, 'rounded');
                $scope.updateQueue();
                $scope.taskDate = false;
                context.taskToOther = false;
            })
        }
    }
    $scope.editPercentage = function(context) {
        context.showRange = !context.showRange;
        context.showPutBack = false;
    }
    $scope.savePercentage = function(task_id) {
        $scope.showRange = false;
        $scope.task_percentage = $('#' + task_id).val()
        url = "/todo/task_percentage/"
        data = $.param({
            task_id: task_id,
            task_percentage: $scope.task_percentage
        })
        // console.log($scope.task_percentage)
        $http.post(url, data).then(function(response) {
            project_date_url = "/api/project/" + $scope.project_id + "/task/date/" + $scope.selected_date
            $http.get(project_date_url).then(function(response) {
                $scope.tasks = response.data
            })
            if ($('#showongoing').is(':checked')) {
                temp_queue = [];
                project_detail_url = "/api/project/" + $scope.project_id;
                $http.get(project_detail_url).then(function(response) {
                    angular.forEach(response.data.tasks, function(task) {
                        if (task.percentage_complete >= 0 && task.percentage_complete < 100 && task.assigned_to != null) {
                            temp_queue.push(task);
                        }
                    })
                    $scope.queue = temp_queue;
                })
            } else {
                $scope.updateQueue();
            }

        })
    }
    $scope.edittaskPutBack = function(context) {
        context.showPutBack = !context.showPutBack
        context.showRange = false;
    }
    $scope.taskPutBack = function(reason, task_id) {
        if (reason != "") {
            data = $.param({ reason: reason, task_id: task_id })
            url = '/todo/task_put_back/'
            $http.post(url, data).then(function(response) {
                Materialize.toast(response.data.message, 2000, 'rounded')
                project_date_url = "/api/project/" + $scope.project_id + "/task/date/" + $scope.selected_date
                $http.get(project_date_url).then(function(response) {
                    $scope.tasks = response.data
                })
                if ($('#showongoing').is(':checked')) {
                    temp_queue = [];
                    project_detail_url = "/api/project/" + $scope.project_id;
                    $http.get(project_detail_url).then(function(response) {
                        angular.forEach(response.data.tasks, function(task) {
                            if (task.percentage_complete >= 0 && task.percentage_complete < 100 && task.assigned_to != null) {
                                temp_queue.push(task);
                            }
                        })
                        $scope.queue = temp_queue;
                    })
                } else {
                    $scope.updateQueue();
                }
            })
        }
    }
    $scope.deleteFromQueue = function(task_id) {
        var task_delete_url = '/todo/delete_task/' + task_id + "/"
        $http.post(task_delete_url).then(function(response) {
            Materialize.toast(response.data.message, 2000, 'rounded')
            project_date_url = "/api/project/" + $scope.project_id + "/task/date/" + $scope.selected_date
            $http.get(project_date_url).then(function(response) {
                $scope.tasks = response.data
            })
            $scope.updateQueue();
        })
    }
    $scope.showOnGoing = function(event) {
        // console.log(event.target.checked)
        temp_queue = []
        if (event.target.checked) {
            project_detail_url = "/api/project/" + $scope.project_id;
            $http.get(project_detail_url).then(function(response) {
                angular.forEach(response.data.tasks, function(task) {
                    if (task.percentage_complete >= 0 && task.percentage_complete < 100 && task.assigned_to != null) {
                        temp_queue.push(task);
                    }
                })
                $scope.queue = temp_queue;
            })
        } else {
            $scope.updateQueue();
        }
    }
    $scope.init();
}]);