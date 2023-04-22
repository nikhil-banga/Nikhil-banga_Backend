# FastAPI

FastAPI is a Python library.

# elasticsearch

elasticsearch is a Python library.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install FASTAPI.

```bash
#type all these commands in terminal

#create virtual environment for python
python3 -m venv FastAPI-ENV

#now shift to that virtual environment
.\FastAPI-ENV\Scripts\activate

#now install required packages
pip3 install fastapi
pip3 install elasticsearch
```
# Install Docker

Docker is Required to use ElasticSearch Functionality

```bash
#type all these commands in terminal

#in the folder there is docker compose file is already there just run this command
docker compose up --build
```

# There are two python files
## one is working with json file with all functionalities
```bash
#to run using json type this command in terminal
uvicorn using-json-all-get-and-post:app --reload       
```
## second is working with elastic search with few of the funtionalities like post request for trades, search request, fetch all trades, find trades by id

```bash
#after completing docker compose up --build
#to run using elasticsearch type this command in terminal
#make sure docker containers are running 
#in yml there is extra kibana image is there u can remove it 
uvicorn elasticsearch-post-fetchall-search:app --reload
```

# Thank you Steeleye for Consideration