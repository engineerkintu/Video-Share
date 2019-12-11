"""Test for Share Video web app"""
import unittest
from datetime import datetime
from app import app, RecipeForm
from data import Movie, User,UpVote
from flask import session

class DataTestCase(unittest.TestCase):
    
    def setUp(self):
        app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
        self.recipe = Recipe()
        self.user = User()
        self.upVote = UpVote()
        self.movie_data = {'id':'5XXXXX', 'title':'Movie one', 'details':'this movie is very funny', 'link':'  https://www.youtube.com/embed/VIDEOID', 'created_by':'Moses','votes':0, 'status':False}
        self.user_data = {'id':'5XXXXX','name':'Moses','email':'engineerkintu@gmail.com','username':'Mosebadus','password':'12345', 'confirm':'12345'}
        self.user_data2 = {'id':'5XXXXX','name':'Moses','email':'engineerkintu2@gmail.com','username':'Mosebadus2','password':'12345', 'confirm':'12345'}
        self.user_data3 = {'id':'5XXXXX','name':'Moses','email':'engkmos@gmail.com','username':'Mosebadus4','password':'12345', 'confirm':'12345'}
        self.upvote_data = {'id':'1XXXXX', 'movie_id':'5XXXXX','voted_by':'Mosebadus'}

    def test_add_movie(self):
        '''test add movie'''
        response = self.movie.set_movie(self.movie_data)
        self.assertEqual(response, "Movie added successfully", msg = "Can't add movie")

    def test_get_movies(self):
        '''test get movies'''
        response = self.movies.get_movies()
        self.assertIsInstance(response, list, msg = "Can't get movies")
        self.assertIsInstance(response[0], dict, msg = "Can't get movies")


    def test_get_movie(self):
        response = self.movie.get_movie('5XXXXX')
        self.assertIsInstance(response, dict, msg = "Can't get movie")

    def get_user_movies(self):
        '''test get user movies'''
        response = self.movie.get_user_movies('Mosebadus')
        self.assertIsInstance(response, list, msg = "Can't get movies")
        self.assertIsInstance(response[0], dict, msg = "Can't get movies")

    def get_movie_titles(self):
        '''test get movie titles'''
        response = self.movie.get_movie_titles('Mosebadus','Movie one')
        self.assertIsInstance(response, list, msg = "Can't get movies")
        self.assertIsInstance(response[0], dict, msg = "Can't get movies")

    def test_reg_user(self):
        '''test register user'''
        response = self.user.register_user(self.user_data)
        self.assertEqual(response, "Your are now registered and can log in", msg = "Can't add movie")

    def test_check_user_name(self):
        '''test username check'''
        self.user.register_user(self.user_data)
        response = self.user.check_user_name('Mosebadus')
        self.assertIsInstance(response, list, msg = "Can't get username")
        self.assertIsInstance(response[0], dict, msg = "Can't get username")

    def test_check_user_email(self):
        '''test user email check'''
        self.user.register_user(self.user_data)
        response = self.user.check_user_email('engineerkintu@gmail.com')
        self.assertIsInstance(response, list, msg = "Can't get user email")
        self.assertIsInstance(response[0], dict, msg = "Can't get user email")

    def test_login_user(self):
        '''test user login'''
        response = self.user.login_user('Mosebadus','12345')
        self.assertIsInstance(response, list, msg = "Can't login user")
        self.assertIsInstance(response[0], dict, msg = "Can't login user")

    def test_set_upvote(self):
        '''test set upvote'''
        response = self.upVote.set_upvote(self.upvote_data)
        self.assertEqual(response, "Movie upvoted Successfully", msg = "Can't upvote movie")

    def test_check_upvote(self):
        '''test check upvotes'''
        self.upVote.set_upvote(self.upvote_data)
        response = self.upVote.check_upvote('Mosebadus','5XXXXX')
        self.assertIsInstance(response, list, msg = "Can't get upvote")
        self.assertIsInstance(response[0], dict, msg = "Can't get upvote")

    def test_get_upVotes(self):
        '''test get number of upvotes'''
        self.upVote.set_upvote(self.upvote_data)
        response = self.upVote.get_upVotes('5XXXXX')
        self.assertIsInstance(response, int, msg = "Can't get votes")

#++++++++++++++++++++++Testing end points++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def test_home_page_header(self):
        """Test home page"""
        client = app.test_client()
        rsp = client.get('/')
        self.assertIn('Movie one', str(rsp.data))

    def test_login_page_header(self):
        """Test login_page"""
        client = app.test_client(self)
        rsp = client.post('/login', content_type='application/x-www-form-urlencoded', data={'username':'geom','password':'12345'}, follow_redirects=True)
        self.assertIn('User not found', str(rsp.data))
        rsp = client.post('/login', content_type='application/x-www-form-urlencoded', data=self.user_data, follow_redirects=True)
        self.assertIn('Your are now logged in', str(rsp.data))

    def test_logout_header(self):
        """Test dashboard_page"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess.clear()
            rsp = c.get('/logout', follow_redirects=True)
            self.assertTrue(rsp, msg='Cant logout')

    def test_register_page_header(self):
        """Test register_page"""
        client = app.test_client(self)
        rsp = client.post('/register', content_type='application/x-www-form-urlencoded', data=self.user_data, follow_redirects=True)
        self.assertIn('Username already taken', str(rsp.data))
        rsp = client.post('/register', content_type='application/x-www-form-urlencoded', data=self.user_data3, follow_redirects=True)
        self.assertIn('Email already exists', str(rsp.data))
        rsp = client.post('/register', content_type='application/x-www-form-urlencoded', data=self.user_data2, follow_redirects=True)
        self.assertIn('Your are now registered and can log in', str(rsp.data))

    def test_dashboard_page_header(self):
        """Test dashboard_page"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['username'] = 'Mosebadus'
                sess['logged_in'] = True
            rsp = c.get('/dashboard')
            self.assertIn('Movie one', str(rsp.data))

    def test_add_movie_page_header(self):
        """Test add_movie_page"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['username'] = 'Geofrocker'
                sess['logged_in'] = True
            rsp = c.post('/add_movie', content_type='application/x-www-form-urlencoded', data=self.recipe_data, follow_redirects=True)
            self.assertIn('Movie created successfully', str(rsp.data))

    def test_add_upvote_page_header(self):
        """Test upvote_page"""
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['username'] = 'Mosebadus'
                sess['logged_in'] = True
            rsp = c.post('/up_vote/5XXXXX', content_type='application/x-www-form-urlencoded', data=self.upvote_data, follow_redirects=True)
            self.assertIn('Movie upvoted Successfully', str(rsp.data))

    

