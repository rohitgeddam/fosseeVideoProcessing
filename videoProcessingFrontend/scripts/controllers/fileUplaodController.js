

app.controller('uploadCtrl', ['$scope', 'fileUpload', function($scope, fileUpload,id){
    $scope.invalidFileType = false

    $scope.clickedOnUploadButton = false 

    $scope.uploadFile = function(id){
     

        var file = $scope.myFile;

        // var uploadUrl = "http://127.0.0.1:8000/api/reupload/"+id;
        var uploadUrl = LOCAL_HOST_URL_WITH_PORT + "/api/reupload/"+id
        if (file.name.split('.').pop() !== "mp3"){
            $scope.invalidFileType = true
        }
        else{
            $scope.invalidFileType = false
            fileUpload.uploadFileToUrl(file, uploadUrl,id);
            $scope.clickedOnUploadButton = true;
        }
    };

    
    
}]);