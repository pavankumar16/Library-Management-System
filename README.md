### Library Management System

## Setup

#### Install Dependencies
- Create a python virtual environment and activate it(preferred)<br>
```python3 -m venv env```
```source env/bin/activate```
- Install Python Dependecies<br>
```pip3 install flask```<br>
```pip3 install mysql-connector```
- Install Node Packages<br>
```cd static```<br>
```npm install```<br>
- Install MySQL for PC/Mac/Linux, and setup.<br>


### Restoring Dump
- Run .sql files in /LMS_Dump. Restoring Dump can also be easily done using a software like MySQL Workbench. 

### Running the Code
In one terminal, go into server directory and run,<br>
 ```python3 server.py```<br>
In another terminal, go into static directory and run,<br>
 ```npm run watch```<br>

Should run at ```http://localhost:5000/``` by default.

### Load Testing
Make ```script.js``` ```postman-to-k6 final_test.json -e env.json -o script.js```<br>
Test Run,<br>
Run test for 15s, with 200 virtual ```k6 run --duration 15s --vus 200 script.js```
