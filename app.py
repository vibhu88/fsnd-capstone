from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    Swagger(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    This is Casting Agency Capstone API GET method to fetch all movies
    This is a generic method and can be accessed by everyone.
    ---
    tags:
        - Capstone API
    responses:
        Good Response:
        description: All Movies with Release Dates
        500:
        description: Something went wrong!
    '''
    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        if movies == []:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })

    '''
    This is Casting Agency Capstone API GET method to fetch all actors
    This is a generic method and can be accessed by everyone.
    ---
    tags:
        - Capstone API
    responses:
        Good Response:
        description: All Actors with Age and Gender
        500:
        description: Something went wrong!
    '''
    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        if actors == []:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })

    '''
    This is Casting Agency Capstone API POST method to add new movie
    This method required Authentication and role based Authorization to be accessible.
    ---
    tags:
        - Capstone API
    parameters:
      - in: body
        title: title
        type: String
        required: true
        description: Title of the Movie
      - in: body
        release_date: release_date
        type: String
        required: true
        description: Release date of the movie
    responses:
        Good Response:
        description: Returns the id of the movie added
        500:
        description: Something went wrong!
    '''
    @app.route('/movies', methods=["POST"])
    @requires_auth(permission='post:movies')
    def create_movie(payload):
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title,
                          release_date=new_release_date
                          )
            movie.insert()
            return jsonify({
                "success": True,
                "new-movie-id": movie.id
            })
        except Exception:
            abort(422)

    '''
    This is Casting Agency Capstone API POST method to add new actor
    This method required Authentication and role based Authorization to be accessible.
    ---
    tags:
        - Capstone API
    parameters:
      - in: body
        name: name
        type: String
        required: true
        description: Name of the Actor
      - in: body
        age: age
        type: Integer
        required: true
        description: Age of the actor
      - in: body
        gender: gender
        type: String
        required: true
        description: Gender of the actor
    responses:
        Good Response:
        description: Returns the id of the actor added
        500:
        description: Something went wrong!
    '''
    @app.route('/actors', methods=["POST"])
    @requires_auth(permission='post:actors')
    def create_actor(payload):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', 0)
        new_gender = body.get('gender', None)

        try:
            actor = Actor(name=new_name,
                        age=new_age,
                        gender=new_gender
                        )
            actor.insert()
            return jsonify({
                "success": True,
                "new-actor-id": actor.id
            })
        except Exception:
            abort(422)

    '''
    This is Casting Agency Capstone API DELETE method to delete a movie
    This is a generic method and can be accessed by everyone.
    ---
    tags:
        - Capstone API
    responses:
        Good Response:
        description: Id of the movie deleted
        500:
        description: Something went wrong!
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })
    
    '''
    This is Casting Agency Capstone API DELETE method to delete an actor
    This is a generic method and can be accessed by everyone.
    ---
    tags:
        - Capstone API
    responses:
        Good Response:
        description: Id of the actor deleted
        500:
        description: Something went wrong!
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    '''
    This is Casting Agency Capstone API PATCH method to update existing movie
    This method required Authentication and role based Authorization to be accessible.
    ---
    tags:
        - Capstone API
    parameters:
    - in: url
        id: id
        type: Integer
        required: true
        description: ID of the Movie to be updated
      - in: body
        title: title
        type: String
        required: true
        description: Title of the Movie
      - in: body
        release_date: release_date
        type: String
        required: true
        description: Release date of the movie
    responses:
        Good Response:
        description: Returns the id of the movie added
        500:
        description: Something went wrong!
    '''
    @app.route("/movies/<int:movie_id>",methods=["PATCH"])
    @requires_auth(permission='patch:movies')
    def edit_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie :
            abort(404)
        else:
            try:
                body = request.get_json()
                title = body.get("title")
                release_date = body.get("release_date")
            
                if title:
                    movie.title = title
                if release_date:
                    movie.release_date = release_date

                movie.update()
                return jsonify({
                    "success": True,
                    "updated-movie-id"  : movie.id
                }), 200

            except Exception:
                abort(500)

    '''
    This is Casting Agency Capstone API PATCH method to update existing actor
    This method required Authentication and role based Authorization to be accessible.
    ---
    tags:
        - Capstone API
    parameters:
    - in: url
        id: id
        type: Integer
        required: true
        description: ID of the Actor to be updated
      - in: body
        name: name
        type: String
        required: true
        description: Name of the Actor
      - in: body
        age: age
        type: Integer
        required: true
        description: Age of the actor
      - in: body
        gender: gender
        type: String
        required: true
        description: Gender of the actor
    responses:
        Good Response:
        description: Returns the id of the actor added
        500:
        description: Something went wrong!
    '''
    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth(permission='patch:actors')
    def edit_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor :
            abort(404)
        else:
            try:
                req_body = request.get_json()
                name = req_body.get("name")
                age = req_body.get("age")
                gender = req_body.get("gender")
                if name:
                    actor.name = name
                if age:
                    actor.age = age
                if gender:
                    actor.gender = gender
                actor.update()
                return jsonify({
                    "success": True,
                    'updated-actor-id': actor.id
                }), 200
            except Exception:
                abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            "error": 404,
            "message": "Resource was not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            'success': False,
            "error": 405,
            "message": "Method not found"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            "error": 500,
            "message": "Internal Server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)