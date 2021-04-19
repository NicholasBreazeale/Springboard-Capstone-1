import datetime
import os
import requests
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, session

from forms import LoginForm, RegisterForm, DeckNewForm, DeckDetailForm, DeckCardForm
from models import db, connect_db, User, Deck, DeckCards

app = Flask(__name__)

app.config["SECRET_KEY"] = "y7C8*#Suh$HNuUqj^H42%ZU6eKA*$RZiXvX02OlDYE&JHRVmZ#yhgc&RH9aY0D0q"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/capstone1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api_request_header = {
    "x-rapidapi-key": os.environ["API_KEY"],
    "x-rapidapi-host": "omgvamp-hearthstone-v1.p.rapidapi.com"
}

connect_db(app)
db.create_all()

@app.route("/", methods=["GET"])
def home():
    """Home page."""

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration."""

    form = RegisterForm()
    if form.validate_on_submit():
        if not User.query.filter_by(username=form.username.data).first():
            user = User(username=form.username.data, image_url=form.image_url.data, date=datetime.datetime.utcnow())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return redirect(f"/user/{user.id}")
        form.username.errors.append("Username taken.")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login."""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session["user_id"] = user.id
            return redirect(f"/user/{user.id}")
        flash("Invalid username or password.", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
def logout():
    """Logout current user."""

    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")

@app.route("/user/<int:user_id>", methods=["GET"])
def profile(user_id):
    """Display user profile."""

    return render_template("user.html", user=User.query.get_or_404(user_id), current_user=(session["user_id"]==user_id))

###############################################################
# Card routes

@app.route("/cards/<card_id>", methods=["GET"])
def card_detail(card_id):
    """Get individual card data from the API."""

    response = requests.get(f"https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/{card_id}", headers=api_request_header)
    return render_template("card.html", card=response.json()[0])

@app.route("/cards/search", methods=["GET"])
def card_search():
    """Send the search query to the API and return its response."""

    # "q" argument must be included
    if "q" not in request.args:
        return {"error": 400, "message": "'q' argument not specified."}, 400
    # and must not be all whitespace
    search_query = request.args["q"].strip()
    if search_query == "":
        return {"error": 400, "message": "Only whitespace was provided."}, 400

    response = requests.get(f"https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/search/{search_query}", headers=api_request_header)
    return jsonify(response.json())

###############################################################
# Deck routes

@app.route("/deck", methods=["GET", "POST"])
def deck_new():
    """Form for creating a new deck."""

    # Must be logged in to create a deck
    if "user_id" not in session:
        return redirect("/")

    form = DeckNewForm()
    if form.validate_on_submit():
        deck = Deck(user_id=session["user_id"], title=form.title.data, description=form.description.data, date=datetime.datetime.utcnow(), public=False)
        db.session.add(deck)
        db.session.commit()
        return redirect(f"/deck/{deck.id}")
    return render_template("deckNew.html", form=form)

@app.route("/deck/<int:deck_id>/detail", methods=["GET", "POST"])
def deck_detail_form(deck_id):
    """Show the form for editing deck details."""

    # User must be logged in and the owner of the current deck
    if "user_id" not in session:
        return redirect("/")
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != session["user_id"]:
        return {"error": 401, "message": "You are not the deck's owner."}, 401

    form = DeckDetailForm()

    # GET method
    if request.method == "GET":
        # If the deck is public, redirect GET requests to the deck view
        if deck.public:
            return redirect(f"/deck/{deck.id}")
        # Populate the from with the current data
        form.title.data = deck.title
        form.description.data = deck.description
        return render_template("deckDetail.html", form=form)
    # PUT method
    else:
        # Public decks may not be edited
        if deck.public:
            return {"error": 401, "message": "Public decks may not be edited."}, 401
        # Validate form data
        if not form.validate():
            return render_template("deckDetail.html", form=form)
        # Update deck details with form data
        deck.title = form.title.data
        deck.description = form.description.data
        deck.public = form.public.data
        if deck.public:
            deck.date = datetime.datetime.utcnow()
        db.session.commit()
        # If deck was made public, go to its view, otherwise return to the user's profile
        if deck.public == True:
            return redirect(f"/deck/{deck.id}")
        else:
            return redirect(f"/user/{session['user_id']}")

@app.route("/deck/<int:deck_id>", methods=["GET", "PATCH"])
def deck_edit(deck_id):
    """Edit a deck if a user is the owner."""

    deck = Deck.query.get_or_404(deck_id)

    # Render the deck
    if request.method == "GET":
        # Private decks may only be viewed by their owner
        if deck.public == False and ("user_id" not in session or deck.user_id != session["user_id"]):
            abort(401)

        # Fetch the data for each card in the deck
        deck_cards = []
        session["deck_id"] = deck_id
        for card in deck.cards:
            card_request = requests.get(f"https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/{card.card_id}", headers=api_request_header)
            if not card_request.ok:
                abort(500)
            card_json = card_request.json()[0]
            deck_cards.append({"id": card.card_id, "name": card_json["name"], "count": card.count})

        # If a deck is public, display the deck info, else display the editor
        return render_template("deck.html" if deck.public else "deckEdit.html", deck=deck, cards=deck_cards)
    else:
        # Public decks may not be edited
        if deck.public:
            return {"error": 401, "message": "Public decks may not be edited."}, 401

        # Only the deck owner may edit the deck
        if "user_id" not in session or deck.user_id != session["user_id"]:
            return {"error": 401, "message": "You are not the deck's owner."}, 401

        # Validate the request arguments
        form = DeckCardForm(request.args, meta={"csrf": False})
        if not form.validate():
            return {"error": 400, "message": "Invalid arguments."}, 400

        # Get the card ID parameter from the request and fetch the card from the API
        card_id = form.cardId.data
        card_request = requests.get(f"https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/{card_id}", headers=api_request_header)
        if not card_request.ok:
            return card_request.json(), card_request.status_code
        deck_card = DeckCards.query.filter_by(deck_id=deck_id, card_id=card_id).first()

        # Add a card to the current deck
        if form.op.data == "add":
            if deck_card:
                deck_card.count += 1
            else:
                deck_card = DeckCards(deck_id=deck_id, card_id=card_id, count=1)
                db.session.add(deck_card)
            db.session.commit()
            return {"success": 200, "message": "Card added to deck.", "card": {"id": card_id, "name": card_request.json()[0]["name"], "count": deck_card.count}}, 200
        # Remove a card from the current deck
        else:
            if not deck_card:
                return {"error": 404, "message": "Card not in deck."}, 404
            deck_card.count -= 1
            if deck_card.count <= 0:
                db.session.delete(deck_card)
            db.session.commit()
            return {"success": 200, "message": "Card removed from deck.", "card": {"id": card_id, "name": card_request.json()[0]["name"], "count": deck_card.count}}, 200