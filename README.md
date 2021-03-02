# Full Stack Capstone Casting Agency API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create the database by running in terminal:
```bash
dropdb fsnd
createdb fsnd
```
With Postgres running, migrate the required tables by running in terminal:
```bash
python manage.py db migrate
python manage.py db upgrade
```

## Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server, refer `setup.sh` and execute:

```bash
export DATABASE_URL=postgresql://<Username>:<Password>@localhost:5432/fsnd
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

## API Refrence

## Getting Started
Base URL: Local backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Remote Production URL: Live backend app is hosted at Heroku and can be accessed with https://fsnd-capstone-vu.herokuapp.com/

Authentication: This app supports 3rd part Authentication using Auth0 JWT tokens.
The API has three registered users:

1. Casting Assistant

```
email: vibhu.aa23@gmail.com
Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOTQwNDkxZGRlYjMwMDY4YjQ5NGQ0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTQ5NDUsImV4cCI6MTYxNDgwMTM0NSwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.XMRTHerC4TpaFp3N6ZJLUGY77eBbW0de9Dcs1Z_8FRfkp78p8NJpNyo9YZvX9gF9UhFfx26xkiSkMYWjg8mzURlXb-2rURhacRchNgRDGbMYMK1KOqPujFQ9SaUZEMxk5hepYcHzBJdMWrQlhzc3owVFbQ0WkYdabViNSXaEhxSvxqyuTmp8hYeuCPZC4kh6CdPIpy_UiFbRmMae4ynMoiBeAYUWKpJr2KkNtmhe5y1B0_91Nym5RUml__sO1x8LvmTr0f9XrPoB5_osGjic-2gN6FavZ-AHlT57BMe7nsrzqtn6RR0PHcnt2y4-Sos74cQlOVBKSHlE7a2z63Rthg
```

2. casting Director

```
email: vibhu.cc23@gmail.com
Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOGE3ZDY3MTYyNTcwMDcxZDM3YzUxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTQ5MzgsImV4cCI6MTYxNDgwMTMzOCwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.I87xjSdWJ4yAZSVN6qg6x0g2CFwMzs2ARODx9BU2wMq2CkWqYFnLpdxksa0bSA_v3B5fdSmDgaauaJUPkURSGj-DzbTgzy5JaehPAdWpoUZzVHVlWkwW2JcUK7NavdeA0BIgHGfVrsTdLSaQhlvOzNayp_Yt2vP4uqxBSmxZoo_5qYoynSGY6SxvV5Ki04Dhk2i2wrTo7n0KVVMMvZJpryKNqz2o2nUs7UDLyZdY3vD4Ziqc4vFNZ2RtDHyrRl85tnxwzth2L4fIdUjRdwi_U_wGaSvTSK6mhfSQHgRjvpQcADKAeX3hasSdv-Q2sntyX_uq02xKPsU4lLUXGx4Gaw
```

3. Producer

```
email: vibhu.eclipse@gmail.com
Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOGE3ZWQ5NTRmYmUwMDZmZTNlNGU1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTMyNTgsImV4cCI6MTYxNDc5OTY1OCwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.AsM93mgcymdkaboe1j55Xy3V9vq0abeatdH-BDTb5ROawaLLLepBGJDVm5UTdBANuBXbqrig1wFoWozA7DnkHIkwCvcxsiDIyFoKBCEQx-Ha59USnRpttlR9wTVynD-Zwgd4YrcksNERCPYwwh_O4sl1TtfJIXjautAPH5FPVtQfKTUEi7nyyTaMdfg1mQ5EMAXvHRWIgSVDEGzXBDGVX34OQSFpiA5Uw6AB7YJ3h60pc0L5ImgX5o3C7mxauzHBh4jYtf4WancrXviNZ75cbaxL-F--DwwoQcQ6JNCiVZ5LxR8xw2jeGNUyW-PdkNgF3JBP4LQeUD9NG22zcUsAwQ
```

## Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three major error types when requests fail:

```
400: Bad Request
404: Resource Not Found
422: Not Processable
```

## Endpoints
```
GET '/movies'
GET '/actors'
DELETE '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
POST '/movies'
POST '/actors'
PATCH '/movies/<int:movie_id>'
PATCH '/actors/<int:actor_id>'
```

GET '/movies'
- Fetches a list of movies stored in the database
- Request Arguments: None
- Returns: An object with movies and release dates.
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 01 Jun 2021 10:00:00 GMT",
            "title": "Kabhi Gham"
        },
        {
            "id": 2,
            "release_date": "Tue, 01 Jan 2030 00:00:00 GMT",
            "title": "Justice League"
        },
        {
            "id": 3,
            "release_date": "Tue, 01 Jun 2021 10:00:00 GMT",
            "title": "Kabhi Khushi Kabhi Gham"
        }
    ],
    "success": true
}
```

GET '/actors'
- Fetches a list of actors stored in the database
- Request Arguments: None
- Returns: An object with actors, their age and gender
```
{
    "actors": [
        {
            "age": 21,
            "gender": "Male",
            "name": "Cinia"
        },
        {
            "age": 45,
            "gender": "MALE",
            "name": "Michael"
        },
        {
            "age": 28,
            "gender": "MALE",
            "name": "George"
        }
    ],
    "success": true
}
```

DELETE '/movies/<int:question_id>'
- Deletes a particular Movie.
- Request Arguments: Movie Id of the Movie to be deleted.
- Returns: Movie Id of the movie which was deleted with a success message.
```
        {
            'success': True,
            'deleted': 1
        }
```

DELETE '/actors/<int:question_id>'
- Deletes a particular Actor.
- Request Arguments: Actor Id of the Actor to be deleted.
- Returns: Actor Id of the Actor which was deleted with a success message.
```
        {
            'success': True,
            'deleted': 1
        }
```

POST '/movies'
- Takes the new movie and release date entered by User and store it in the Movie table.
- Request Arguments: Fields should be passed in the request body in JSON format - Movie, Release Date
- Returns: Movie Id of the movie which was added with a success message.
```
        {
            'success': True,
            'new-movie-id': 2
        }
```

POST '/actors'
- Takes the new actor, age and gender entered by User and store it in the Actor table.
- Request Arguments: Fields should be passed in the request body in JSON format - Name, Age, Gender
- Returns: Movie Id of the movie which was added with a success message.
```
        {
            'success': True,
            'new-actor-id': 2
        }
```

PATCH '/movies/<int:movie-id>'
- Takes an existing movie and release date entered by User and updates it in the Movie table.
- Request Arguments: Fields should be passed in the request body in JSON format - Movie, Release Date
- Returns: Movie Id of the movie which was updated with a success message.
```
        {
            'success': True,
            'updated-movie-id': 2
        }
```

PATCH '/actors'
- Takes an existing actor, age and gender entered by User and update it in the Actor table.
- Request Arguments: Fields should be passed in the request body in JSON format - Name, Age, Gender
- Returns: Actor Id of the movie which was added with a success message.
```
        {
            'success': True,
            'updated-actor-id': 2
        }
```



## Testing
To run the tests, run
```
python test_app.py
```