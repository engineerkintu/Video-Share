"""Video Share app for sharing youtube videos"""
import os
from functools import wraps
import uuid
from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, BooleanField, TextAreaField, SelectField, PasswordField, validators
from movies import movies
from users import users
from votes import votes
from data import Movie, User, Upvote


app = Flask(__name__)

all_movies = movies()
new_movie = Movie()
user = User()
upVote = Upvote()
#All Movies
@app.route('/')
def movies():
    """Display all movies"""
    new_movies=new_movie.get_movies()
    for movie in new_movies:
	
        votes = upVote.get_upVotes(movie['id'])
        movie['votes'] = votes
       
    if all_movies:
        return render_template('movies.html', all_movies=all_movies, new_movies=new_movies)
    else:
        msg = 'No Movie Found'
        return render_template('movies.html', msg=msg)


#Register form class
class RegisterForm(Form):
    """Register form for new users"""
    
    username = StringField(u'Username', validators=[validators.Length(min=1, max=50)])
    email = StringField(u'Email', validators=[validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

#Movie form class
class MovieForm(Form):
    """Movie form for adding movies"""
    title = StringField(u'Title', validators=[validators.Length(min=1, max=200)])
    description = StringField(u'Description', validators=[validators.Length(min=1, max=500)])
    link = StringField(u'Youtube URL', validators=[validators.Length(min=1, max=40)])


#user register
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register function for a new user"""
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
       
        email = form.email.data
        username = form.username.data
        password = form.password.data
        if user.check_user_name(username):
            flash('Username already taken', 'danger')
            return redirect(url_for('register'))
        if user.check_user_email(email):
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
        user_data = {'id':str(uuid.uuid4()),'username':username,'email':email,'password':password}
        response = user.register_user(user_data)
        #flash message
        flash(response, 'success')
        #redirect to home page
        return redirect(url_for('movies'))
    return render_template('register.html', form=form)

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login function for a member"""
    if request.method == 'POST':
        #get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        logged_in_user = user.login_user(username,password_candidate)
        if logged_in_user:
            #passed
            session['logged_in'] = True
            session['username'] = username
            flash('Your are now logged in', 'success')
            return redirect(url_for('dashboard'))

        else:
            error = 'User not found'
            return render_template('login.html', error=error)
    return render_template('login.html')

#Check if user is logged
def is_logged_in(f):
    """implement decorator for checking if a user is logged in"""
    @wraps(f)
    def wrap(*args, **kwargs):
        """check if user is logged"""
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#logout
@app.route('/logout')
@is_logged_in
def logout():
    """log out function for the user"""
    session.clear()
    return redirect(url_for('login'))

#dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    """implement the user dashboard"""
	#get Movies
    all_movies=new_movie.get_user_movies(session['username'])
    if all_movies:
        return render_template('dashboard.html', all_movies=all_movies)
    else:
        msg = 'No Movies Found'
        return render_template('dashboard.html', msg=msg)

#add movie
@app.route('/add_movie', methods=['POST', 'GET'])
@is_logged_in
def add_movie():
    """Function for adding a movie"""
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        movie_data = {}
        title = form.title.data
        description = form.description.data
	link = form.link.data
        if session['username']:
            created_by = session['username']
        else:
            created_by = 'Anonymous'
        if new_movie.get_movie_titles(created_by, title):
            #flash message
            flash('Title already exists', 'danger')
            #redirect to home page
            return redirect(url_for('add_movie'))
            
        movie_data = {'id':str(uuid.uuid4()),'title':title,'details':details,'link':link,'created_by':created_by,'votes':0}
	
        response = new_movie.set_movie(movie_data)
        flash(response, 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_movie.html', form=form)


#Up vote Movie
@app.route('/up_vote/<string:id>', methods=['POST'])
@is_logged_in
def up_vote(id):
    """Up_vote function for upvoting movies"""
	upvote_data = {'id':str(uuid.uuid4()),'movie_id':id,'voted_by':session['username']}

    if upVote.check_upvote(session['username'], id):
        #flash message
        flash('You already upvoted this movie', 'success')
        #redirect to review page
        return redirect(url_for('movie', id=id))
    response = upVote.set_upvote(upvote_data)
    flash(response, 'success')
    return redirect(url_for('movie', id=id))


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
