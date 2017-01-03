# Blazr
This repository includes all files pertaining to the Blazr job finder app. Also includes all assignments relating to the Blazr app for CS 411 at Boston University.

### How to Set Up and Run Backend Server 
1. Install Flask, requests with pip install. 
2. Open Blazr directory (should contain blazr.py)
3. Windows cmd: <br>
	set FLASK_APP=blazr.py <br>
	flask run
   <br>(if on mac/linux):<br>
	export FLASK_APP=blazr.py <br>
	flask run
4. If step 3 fails, install the necessary packages the console asks for.
5. Once server is up you can make calls to it by typing into a browser (or making an http request via other software)  the following: "http://localhost:5000/" + endpoint
6. '/' route should render the login.html page in "templates" folder, or if already logged in, home.html in "views"
