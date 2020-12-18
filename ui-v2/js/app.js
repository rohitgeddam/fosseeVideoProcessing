console.log("hello")

$(document).ready(function(){
    $(".file-upload__submit-btn").click(function(event){
  
        event.preventDefault();
        var videoFile = $("#video")[0].files[0]
        var srtFile = $("#srt")[0].files[0]
        var fd = new FormData($('.file-upload__form')[0]);

        fd.append("video", videoFile)
        fd.append("srt", srtFile)

        for (var key of fd.entries()) {
            console.log(key[0] + ', ' + key[1]);
        }
        
    })
})