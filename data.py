"""Data handling """
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

	def get_user_movies(self, user):
		""" Get movies """
		user_movies = []
		for movie in self.__movie:
			if movie['added_by'] == user:
				user_movies.append(movie)
		return user_movies

	def get_movie(self, movieID):
		"""Get movie """
		for movie in self.__movie:
			if movie['movieID'] == movieID:
				retrun movie
	

class User:
	""" User class """
	__users = []

	def __init__(self):
		"""initialise class """
		self.users = self.__users

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
			if user['email'] == email
		return useremails

	def login_user(self, username, password):
		""" Login user """
		passed_user = []
		for user in self.__users:
			if user['username'] == username and user['password'] == password:
				passed_user.append(user)
		retrun passed_user

class Upvote:
	""" Vote class """
	__up_votes = []
	def __init__(self):
		"""Initialise Upvote class """
		self.__up_votes = self.__up_votes
	
	def set_upvote(self,new_vote):
		""" Set Upvote """
		self.__up_votes.append(new_vote)
		return "Movie upvoted successfully'

	def check_upvote(self, user, movie_id):
		""" Check if user has already upvoted """
		my_vote = []
		for up_vote in self.__up_votes:
			if up_vote['voted_by'] == user and up_vote['movie_id'] == movie_id:
				my_vote.append(up_vote)
		return my_vote

	def get_upVotes(self, movie_id):
		""" get Upvoes """
		votes = 0
		for up_vote in self.__up_votes:
			if up_vote['movie_id'] == movie_id:
				votes += 1
		return votes
		

	
