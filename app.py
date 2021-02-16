from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Movie, Actor



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        if movies == []:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })

    @app.route('/actors')
    def get_movies():
        actors = Actor.query.order_by(Actor.id).all()
        if actors == []:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })

    @app.route('/movies', methods=["POST"])
    def create_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title,
                          release_date=new_release_date
                          )
            movie.insert()
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except Exception:
            abort(422)

    @app.route('/actors', methods=["POST"])
    def create_actor():
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
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except Exception:
            abort(422)


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

    # @app.errorhandler(AuthError)
    # def handle_auth_error(ex):
    #     response = jsonify(ex.error)
    #     response.status_code = ex.status_code
    #     return response

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)