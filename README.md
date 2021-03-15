# FER Offline
> **Engineer Team**  
> last update: 2021.03.15    
> 
> @ author: Chun-Yu Chen  
> @ email: adam@gapp.nthu.edu.tw  
> @ mattermost: chen-chun-yu  


## Setting
* Image    
	1. install docker in your device
	2. use your account login to gitlab `docker login biicgitlab.ee.nthu.edu.tw:5050`
	3. download the image `docker pull biicgitlab.ee.nthu.edu.tw:5050/prod/engineer/fer_offline`

* Code Structure
	1. `git clone https://biicgitlab.ee.nthu.edu.tw/prod/engineer/fer_offline.git`

## Run 

### Mode1 > Assign Folder 

1. Go to the path where you clone the repository, run `cd <your_path>`

2. Put your files in `fer_input/<your_folder>/` 
  
3. Execute **docker_run.sh** or **docker_run.bat** depends on your OS:     
     
   Only do files in `fer_input/<your_folder>`    
   * if your OS is UBUNTU, `bash docker_run.sh  <your_folder>`   
   * if your OS is WINDOWS, `docker_run.bat  <your_folder>`

4. Check result in the `fer_result` folder 
5. The original files and folder will be moved to 
	
	`fer_finished/<your_folder>/*.mp4`  

### Mode2 > Do All files

1. Go to the path where you clone the repository, run `cd  <your_path>`

2. Put all the files in `fer_input/` 

3. Execute **docker_run.sh** or **docker_run.bat** depends on your OS:     
     
   do all files in `fer_input/` without input folder name
	* if your OS is UBUNTU, run `bash docker_run.sh`
	* if your OS is WINDOWS, run `docker_run.bat` 

4. Check result in the `fer_result` folder 
5. The original files and folder will be moved to `fer_finished/*`

## Input Data Requirement
1. Only process .mp4 files.

## Output Format
1. `.csv` files. And each colume in the `.csv` file is:
    * time
    * frame
    * face_x
    * face_y
    * face_w
    * face_h
    * emotion

    ![](https://i.imgur.com/lvjzuci.png)
2. `.mp4` files showing the recognized face frame and the current emotion of the face.
3. `.csv` files & `.mp4` files would be compressed as a `.zip` file.
4. `.zip` file can be named by passing parameter when executing `video_emotion_color_demo.py`, if you don't pass parameter, `.zip` file would be named with the current time stamp.
