import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOTQwNDkxZGRlYjMwMDY4YjQ5NGQ0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ2MjY1OTEsImV4cCI6MTYxNDcxMjk5MSwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.m0fYOsr0v4oFJhezJZpBx4P0M7qSjF4ndmj_hkJufubSrhezWBxXfUGLNC2t1RRYS6UYwPB9ezWPRyT6CwdlZg8mMO4sxzMU_ivUS-Ty0RMoGVPUECsOWHx8IVC_QSGV9-L8B7EjBrMFDS-fH4jNIIbc2cRj6Gvkyrw48tPtfFz3ZS8NQUdHr839_zoj6lZR6tQsqphCPHgVA_gIbcRBZCl4JycuEqkE2vo16JBgB8bbmHdHHi5MI6GAWSN6zJ0928zE9muh0er7CVcJrYKsFqwZvOdvjX_T_2JDn7OGksiJrOq_Ho2c7KOx_Sas2nbT11hqOLy5-uTdTUsR3Y9PNQ'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOGE3ZDY3MTYyNTcwMDcxZDM3YzUxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ2MjY2MTcsImV4cCI6MTYxNDcxMzAxNywiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.TtjGHxA2uedx2B86eNruYsJAUrhaCna6qjXTeULMSh4l6VlTSsba1j_xVriWRZTh6DwlURbMMGSHxnxqKU0Yu605eN9pq8s4dMQczvujTem2CXbDoXt3ZWq-NBsbcLcSMLDYTzytLSb3luCs2ypLvoqlal4SkoaCr4e1grH_gWyYNZ7ulDYDDrTaXHPn-iv327xN-euWp9DJ46sMEf_hpMc0TJLZWGBgsoCvAqMmbdInMVX-53r6vfbA0SVGmiGH2g1WRTmwnI491wAQpSbq4oDeG_bO-sjSjGCnBMBxP07Sw2FGEG2Jtug1tzsEj96opQHEJSvJKW4xt_TmlIWfEQ'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOGE3ZWQ5NTRmYmUwMDZmZTNlNGU1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ2MjY3MDAsImV4cCI6MTYxNDcxMzEwMCwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.ivll_uImb49VbJU_4dMT-OjvG6_tsH7Qown7NEpUFbFZydv6n47HzYy9dle2hZJyjfXi1eowOAVyJSjU7CD3G-qkbTRVtFHzqRRginslfLOw6EvJthQQyhFpCoOEfJdH5oSAskJkwSbSaxGkN1PVFSi_7jt4UU9dWObZo3qVDusrJno9tbYytKgBBIzW56nj6TQfW5R2fq2rAZLlxS8x4FiuuuGoMF-teYYN1xD5r2B96ClvW8CLrNLocoMMO7Wy7FnVsjRGltSYy7IHESo_lfRIk4g30GoefZIkwOwtDFmoj8FclzKaf0RP90U2QM42p00hXisUZ-_eULUT9enS-A'

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}

        self.app = create_app()
        self.client = self.app.test_client
        self.DB_PATH = os.getenv('DATABASE_URL')  
        setup_db(self.app, self.DB_PATH)

        # Test data set-up for all tests down under

        self.new_actor = {
            'name': "SRK",
            'age': 55,
            'gender': 'MALE'
        }

        self.new_actor_tc = {
            'name': "Tom Cruise",
            'age': 50,
            'gender': 'MALE'
        }

        self.new_actor_up = {
            'name': "Brad Pitt",
            'age': 52,
            'gender': 'MALE'
        }

        self.new_movie = {
            'title': "TEST MOVIE",
            'release_date': "2021-06-01 10:00:00"
        }

        self.new_movie_tc = {
            'title': "Avengers",
            'release_date': "2021-06-01 10:00:00"
        }

        self.new_movie_up = {
            'title': "Justice League",
            'release_date': "2021-06-01 10:00:00"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass


# Test cases for /actors Endpoints 
# ---------------------------------
# GET Positive case - Producer Role

    def test_200_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

# POST Positive case - Director Role
    def test_post_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.director_auth_header)
        data = json.loads(res.data)
        actor = Actor.query.filter_by(id=data['new-actor-id']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# DELETE Positive Case - Deleting an existing actor - Director Role
    def test_delete_actor(self):
        res = self.client().post('/actors', json=self.new_actor_tc, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['new-actor-id']

        res = self.client().delete('/actors/{}'.format(actor_id), headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor_id)

# DELETE Negative Case - Actor not found - Director Role
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999', headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource was not found')

# PATCH Positive case - Update age of an existing - Director Role
    def test_patch_actor(self):
        res = self.client().post('/actors', json=self.new_actor_tc, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['new-actor-id']

        res = self.client().patch('/actors/{}'.format(actor_id), json=self.new_actor_up, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated-actor-id'], actor_id)

# RBAC GET actors w/o Authorization header
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors', json=self.new_actor_tc)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)  
        self.assertEqual(data['description'], 'Authorization header is expected in the request')

# RBAC POST actor with wrong Authorization header - Casting Assistant Role
    def test_new_actor_wrong_auth(self):
        res = self.client().post('/actors', json=self.new_actor_tc, headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission Not Granted')




# Test cases for  /movies Endpoints 
# -----------------------------------
# GET Positive case - Producer Role

    def test_200_get_movies(self):
        res = self.client().get('/movies', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

# POST Positive case - Producer Role
    def test_post_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.producer_auth_header)
        data = json.loads(res.data)
        movie = Movie.query.filter_by(id=data['new-movie-id']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)


# DELETE Positive Case - Deleting an existing movie - Producer Role
    def test_delete_movie(self):
        res = self.client().post('/movies', json=self.new_movie_tc, headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        movie_id = data['new-movie-id']

        res = self.client().delete('/movies/{}'.format(movie_id), headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], movie_id)

# DELETE Negative Case - movie not found - Director Role
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/999', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource was not found')

# PATCH Positive case - Update age of an existing - Producer Role
    def test_patch_movie(self):
        res = self.client().post('/movies', json=self.new_movie_tc, headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        movie_id = data['new-movie-id']

        res = self.client().patch('/movies/{}'.format(movie_id), json=self.new_movie_up, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated-movie-id'], movie_id)

# PATCH Negative case - Update age of an existing - Producer Role
    def test_patch_movie(self):
        res = self.client().patch('/movies/99999', json=self.new_movie_up, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource was not found')
        
# RBAC - Test Cases:
# RBAC GET movies w/o Authorization header
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies', json=self.new_movie_tc)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)  
        self.assertEqual(data['description'], 'Authorization header is expected in the request')

# RBAC POST movie with wrong Authorization header - Assistant Role - No Permission
    def test_new_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.new_movie_tc, headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission Not Granted')

# RBAC POST movie with wrong Authorization header - Director Role - No Permission
    def test_new_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.new_movie_tc, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission Not Granted')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()