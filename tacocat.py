from flask import (Flask, render_template, flash, redirect, url_for)

import forms
import models

DEBUG = True
PORT = 3000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = "It's a secret to everybody."


@app.route('/')
def index():
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


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
