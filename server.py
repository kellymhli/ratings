"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    # Display login and logout link depending on if user is logged in session.
    if session.get('user') != None:
        session['logged_in'] = True
    else:
        session['logged_in'] = False

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=['GET'])
def register_form():
    """Render register form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process resgistration information."""

    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)

    # Check if user email and password are in the db
    user = User.query.filter(User.email == email, 
                             User.password == password).first()
    print(user)

    # Add new user if not in database, else redirect to homepage
    if user == None:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.user_id
    else:
        session['user'] = user.user_id
        session['logged_in'] = True
        flash("Logged in")

    return redirect('/')


@app.route('/logout')
def logout():
    """Log user our of the session."""

    # Remove user from session
    session.pop('user')
    flash("Logged out")

    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
