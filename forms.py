from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Optional, URL

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=8, message="Must be at least %(min)d characters.")])
    image_url = StringField("Image URL", validators=[Optional(), URL()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60, message="Must be %(min)d-%(max)d characters.")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=8, max=60, message="Must be %(min)d-%(max)d characters.")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60, message="Must be %(min)d-%(max)d characters.")])