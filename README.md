# Handlebars
Roster: Kenneth Chin, Calvin Chu, Jeff Lin (Project Manager), and Henry Liu

## Website purpose:
Our website's purpose is to allow a user to explore nearby city bikes, the weather of a certain location, and an image of the location. Users will also be given the opportunity to rate bike companies which will be visible to other users.

## APIs:
[City Bike](http://api.citybik.es/v2/networks) [[Documentation](http://api.citybik.es/v2/#filter)]
- We use this API to retrieve information about city bikes as well as their longitude and latitude.

[MapQuest Open Geocoding](https://developer.mapquest.com/documentation/open/geocoding-api/)
- We use this API to retrieve an image of a requested location.  
- Note: requires a key, but project currently doesn't require users to register for their own key

[Metaweather](https://www.metaweather.com/api/)
- We use this API to retrieve weather of a requested location.


## How to Run the Project:  
### Requirements:
Python3 and pip is required to run the project  
[Download Python3 here](https://www.python.org/downloads/) (pip3 comes with python3 download)

### Creating and activating a virtual environment:
`$ python3 -m venv <name>`  
`$ ./<name>/bin/activate`

### Clone the project and install requirments.txt:
`$ git clone git@github.com:nilffej/Handlebars.git`  
After activating the virutal environment:  
`(venv)$ cd Handlebars`    
`(venv)$ pip3 install -r doc/requirements.txt`  

### Run the project: 
`$ python3 app.py`  
  
