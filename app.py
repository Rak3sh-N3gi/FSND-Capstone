import os
from flask import Flask, abort, request, jsonify
from sqlalchemy import null
from models import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app(test_config=None):

    app = Flask(__name__)
    # db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        setup_db(app)
        CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting
    
    # Get actors by actor ID
    @app.route('/actors/<int:id>')
    def get_actor(id):
        actors = Actors.display(id)
        if actors is None or null:
            abort(400)
        return json.loads(actors)
    
    # Get movies by movie ID
    @app.route('/movies/<int:id>')
    def get_movie(id):
        movies = Movies.display(id)
        if movies is None or null:
            abort(400)
        return json.loads(movies)

    # Get all actors
    @app.route('/actors')
    def get_actors():
        actors = Actors.display_all()
        return json.loads(actors)

    # Get all movies
    @app.route('/movies')
    def get_movies():
        movies = Movies.display_all()
        return json.loads(movies)
    
    # Delete actor by actor ID
    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        if id is None or id == 0:
            abort(400)

        rc = Actors.delete(id)
        if rc == 0:
            abort(400)
        else:
            return jsonify ({
                "success": True
            })
    
    #delete movie by movie ID
    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        if id is None or id == 0:
            abort(400)

        rc = Movies.delete(id)
        if rc == 0:
            abort(400)
        else:
            return jsonify ({
                "success": True
            })
    
    # Create actor
    @app.route('/actors', methods=['POST'])
    def create_actor():
        if request.get_json().get("name") is None or request.get_json().get("age") is None or request.get_json().get("gender") is None:
            abort(422)
            
        actor = Actors(request.get_json().get("name"),request.get_json().get("age"),request.get_json().get("gender"))
        rc = Actors.insert(actor)
        if rc == 0:
            abort(500)
        else:
            return jsonify ({
                "success": True,
                "created": rc
            })
    
    # Create movie
    @app.route('/movies', methods=['POST'])
    def create_movie():
        if request.get_json().get("title") is None or request.get_json().get("release_date") is None:
            abort(422)

        movie = Movies(request.get_json().get("title"),request.get_json().get("release_date"))
        rc = Movies.insert(movie)
        if rc == 0:
            abort(500)
        else:
            return jsonify ({
                "success": True,
                "created": rc
            })
    
    # Update actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    def update_actor(id):
        if id is None or id == 0:
            abort(400)

        if request.get_json().get("name") is None and request.get_json().get("age") is None and request.get_json().get("gender") is None:
            abort(422)
        else:
            actor = Actors.display(id)
            if actor is None or null:
                abort(400)
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

            rc = Actors.update(id,name,age,gender)

        if rc == 0:
            return jsonify ({
                "success": False,
                "created": rc
            })
        else:
            return jsonify ({
                "success": True,
                "created": rc
            })
    
    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movie(id):
        if id is None or id == 0:
            abort(400)

        if request.get_json().get("title") is None and request.get_json().get("release_date") is None:
            abort(422)
        else:
            movie = Movies.display(id)
            if movie is None or null:
                abort(400)
            movie = json.loads(movie)
            if request.get_json().get("title") is not None:
                title = request.get_json().get("title")
            else:
                title = movie["name"]
            if request.get_json().get("release_date") is not None:
                releaseDate = request.get_json().get("release_date")
            else:
                releaseDate = movie["releaseDate"]

            rc = Movies.update(id,title,releaseDate)

        if rc == 0:
            abort(500)
        else:
            return jsonify ({
                "success": True,
                "created": rc
            })
  
    # Error handling
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "bad request"}),
                400,
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
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
