app.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl,id){
        var fd = new FormData();
        console.log(fd)
        fd.append('file', file,id+".mp3");
        
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined} 
        }) 
        .then(
            function success(response){
                console.log(response)
            },
            function error(err){
                console.log(err)
            }
        )
        
    } 
}]);