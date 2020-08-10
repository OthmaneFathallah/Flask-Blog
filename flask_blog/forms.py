from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from flask_blog.models import User


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[Length(min=2, max=20)])
    email = StringField("Email Address", validators=[Length(min=6, max=30), Email("Problem: Not a valid email.")])
    password = PasswordField("Password", validators=[
        Length(min=6, max=15),
        Regexp("^[0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", message="Password must contain only letters and numbers.")
    ])
    confirm_password = PasswordField("Repeat Password", validators=[
        EqualTo("password")
    ])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError("Username already exists! Try another username.")

    def validate_email(self, email):
        email = User.query.filter_by(email=self.email.data).first()
        if email:
            raise ValidationError("Email already exists! Try another email.")

class LoginForm(FlaskForm):
    
    email = StringField("Email Address", validators=[Length(min=6, max=30), Email("Problem: Not a valid email.")])
    password = PasswordField("Password", validators=[
        Length(min=6, max=15),
        Regexp("^[0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", message="Password must contain only letters and numbers.")
    ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

