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
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOTQwNDkxZGRlYjMwMDY4YjQ5NGQ0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTQ5NDUsImV4cCI6MTYxNDgwMTM0NSwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.XMRTHerC4TpaFp3N6ZJLUGY77eBbW0de9Dcs1Z_8FRfkp78p8NJpNyo9YZvX9gF9UhFfx26xkiSkMYWjg8mzURlXb-2rURhacRchNgRDGbMYMK1KOqPujFQ9SaUZEMxk5hepYcHzBJdMWrQlhzc3owVFbQ0WkYdabViNSXaEhxSvxqyuTmp8hYeuCPZC4kh6CdPIpy_UiFbRmMae4ynMoiBeAYUWKpJr2KkNtmhe5y1B0_91Nym5RUml__sO1x8LvmTr0f9XrPoB5_osGjic-2gN6FavZ-AHlT57BMe7nsrzqtn6RR0PHcnt2y4-Sos74cQlOVBKSHlE7a2z63Rthg'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOGE3ZDY3MTYyNTcwMDcxZDM3YzUxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTQ5MzgsImV4cCI6MTYxNDgwMTMzOCwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.I87xjSdWJ4yAZSVN6qg6x0g2CFwMzs2ARODx9BU2wMq2CkWqYFnLpdxksa0bSA_v3B5fdSmDgaauaJUPkURSGj-DzbTgzy5JaehPAdWpoUZzVHVlWkwW2JcUK7NavdeA0BIgHGfVrsTdLSaQhlvOzNayp_Yt2vP4uqxBSmxZoo_5qYoynSGY6SxvV5Ki04Dhk2i2wrTo7n0KVVMMvZJpryKNqz2o2nUs7UDLyZdY3vD4Ziqc4vFNZ2RtDHyrRl85tnxwzth2L4fIdUjRdwi_U_wGaSvTSK6mhfSQHgRjvpQcADKAeX3hasSdv-Q2sntyX_uq02xKPsU4lLUXGx4Gaw'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFTOGcwTEl0Z2ZOUTdBdkg3RHdGUyJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS12dS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzOGE3ZWQ5NTRmYmUwMDZmZTNlNGU1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTMyNTgsImV4cCI6MTYxNDc5OTY1OCwiYXpwIjoiZ05uWEdkYXpUeFZpM3VIYUNmbExOSEhiY1F3VThlaHEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.AsM93mgcymdkaboe1j55Xy3V9vq0abeatdH-BDTb5ROawaLLLepBGJDVm5UTdBANuBXbqrig1wFoWozA7DnkHIkwCvcxsiDIyFoKBCEQx-Ha59USnRpttlR9wTVynD-Zwgd4YrcksNERCPYwwh_O4sl1TtfJIXjautAPH5FPVtQfKTUEi7nyyTaMdfg1mQ5EMAXvHRWIgSVDEGzXBDGVX34OQSFpiA5Uw6AB7YJ3h60pc0L5ImgX5o3C7mxauzHBh4jYtf4WancrXviNZ75cbaxL-F--DwwoQcQ6JNCiVZ5LxR8xw2jeGNUyW-PdkNgF3JBP4LQeUD9NG22zcUsAwQ'

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