"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "DEV"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/all_movies')
def all_movies():
    """View all movies."""

    movies = crud.all_movies()

    return render_template("all_movies.html", movies = movies)

@app.route('/all_movies/<movie_id>')
def show_movie(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie = movie)

@app.route('/all_users')
def all_users():
    """View all users."""

    users = crud.all_users()

    return render_template("all_users.html", users = users)

@app.route('/all_users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user = user)

    

@app.route('/users', methods = ["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)

    if user:
        flash("Already a user")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")

    return redirect('/')

@app.route('/login', methods = ["POST"])
def show_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    user_password = crud.get_user_by_password(password)
    
    if user == user_password:
        flash("You have successfully logged in!")
    else:
        flash("Incorrect email or Password")

    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
