from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, Optional, URL

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=8, message="Must be at least %(min)d characters.")])
    image_url = StringField("Image URL", validators=[Optional(), URL()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60, message="Must be %(min)d-%(max)d characters.")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=8, max=60, message="Must be %(min)d-%(max)d characters.")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60, message="Must be %(min)d-%(max)d characters.")])

class DeckNewForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=4, message="Must be at least %(min)d characters.")])
    description = TextAreaField("Description", validators=[Optional()])

class DeckDetailForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=4, message="Must be at least %(min)d characters.")])
    description = TextAreaField("Description", validators=[Optional()])
    public = BooleanField("Public (this will make the deck uneditable)", validators=[Optional()])

class DeckCardForm(FlaskForm):
    cardId = StringField("Card ID", validators=[InputRequired()])
    op = SelectField("Operation", choices=[("add", "Add"), ("rem", "Remove")], validators=[InputRequired()])