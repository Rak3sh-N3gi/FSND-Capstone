import os
from flask import Flask, request, jsonify
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

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    # Get actors by actor ID
    @app.route('/actors/<int:id>')
    def get_actor(id):
        actors = Actors.display(id)
        return json.loads(actors)
    
    # Get movies by movie ID
    @app.route('/movies/<int:id>')
    def get_movie(id):
        movies = Movies.display(id)
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
        rc = Actors.delete(id)
        if rc == 0:
            return "Actor deletion failed."
        else:
            return ("Actor with id=%d deleted successfully" % id)
    
    #delete movie by movie ID
    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        rc = Movies.delete(id)
        if rc == 0:
            return "Movie deletion failed."
        else:
            return ("Movie with id=%d deleted successfully" % id)
    
    # Create actor
    @app.route('/actors', methods=['POST'])
    def create_actor():
        actor = Actors(request.get_json().get("name"),request.get_json().get("age"),request.get_json().get("gender"))
        rc = Actors.insert(actor)
        if rc == 0:
            return "Actor creation failed."
        else:
            return ("Actor created with id=%d" % rc)
    
    # Create movie
    @app.route('/movies', methods=['POST'])
    def create_movie():
        movie = Movies(request.get_json().get("title"),request.get_json().get("release_date"))
        rc = Movies.insert(movie)
        if rc == 0:
            return "Movie creation failed."
        else:
            return ("Movie created with id=%d" % rc )
    
    # Update actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    def update_actor(id):
        actor = Actors.display(id)
        actor = json.loads(actor)
        
        if id is None or id == 0:
            return "Actor not found."
        else:
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
                return "Actor update failed."
        else:
                return ("Actor details with id=%d updated successfully" % id)        
    
    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movie(id):
        movie = Movies.display(id)
        movie = json.loads(movie)
        
        if id is None or id == 0:
            return "Movie not found."
        else:
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
                return "Movie update failed."
        else:
                return ("Movie details with id=%d updated successfully" % id)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
