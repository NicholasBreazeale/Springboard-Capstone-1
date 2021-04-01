from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    biography = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)

    def set_password(self, pwd):
        self.password = bcrypt.generate_password_hash(pwd, rounds=14).decode("utf-8")

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        return user if user and bcrypt.check_password_hash(user.password, password) else None

class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text)
    public = db.Column(db.Boolean)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref="decks")
    cards = db.relationship("DeckCards")

class DeckCards(db.Model):
    __tablename__ = "deckCards"

    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), primary_key=True)
    card_id = db.Column(db.Text, primary_key=True)
    card_count = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref="reviews")