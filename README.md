# Hearthstone Deck Builder

A webapp for creating, saving, and publishing decks for Hearthstone. Share you public decks with others simply by copying its URL and pasting it elsewhere.

Created in [Visual Studio Code](https://code.visualstudio.com/) using a [Hearthstone Card API](https://rapidapi.com/omgvamp/api/hearthstone).

## Running the Server Yourself

1. Install the latest version of Python3.
1. Install [PostgreSQL](https://www.postgresql.org/) and create a database with a name of "capstone1".
1. Create an account at [RapidAPI.com](https://rapidapi.com).
1. Create the environment variable "API_KEY" and set it to the key provided by RapidAPI.
1. Clone this repository into a local directory.
1. In the root of the local directory, run Python's `venv` module and activate it.
1. Run `pip -install requirements.txt`.
1. To start the server, run `flask run` in the root of the local directory.
