# ScreenshotApp-Service

This repo contains the code for our webapp that will allow users to view images and make comments.
Images can be uploaded to the backend server from the Hololens, and then interacted with on the frontend.
Currently our frontend is undergoing maintenance and is not live on a production server, but the backend
is up at the link below. 

Backend server is [here](https://screenshot-tool-server.herokuapp.com/)

### Dependencies
The dependencies for the backend are established in `requirements.txt` and require pip to install.
These can be installed by running:
```
cd backend
sudo pip install -r requirements.txt
```

The dependencies for the frontend require npm to install.
They can be installed by running:
```
cd front
npm install webpack-dev-server rimraf webpack typescript -g
npm install
```

### Instructions for running locally
In a terminal window:
```
cd backend
python3 server.py
```

In a different terminal window:
```
cd front
npm run server:dev:hmr
```
