# Blazr
This repository includes all files pertaining to the Blazr job finder app. Also includes all assignments relating to the Blazr app for CS 411 at Boston University.

### How to Set Up and Run Backend Server 
1. Install Flask and requests. 
2. Open Blazr directory (should contain blazr.py)
3. windows cmd: <br>
	set FLASK_APP=blazr.py
	flask run
   <br>(if on mac/linux):<br>
	export FLASK_APP=blazr.py
	flask run
4. Once server is up you can make calls to it by typing into a browser (or making an http request via other software)  the following: "http://localhost:5000/" + endpoint
5. '/' route should render the index.html page in templates
