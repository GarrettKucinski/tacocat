from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
from flask_bcrypt import check_password_hash

import forms
import models

DEBUG = True
PORT = 3000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = "It's a secret to everybody."

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


# @app.before_request
# def before_request():
#     """Connect to database before each request"""

#     g.db = models.db
#     g.db.connect()
#     g.user = current_user


# @app.after_request
# def after_request(response):
#     """Close the database connection"""
#     g.db.close()
#     return response


@app.route('/')
def index():
    if current_user.is_authenticated:
        try:
            user = models.User.get(id=current_user.id)
            tacos = user.get_tacos()
        except ValueError:
            pass
    else:
        tacos = []
    return render_template('index.html', tacos=tacos)


@app.route('/register', methods=("GET", "POST"))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(email=form.email.data,
                                password=form.password.data)
        flash("Yay, you've completed registration!")
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/login', methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("You've entered and incorrect email or password!")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've logged in successfully!", "succes")
                return redirect(url_for('index'))
            else:
                flash("You've entered and incorrect email or password!")

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for("index"))


@app.route('/taco', methods=("GET", "POST"))
def create_taco():
    form = forms.TacoCatForm()
    if form.validate_on_submit():
        models.Taco.create(
            user=current_user._get_current_object(),
            protein=form.protein.data,
            cheese=form.cheese.data,
            extras=form.extras.data
        )
        return redirect(url_for('index'))

    return render_template("taco.html", form=form)


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
