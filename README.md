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

### Instructions for running locally
In a terminal window:
```
python3 app.py
```
Then in a web browser open the app at the IP and port that is displayed in the terminal log information. Ex: `0.0.0.0:8080`
