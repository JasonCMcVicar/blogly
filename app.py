"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.get("/")
def homepage():
    '''redirect to users list'''

    return redirect('/users') #add url

@app.get("/users")
def list_users():
    '''list users'''
    users = User.query.all()
    return render_template("users.html", users=users)

@app.get('/users/new')
def show_new_user_form():
    '''Bring to new user form page'''

    return render_template('new_user.html')

@app.post("/users/new")
def add_user():
    '''add user and redirect to list'''

    fname= request.form['first_name']
    lname = request.form['last_name']
    image = request.form['image']
    image = ('default') #create global variable later

    user = User(first_name = fname, last_name = lname,
    image = image)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')#fill in later

@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.get('/users/<int:user_id>/edit')
def show_edit_user_info(user_id):
    """Show the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    '''Process the edit form, returning the user to the user list'''

    fname= request.form['first_name']
    lname = request.form['last_name']
    image = request.form['image']
    image = ('default') #create global variable later

    user = User.query.get_or_404(user_id)
    user.first_name = fname,
    user.last_name = lname
    user.image = image

    db.session.commit()

    return redirect('/users')

@app.post('/user/<int:user_id>/delete')
def delet_user(user_id):
    """Delete user from the list"""

    user = User.query.get_or_404(user_id)
    user.query.delete()

    return redirect('/users')