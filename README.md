# Screening Task 1: Video Processing
This is a Django application that allows a user to upload a video and its .srt file
containing subtitles.The video is then broken into chunks,based on the timing information specified
in the .srt file. The corresponding audio is extracted from each video chunk and stored separately.For the uploaded video the
web app displays the start time, end time, video chunk sequence number,subtitles and its respective audio(.mp3).
For each audio the use can reupload the edited .mp3 file for that video chunk.The app combines all the audio and video chunks into
one a single video(.mp4) file when the use clicks on the compile button at the bottom of the page and provides a download link.

## Table of Content:

* [Installation](#Installation)
* [Usage](#Usage)
* [API](#Api)
* [videoProcessing module](#VideoProcessing module)
* [miscFunctions module](#MiscFunctions module)
* [Credits](#Credits)


# Installation:
* You can either clone the project or download as zip
* To clone the project you must have git installed on your computer.

* click on the Clone or download button and copy the url.
* open the command prompt(windows) or terminal(mac/linux) and  type `git clone [copied_url]` or simply copy and past in terminal
`git clone https://github.com/rohitgeddam/fosseeVideoProcessing.git`

You need to install few things before you can run the project.
* [Python 3.x](https://www.python.org/downloads/)
* [FFmpeg](https://www.ffmpeg.org/download.html)
* [MySQL](https://www.mysql.com/downloads/)

After you have installed the above you can continue
* Move into the downloaded directory `cd fosseeVideoProcessing/videoProcessingAPI/`
* Install required python packages by typing `pip install -r requirments.txt` into the terminal

You need to change some settings to run the database
* Create a new database in MySQL with any name you like `e.g. fossee-task-1`
* navigate to `fosseeVideoProcessing/videoProcessingAPI/` and open `settings.py` file.
* make the following changes to the `settings.py` file
    1. Change DB_NAME to the name of the database you created (around line number 80)
    2. Change DB_PASSWORD to your database password
    3. likewise change DB_HOST and DB_PORT 
* If you dont want to make the above changes you should create the database with the name `fossee-task-1` and everything will work without any changes in `settings.py` file.
* Navigating to `fosseeVideoProcessing/videoProcessingAPI/` and run command `python manage.py migrate` in terminal.
* Before running the project you can run the tests by  navigating to `fosseeVideoProcessing/videoProcessingAPI/` and typing `python manage.py test`
* Before you start the server make sure the MySQL server is running at port `3306` or the port that you decided while creating the database.
* You can now run the project by navigating to `fosseeVideoProcessing/videoProcessingAPI/` and typing `python manage.py runserver`
* If everything goes well the server will be up and running.

# Usage:
* Make sure the Django server and MySQL database is up and running. if not follow the **installation** section properly.
* Now navigate to `fosseeVideoProcessing/videoProcessingFrontend/`
* open `index.html` in a browser (you need to have internet connection as it need to download some scripts from cdn)
* Screenshot below
![homepage_no_files](https://github.com/rohitgeddam/fosseeVideoProcessing/blob/master/images/home_page.png)
* Select any video file (.mp4) and srt file (.srt) from your drive or you can use the ones in the `/fosseeVideoProcessing/videoProcessingAPI/test_files/` (**do not delete any files in test_files directory**)
* Click the **Upload Files**  button to upload your files to the server.
* After the File Upload is successfull **Process Video** button appears click on that button to process the video.
![homepage_files_selected](https://github.com/rohitgeddam/fosseeVideoProcessing/blob/master/images/files_selected.png)

* After the processing is done. The details are listed.
![homepage_processing](https://github.com/rohitgeddam/fosseeVideoProcessing/blob/master/images/list_details.png)

* If you want to re-upload modified audio for a particular video chunk. Under **AUDIO RE-UPLOAD** column select the audio file and click **upload** button
![homepage_reuplaod_audio](https://github.com/rohitgeddam/fosseeVideoProcessing/blob/master/images/details_with_reupload.png)

* Click on the **COMPILE** button at the bottom of the page.
![homepage_compile](https://github.com/rohitgeddam/fosseeVideoProcessing/blob/master/images/compile.png)

* When you click on the **COMPILE** button a **DOWNLOAD TUTORIAL** button is available to download the tutorial.
![homepage_download](https://github.com/rohitgeddam/fosseeVideoProcessing/blob/master/images/download_tutorial.png)

* You can click on the download button to download the tutorial or *right-click* and select *save link as*.

# Api
###Api Endpoints:
* `api/upload/`
    **[POST]**
   <p>This endpoint is used to upload files to the server.It only accepts (.mp4) and (.srt) files
   the uploaded files are stored temporarily before its processed in the media directory.
   It requires 2 files one is video file (.mp4) and the other is (.srt) file.Pass these using form data with the name
   'video' and 'srt' respectively.
   </p>
**returns: JSON**
   
    operationId
    message
    operation_url
   
  
* `api/process/<int:id>`
    **[GET]** 
    <p>This endpoint is used to process the uploaded video.Requires (id) paramater which is the operation_id of the video</p>
    
**returns: JSON**

    message
    time(sec)
    path
    downloadUrl
    chunks
    
* `api/getdetails/<int:id>` 
**[GET]** 
    <p>This endpoint fetches the details of processed video.The (id) parameter is required which is the operation_id of the processed video.</p>
    <p>We can also get the details of previously processed video by specifying the operation_id of that video in parameter.</p>
**returns: JSON**
   
    message
    downloadUrl
    chunks
   
        
* `api/reupload/<int:chunk_id>` 
**[POST]**
 <p>This endpoint is used to reupload the audio file (.mp3).The file is uploaded using form field with the name 'file'. chunk_id is required as parameter.</p>
   <p>This route is redirected to the getdetails route which returns  JSON</p>
    
    message
    downloadUrl
    chunks
   

   
* `api/download/<int:operationId>`
**[GET]** 
    <p>This endpoint compiles all the video and audio chunk into one file and provide a download link. requires operation_id of the video as parameter </p>
**returns:**
   
    message
    name_of_file
    download
  
###API Testing:
###To test the api run the following command.
*   navigate to `fosseeVideoProcessing/videoProcessingAPI/` and run command `python manage.py test` in the terminal.


# VideoProcessing module
#####This is a local module which contains classes and methods usefull for videoprocessing
#####location of module `fosseeVideoProcessing/videoProcessingAPI/api/videoProcessing`

####Classes:
* SRT
* VideoClip
####Methods in SRT class:
* numberOfChunksInSrt
* extractSrtData

####Methods in VideoClip class:
* extractAudioFromVideoAndSave
* removeAudioFromVideoAndSave
####Methods:
* mergeVideoAndAudioToGetDownloadFile
* mergeAudiosForDownload
* mergeVideoForDownload
* trimAudioClipAndSave
* getVideoLengthInSeconds
* convertTimeToSeconds


# MiscFunctions module

#####This is a local module which contains utility or helper functions

#####location of module `fosseeVideoProcessing/videoProcessingAPI/api/miscFunctions`

####Functions in this module
* checkExtensionOfFileFromRequestObject
* handleUploadedFilesAndSave
* serializeObject
* removeAndCreateDirectoryInSamePath
* createDirectoryIfNotExists
* splitAudioAndVideoIntoChunk
* writePathsToTxtFileToUseWithFFMPEG

# Credits
* FFmpeg (License: GNU General Public License (GPL) (GPLv2))
* pysrt (License: GNU General Public License (GPL) (GPLv3))
* mysqlclient (License: GNU General Public License (GPL))
* django-rest-framework (License: BSD License (BSD))
* moviepy (License: MIT License (MIT License))
* pydub (License: MIT License (MIT))
* Django (License: BSD License (BSD))

