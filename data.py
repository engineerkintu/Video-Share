"""Data handling """
from users import users
from votes import votes
from movies import movies


class Movie:
	"""Movie class"""
	__movie = []

	def __init__(self):
		"""initialise class """
		self.__movie = self.__movie

	def set_movie(self,movie):
		"""Set the movie variables"""
		self.__movie.append(movie)
		return 'Movie added successfully'

	def get_movies(self):
		"""A vistor gets movies """
		public_movies = []
		for movie in self.__movie:
			public_movies.append(movie)
		return public_movies

class User:
	""" User class """
	__users = []
	def __init__(self):
		"""initialise class """
		self.__users = self.__users

	def register_user(self, user):
		""" Set user """
		self.__users.append(user)
		return 'You are now registered, and can login'

	def check_user_name(self,username):
		"""Check if username exists """
		usernames = []
		for user in self.__users:
			if user['username'] == username:
				usernames.append(user)
		
		return usernames

	def check_user_email(self, email):
		"""Check if email exists """
		useremails = []
		for user in self.__users:
			if user['email'] == email:
				useremails.append(user)
		
		return useremails

	def login_user(self, username, password):
		""" Login user """
		
		passed_user = []
		for user in self__users:
			if user['username'] == usernane and user['password'] == password:
				passed_user.append(user)
		return passed_user

class Vote:
	""" Vote class """
	__votes =[]
	def __init__(self):
		"""Initialise Vote class """
		self.__votes = self.__votes
	
	def set_vote(self,new_vote):
		""" Set Vote """
		self.__votes.append(new_vote)
		return 'Movie voted successfully'

	def check_vote(self, user, movie_id):
		""" Check if user has already upvoted """
		my_vote = False
		for vote in self.__votes:
			if vote['voted_by'] == user and vote['movie_id'] == movie_id:
				my_vote = True
		return my_vote

	def get_upVotes(self, movie_id):
		""" get up votes """
		vts = 0
		for vote in self.__votes:
			if vote['movie_id'] == movie_id and vote['vote_type'] == "up_vote":
				vts += 1
		return vts

	def get_downVotes(self, movie_id):
		""" get down votes """
		vts = 0
		for vote in self.__votes:
			if vote['movie_id'] == movie_id and vote['vote_type'] == "down_vote":
				vts += 1
		return vts

	def check_voteType(self, user, movie_id):
		""" check whether a user voted up or down for a movies"""
		up_vote = False
		for vote in self.__votes:
			if vote['movie_id'] == movie_id and vote['vote_type'] == "up_vote":
				up_vote = True
		return up_vote
				
		

	
