# ireporter-challenge-2
A simple api endpoints to the Andela iReporter

[![Coverage Status](https://coveralls.io/repos/github/v1b3m/ireporter-challenge-2/badge.svg?branch=develop)](https://coveralls.io/github/v1b3m/ireporter-challenge-2?branch=develop) [![Build Status](https://travis-ci.org/v1b3m/ireporter-challenge-2.svg?branch=Add-travis)](https://travis-ci.org/v1b3m/ireporter-challenge-2) [![Maintainability](https://api.codeclimate.com/v1/badges/b926e59a913d6c5e1f43/maintainability)](https://codeclimate.com/github/v1b3m/ireporter-challenge-2/maintainability)

# Overview
Corruption is a huge bane to Africa’s development. African countries must develop novel and localised 
solutions that will curb this menace, hence the birth of iReporter. iReporter enables any/every citizen 
to bring any form of corruption to the notice of appropriate authorities and the general public. Users 
can also report on things that needs government intervention.

The Api servers to create, edit, patch, retrive and delete redflag records

# Heroku
An online version of the api is available at https://andelaireporterapp.herokuapp.com/
Feel free to check it out at your own convenience

# Endpoints description
|Endpoint                                      | Role
|----------------------------------------------|------------------------------------------------
|GET /api/v1/red-flags                         | Retrieves all red-flag records in the database
|GET /api/v1/red-flags/<red_flag_id>           | Retrieves a red-flag specified by its id
|POST /api/v1/red-flag                         | Adds a red-flag to the database
|PATCH /api/v1/red-flag/<red_flag_id>/location | Edits the location of a specified red-flag
|PATCH /api/v1/red-flag/<red_flag_id>/comment  | Edits a the comment of a specific red-flag
|DELETE /api/v1/red-flag/<red_flag_id>         | Deletes a red-flag specified by Id

Note that all API endpoints use json formatted data. An example is given below for the POST endpoint:
```javascript
{
    "status": "Approved", 
    "location": {"lat": "0.96", "long": "1.23"}, 
    "createdBy": "Benjamin", 
    "type": "red-flag", 
    "comment": "I am the greatest"
}
```
The request above will return the following json data:
```javascript
{
    "data": [
        {
            "id": 7278781,
            "message": "Created red-flag record"
        }
    ],
    "status": 201
}
```
# Installation guidelines
(I've not seen an installation this easy)
* Clone this repo onto your machine
* Make sure to install python3 and postman(to test the endpoints)
* Navigate to the repository route and creata a virtual environment
```
$ cd ireporter-challenge-2
$ python3 -m venv venv
```
* Activate the virtual environment and install dependencies in the requirements.txt file
```
$ . venv/bin/activate
$ pip install -r requirements.txt
```
* Fire Up the API
```
$ flask run
```
* Play around with the API

# Contributors
* v1b3m - *vibenjamin6@gmail.com*