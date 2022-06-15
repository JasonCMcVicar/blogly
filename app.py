"""Blogly application."""

from flask import Flask
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.get("/")
def list_users():
    '''list users'''
    users = User.query.all()
    return render_template("TBD", users=users) #add url

@app.post("/")
def add_user():
    '''add user and redirect to list'''

    fname= request.form['first_name']
    lname = request.form['last_name']
    image = request.form['image']
    image = (default) #create global variable later

    user = User(first_name = fname, last_name = lname,
    image = image)
    db.session.add(user)
    db.session.commit()

    return redirect(...)#fill in later
