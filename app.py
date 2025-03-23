import os
from flask import Flask, abort, request, jsonify
from sqlalchemy import null
from models import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)

    migrate = Migrate(app, db)

    with app.app_context():
        if test_config is None:
            setup_db(app)
        else:
            database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
            setup_db(app, database_path=database_path)

        # db.create_all()

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + " welcome to Casting Agency application home."
        return jsonify({
            'message': greeting
        })

    # Get actors by actor ID
    @app.route('/actors/<int:id>')
    @requires_auth('read:actors')
    def get_actor(payload, id):
        actors = Actors.display(id)
        if actors is None or len(actors) == 0:
            abort(404)
        return json.loads(actors)
        # return actors

    # Get movies by movie ID
    @app.route('/movies/<int:id>')
    @requires_auth('read:movies')
    def get_movie(payload, id):
        movies = Movies.display(id)
        if movies is None or len(movies) == 0:
            abort(404)
        return json.loads(movies)

    # Get all actors
    @app.route('/actors')
    @requires_auth('read:actors')
    def get_actors(payload):
        actors = Actors.display_all()
        if actors is None or len(actors) == 0:
            abort(404)
        return json.loads(actors)

    # Get all movies
    @app.route('/movies')
    @requires_auth('read:movies')
    def get_movies(payload):
        movies = Movies.display_all()
        if movies is None or len(movies) == 0:
            abort(404)
        return json.loads(movies)

    # Delete actor by actor ID
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        if id is None or id == 0:
            abort(400)
        rc = Actors.display(id)
        if rc is None or len(rc) == 0:
            abort(404)
        rc = Actors.delete(id)
        if rc == 0:
            abort(400)
        else:
            return jsonify({
                "success": True
            })

    # delete movie by movie ID
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        if id is None or id == 0:
            abort(400)
        rc = Movies.display(id)
        if rc is None or len(rc) == 0:
            abort(404)
        rc = Movies.delete(id)
        if rc == 0:
            abort(400)
        else:
            return jsonify({
                "success": True
            })

    # Create actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        if request.get_json().get("name") is None or request.get_json().get("age") is None or request.get_json().get("gender") is None:
            abort(422)

        actor = Actors(request.get_json().get("name"), request.get_json().get(
            "age"), request.get_json().get("gender"))
        rc = Actors.insert(actor)
        if rc == 0:
            abort(500)
        else:
            return jsonify({
                "success": True,
                "created": rc
            })

    # Create movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        if request.get_json().get("title") is None or request.get_json().get("release_date") is None:
            abort(422)

        movie = Movies(request.get_json().get("title"),
                       request.get_json().get("release_date"))
        rc = Movies.insert(movie)
        if rc == 0:
            abort(500)
        else:
            return jsonify({
                "success": True,
                "created": rc
            })

    # Update actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, id):
        if id is None or id == 0:
            abort(400)

        if request.get_json().get("name") is None and request.get_json().get("age") is None and request.get_json().get("gender") is None:
            abort(422)
        else:
            actor = Actors.display(id)
            if actor is None or len(actor) == 0:
                abort(404)
            actor = json.loads(actor)
            if request.get_json().get("name") is not None:
                name = request.get_json().get("name")
            else:
                name = actor["name"]
            if request.get_json().get("age") is not None:
                age = request.get_json().get("age")
            else:
                age = actor["age"]
            if request.get_json().get("gender") is not None:
                gender = request.get_json().get("gender")
            else:
                gender = actor["gender"]

            rc = Actors.update(id, name, age, gender)

        if rc == 0:
            abort(500)
        else:
            return jsonify({
                "success": True
            })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, id):
        if id is None or id == 0:
            abort(400)

        if request.get_json().get("title") is None and request.get_json().get("release_date") is None:
            abort(422)
        else:
            movie = Movies.display(id)
            if movie is None or len(movie) == 0:
                abort(404)
            movie = json.loads(movie)
            if request.get_json().get("title") is not None:
                title = request.get_json().get("title")
            else:
                title = movie["title"]
            if request.get_json().get("release_date") is not None:
                releaseDate = request.get_json().get("release_date")
            else:
                releaseDate = movie["release_date"]

            rc = Movies.update(id, title, releaseDate)

        if rc == 0:
            abort(500)
        else:
            return jsonify({
                "success": True
            })

    # Error handling
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "bad request"}),
                400,
                )
    
    @app.errorhandler(401)
    def unauthorized(error):
        return (jsonify({"success": False, "error": 401, "message": "unauthorized"}),
                401,
                )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "Unprocessable entity"}),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (jsonify({"success": False, "error": 500, "message": "Server error"}),
                400,
                )

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
