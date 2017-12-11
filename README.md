# ScreenshotApp-Service

This repo contains the code for our web application that is meant to work with our HoloLens application.

Live website can be accessed [here](https://screenshot-tool-eecs498.herokuapp.com)

### Dependencies
The dependencies for the backend are established in `requirements.txt` and require pip to install.
These can be installed by running:
```
sudo pip install -r requirements.txt
```

## Usage

### Application

![alt text](https://user-images.githubusercontent.com/8772290/33816306-ff908914-de05-11e7-99a8-a1318ccd073f.png)  
This is the login screen where a user can enter their credentials to log into the application assuming they have an already created account. An account can be created by clicking the 'New User' button.  

![alt text](https://user-images.githubusercontent.com/8772290/33816308-030a16aa-de06-11e7-8a06-37a31de9c203.png)  
In this page a new user can create their account by entering their first name, last name, email, requested username, and password. Emails and usernames must be unique and passwords must be eight characters long with at least one uppercase letter.  

![alt text](https://user-images.githubusercontent.com/8772290/33816312-07148438-de06-11e7-956f-8aaaf5121ba3.png)
Here is the base dashboard for a user, they are able to see the navbar where they will be able to logout with the 'Logout' button at any point and return to this dashboard by clicking the 'Home' button. A user can see the images they own along with images they have been invited to see, they will be listed and clickable in this way: ![alt text](https://user-images.githubusercontent.com/8772290/33816316-0d387720-de06-11e7-8088-767ab36ac76f.png)  

![alt text](https://user-images.githubusercontent.com/8772290/33816327-183758f8-de06-11e7-98b1-17b9346438f3.png)  
After clicking on an image a user will be redirected to a page with the image along with multiple options regarding the image.  

![alt text](https://user-images.githubusercontent.com/8772290/33816330-1c883c06-de06-11e7-8914-7e1cfce4d99d.png)  
This right panel will have information about the image and if the image is owned by the logged in user, the user will be able to invite other users (assuming they are valid users) to view and comment on the image. 

![alt text](https://user-images.githubusercontent.com/8772290/33816340-2a591422-de06-11e7-97e6-ff14dbc7cd38.png)  
Finally, users can comment on images to comverse with others users regarding the content of the images.  

### Api Usage

Endpoint: '/api/new-image-hololens' POST  
Usage: Used for adding an image to an account from a Microsoft HoloLens  
Format: Form data  
```
username: string
password: string
caption: string (optional)
image: file
```

Endpoint: '/api/get-image?id=#' GET  
Usage: Used for getting image by # id  
Requirements: Logged in to an account which owns or is able to view image  

Endpoint: '/api/add_comment' POST  
Usage: Used for adding a comment to an existing image  
Format: Form data  
Requirements: Logged in to an account which owns or is able to view image  
```
image_id: number
comment: string
```

Endpoint: '/api/add_viewer' POST  
Usage: Used for adding a viewer to an existing image  
Format: Form data  
Requirements: Logged in to an account which owns the image  
```
image_id: number
new_viewer: string
```

Endpoint: '/api/edit_title' POST  
Usage: Edit the title of an existing image  
Format: Form data  
Requirements: Logged in to an account which owns the image  
```
image_id: number
new_title: string
```

Endpoint: '/api/edit_caption' POST  
Usage: Edit the caption of an existing image 
Format: Form data  
Requirements: Logged in to an account which owns the image  
```
image_id: number
new_caption: string
```

### Instructions for running locally
In a terminal window:
```
python3 app.py
```
Then in a web browser open the app at the IP and port that is displayed in the terminal log information. Ex: `0.0.0.0:8080`
