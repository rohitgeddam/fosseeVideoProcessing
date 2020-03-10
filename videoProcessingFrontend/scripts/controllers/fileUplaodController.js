app.controller('myCtrl', ['$scope', 'fileUpload', function($scope, fileUpload,id){
    invalidFileType = false
    $scope.uploadFile = function(id){
        var file = $scope.myFile;
        // file.name = id+'.mp3';
        // console.log(file)
        // console.log('file is ' );
        // console.dir(file);
        // console.log("this is the file from controlelr")
        // console.log(file.name)
        var uploadUrl = "http://127.0.0.1:8000/api/reupload/"+id;
        if (file.name.split('.').pop() !== "mp3"){
            $scope.invalidFileType = true
        }
        else{
            $scope.invalidFileType = false
            fileUpload.uploadFileToUrl(file, uploadUrl,id);
        }
    };

    
    
}]);