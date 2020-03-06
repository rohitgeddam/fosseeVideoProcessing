app.controller('myCtrl', ['$scope', 'fileUpload', function($scope, fileUpload,id){
    
    $scope.uploadFile = function(id){
        var file = $scope.myFile;
        // file.name = id+'.mp3';
        // console.log(file)
        // console.log('file is ' );
        // console.dir(file);
        console.log(file)
        var uploadUrl = "http://127.0.0.1:8000/api/reupload/"+id;
        fileUpload.uploadFileToUrl(file, uploadUrl,id);
    };
    
}]);