import os
from flask import Flask
from models import setup_db
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
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
    
    @app.route('/actors')
    def get_actors():
        return "Get actors"
    
    @app.route('/movies')
    def get_movies():
        return "Get movies"
    
    @app.route('/actors', methood=['DELETE'])
    def delete_actor():
        return "Delete actor"
    
    @app.route('/movies', methood=['DELETE'])
    def delete_movie():
        return "Delete movie"
    
    @app.route('/actors', methood=['POST'])
    def create_actor():
        return "Create actor"
    
    @app.route('/movies', methood=['POST'])
    def create_movie():
        return "Create movie"
    
    @app.route('/actors', methood=['PATCH'])
    def update_actor():
        return "Update actor"
    
    @app.route('/movies', methood=['PATCH'])
    def update_movie():
        return "Update movie"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
