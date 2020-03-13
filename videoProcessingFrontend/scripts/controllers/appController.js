app.controller('appController',function($scope,$http){
    $scope.response = ''
    $scope.uploadedSuccessfully = false
    $scope.processUrl = ''
    $scope.operationId = ''
    $scope.processResponse = ''
    $scope.isError = false;
    $scope.isLoaded = true

    $scope.filesLoaded = true

    $scope.downloadReady = false
    $scope.isCompiled = true
    // to hide show the table
    $scope.dataReceived = false;
    // remove after testing
    $scope.tempId = ''
    $scope.reuploadAudioFile = '';



 $scope.upload = function(){
    console.log($scope.filesLoaded);

  var fd = new FormData();
  var vidfiles = document.getElementById('video').files[0];
  var srtfiles = document.getElementById('srt').files[0];





  console.log(fd)

  if(!vidfiles || !srtfiles){
    $scope.filesLoaded = false;
  
  }
 
  // AJAX request
  else{
    fd.append('video', vidfiles,vidfiles.name.replace(/\s/g, ''));


    fd.append('srt', srtfiles,srtfiles.name.replace(/\s/g, ''));
    $scope.filesLoaded = true
    $http({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/upload/',
        data: fd,
        headers: {'Content-Type': undefined},
       }).then(function successCallback(response) { 
         // Store response data
         $scope.response = response.data;
         console.log(response.data)
         $scope.isError = false;
         $scope.uploadedSuccessfully = true
         $scope.processUrl = response.data.operation_url;
         $scope.operationId = response.data.operationId;
       }).catch(function error(err){
           console.log(err);
           $scope.isError = true;
       })
  }
 
 }


 
$scope.process = function(){
    $scope.isLoaded = false
    $http({
        method:'get',
        url : "http://127.0.0.1:8000/api/process/" + $scope.operationId,
    }).then(function success(response){
        console.log(response);
        $scope.processResponse = response.data;
        $scope.isLoaded = true;
        $scope.dataReceived = true;
    }).catch(function error(err){
        console.log(err);
        $scope.isLoaded = true;
    })
}

$scope.compile = function(){
    $scope.isCompiled = false
    $http({
        method:'get',
        url : "http://127.0.0.1:8000" + $scope.processResponse.downloadUrl,
    }).then(function success(response){
            
        console.log(response)
        $scope.downloadFilePath = "http://127.0.0.1:8000"+response.data.download
        console.log($scope.downloadFilePath);
        //nested http request
        $scope.downloadReady = true
        $scope.isCompiled = true
        
    }).catch(function error(err){
        console.log(err);
        $scope.isCompiled = true
       
    })
}

});
