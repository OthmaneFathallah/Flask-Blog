from flask_blog.models import User, Post
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog import app, db, bcrypt
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

my_dict = {'name': 'Jack', 'age': 26}
@app.route("/")
@app.route("/home")
def home():
    title = "Home Page"
    return render_template("index.html", posts= my_dict, title=title)

@app.route("/about")
def about():
    title = "About Us"
    return render_template("about.html", title=title)

@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Create Account"
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully! You are now able to log in.", "success")
        flash("OK!", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html", title=title, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login"
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Logged in Successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title=title, form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    title = "Logout"
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    title = "Account"
    return render_template("account.html", title=title)