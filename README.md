# Screening Task 1: Video Processing
This is a Django application that allows a user to upload a video and its .srt file
containing subtitles.The video is then broken into chunks,based on the timing information specified
in the .srt file. The corresponding audio is extracted from each video chunk and stored separately.For the uploaded video the
web app displays the start time, end time, video chunk sequence number,subtitles and its respective audio(.mp3).
For each audio the use can reupload the edited .mp3 file for that video chunk.The app combines all the audio and video chunks into
one a single video(.mp4) file when the use clicks on the compile button at the bottom of the page and provides a download link.

##Table of Content:

* [Installation](#Installation)
* [Usage](#Usage)
* [Credits](#Credits)
* [License](#License)

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
* Move into the downloaded directory `cd fosseeVideoProcessing/videoProcessingAP/`
* Install required python packages by typing `pip install -r requirments.txt` into the terminal

You need to change some settings to run the database
* Create a new database in MySQL with any name you like `e.g. fossee-task-1`
* navigate to `fosseeVideoProcessing/videoProcessingAPI/videoProcessingApp` and open `settings.py` file.
* make the following changes to the `settings.py` file
    1. Change DB_NAME to the name of the database you created (around line number 80)
    2. Change DB_PASSWORD to your database password
    3. likewise change DB_HOST and DB_PORT 
* If you dont want to make the above changes you should create the database with the name `fossee-task-1` and everything will work without any changes in `settings.py` file.

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

