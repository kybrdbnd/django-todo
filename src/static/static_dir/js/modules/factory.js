angular_module.factory('Project',['$resource', function($resource){
    
    return {
    	Summary: $resource('/api/'),
    	ProjectDetail: $resource("/api/project/:project_id",{project_id:'@project_id'}),
		CurrentProject: $resource('/api/project/:project_id/task/date/:selected_date',{project_id:'@project_id',selected_date:'@selected_date'},{
			query: {method: 'get', isArray: true}
		})

    }
}]);


angular_module.factory('Task',['$resource', function($resource){
    var Task = $resource('/api/tasks/');
    return Task
}]);
