import os
import unittest

from app import create_app
from models import db, Actors, Movies


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "casting_test"
        self.database_user = "postgres"
        self.database_password = "abc"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"
        AssistantToken = os.environ['ASSISTANT_TOKEN']
        self.AssistantHeaders = { 'Authorization':'Bearer '+AssistantToken,'Content-Type': 'application/json'}
        DirectorToken = os.environ['DIRECTOR_TOKEN']
        self.DirectorHeaders = { 'Authorization':'Bearer '+DirectorToken,'Content-Type': 'application/json'}
        ProducerToken = os.environ['PRODUCER_TOKEN']
        self.ProducerHeaders = { 'Authorization':'Bearer '+ProducerToken,'Content-Type': 'application/json'}

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()
    

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
# Test to check if the app is running
    def test_retrive_greetings(self):
        response = self.client.get("/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["message"],"Hello welcome to Casting Agency application home.")

# successfull test cases
    def test_retrive_actor_by_id(self):
        with self.app.app_context():
            actor = Actors(
                name="Tom Hanks",
                age=55,
                gender="Male")
            
            actor.insert()
            response = self.client.get(f"/actors/{actor.id}",headers=self.AssistantHeaders)
            data = response.get_json()
            self.assertEqual(actor.id, 1)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["name"],actor.name)
            self.assertTrue(data["age"],actor.age)
            self.assertTrue(data["gender"],actor.gender)
    
    # actor not found test case
    def test_retrive_actor_by_id_not_found(self):
        response = self.client.get("/actors/999",headers=self.AssistantHeaders)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    # test for successful fetch of movie by id
    def test_retrive_movie_by_id(self):
        movie = Movies("The Shawshank Redemption","1994-09-22")
        with self.app.app_context():
            rc = Movies.insert(movie)
            
            response = self.client.get(f"/movies/{rc}",headers=self.AssistantHeaders)
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["title"],movie.title)
            self.assertTrue(data["release_date"],movie.release_date)

    # movie not found test case
    def test_retrive_movie_by_id_not_found(self):
        response = self.client.get("/movies/999",headers=self.AssistantHeaders)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    # test for successful retrieve of actors
    def test_retrieve_Actors(self):
        actor = Actors(
                name="Tom Hardy",
                age=55,
                gender="Male"
         )
        
        with self.app.app_context():
            actor.insert()
        response = self.client.get("/actors",headers=self.AssistantHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data[0]["name"],actor.name)
        self.assertTrue(data[0]["age"],actor.age)
        self.assertTrue(data[0]["gender"],actor.gender)

    # test for unsuccessful retrieve of Actors
    def test_retrieve_Actors_not_found(self):
        response = self.client.get("/actors",headers=self.AssistantHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    # test for successful retrieve of movies
    def test_retrieve_Movies(self):
        movie = Movies(
                title="The Dark Knight Rises",
                release_date="2008-09-22"
         )
        with self.app.app_context():
            movie.insert()
        response = self.client.get("/movies",headers=self.AssistantHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data[0]["title"],movie.title)
        self.assertTrue(data[0]["release_date"],movie.release_date)

    # test for unsuccessful retrieve of Movies
    def test_retrieve_Movies_not_found(self):
        response = self.client.get("/movies",headers=self.AssistantHeaders)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    # test for successful delete of actor
    def test_delete_actor(self):
        with self.app.app_context():
            actor = Actors(
                name="Tom Hanks",
                age=55,
                gender="Male"
            )
            with self.app.app_context():
                actor.insert()

            response = self.client.delete(f"/actors/{actor.id}",headers=self.DirectorHeaders)
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])

    # test for delete of actor which doesn't exist
    def test_delete_actor_not_found(self):
        response = self.client.delete("/actors/999",headers=self.DirectorHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    # test for successful delete of movie
    def test_delete_movie(self):
        with self.app.app_context():
            movie = Movies(
                title="The Shawshank Redemption",
                release_date="1994-09-22"
            )
            with self.app.app_context():
                movie.insert()

            response = self.client.delete(f"/movies/{movie.id}",headers=self.ProducerHeaders)
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])

    # test for delete of movie which doesn't exist
    def test_delete_movie_not_found(self):
        response = self.client.delete("/movies/999",headers=self.ProducerHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])

    # test for successful creation of actor
    def test_create_actor(self):
        response = self.client.post("/actors",headers=self.DirectorHeaders, json={
            "name": "Tom Cruise",
            "age": 55,
            "gender":"male"
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

    # test for creation of actor with missing data
    def test_create_actor_missing_data(self):
        response = self.client.post("/actors",headers=self.DirectorHeaders, json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])

    # test for successful creation of movie
    def test_create_movie(self):
        response = self.client.post("/movies",headers=self.ProducerHeaders, json={
            "title": "Mission Impossible",
            "release_date": "2004-09-22"
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

    # test for creation of movie with missing data
    def test_create_movie_missing_data(self):
        response = self.client.post("/movies",headers=self.ProducerHeaders, json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])

    # Authorization header missing test cases
    def test_error_401(self):
        response = self.client.get("/actors")
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")
        self.assertEqual(data["message"]["description"], "Authorization header is expected.")


    # Access permission test for Casting Assistant
    def test_error_403_CA1(self):
        response = self.client.post("/actors",headers=self.AssistantHeaders, json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"]["code"], "unauthorized")
        self.assertEqual(data["message"]["description"], "Permission not found.")

    def test_error_403_CA2(self):
        response = self.client.delete("/actors/1",headers=self.AssistantHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"]["code"], "unauthorized")
        self.assertEqual(data["message"]["description"], "Permission not found.")

    # Access per,misison test for Casting Director
    def test_error_403_CD1(self):
        response = self.client.post("/movies",headers=self.DirectorHeaders, json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"]["code"], "unauthorized")
        self.assertEqual(data["message"]["description"], "Permission not found.")

    def test_error_403_CD2(self):
        response = self.client.delete("/movies/1",headers=self.DirectorHeaders)
        data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 403)
        self.assertEqual(data["message"]["code"], "unauthorized")
        self.assertEqual(data["message"]["description"], "Permission not found.")

    def test_error_404(self):
        response = self.client.get("/invalid")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource not found")

    def test_error_422(self):
        response = self.client.post("/actors",headers=self.DirectorHeaders, json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable entity")
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()