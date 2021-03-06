
from flask import Flask, render_template, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import requests

# create engine
connection_string = "mario:12345@localhost:5432/movie_search_project"
engine = create_engine(f'postgresql://{connection_string}')
connection = engine.connect()

# Creat new endpoint for pretty json file
Base = automap_base()
Base.prepare(engine, reflect = True)
Streaming = Base.classes.movie_search_project
session = Session(engine)
app = Flask(__name__)

@app.route("/")
def Homepage():
    return render_template("index.html")
@app.route("/search")
def SearchPage():
    return render_template("search.html")
@app.route("/backhome")
def ReturnHome():
    return render_template("index.html")

# Creat new rout for score
@app.route("/movies_score")
def movies_score():
    movies = pd.read_sql("select age, runtime, title, imdb, rotten_tomatoes,((imdb+(rotten_tomatoes/10))/2) as score from movie_search_project order by score desc", connection)
    return movies.to_json()
# Creat new rout for genres
@app.route("/movies_genre")
def movies_genere():
    movies = pd.read_sql("select genres, count(genres) as count from movie_search_project group by genres", connection)
    return movies.to_json()


@app.route("/movies")
def movies():
    # movies = pd.read_sql("select * from movie_search_project order by rotten_tomatoes desc", connection)
    movies = pd.read_sql("select * from movie_search_project", connection)
    return movies.to_json()

@app.route("/movies2")
def movies2():
    results = session.query(Streaming.title, Streaming.genres, Streaming.age, Streaming.imdb, Streaming.netflix, Streaming.hulu,\
            Streaming.prime_video, Streaming.runtime, Streaming.year, Streaming.directors, Streaming.rotten_tomatoes).all()
    moviesDB = []
    for title, genre, age, imdb, netflix, prime, hulu, runtime, year, directors, rotten in results:
            all_movies_dict = {}
            all_movies_dict["title"] = title
            all_movies_dict["genres"] = genre
            all_movies_dict["age"] = age
            all_movies_dict["imdb"] = imdb
            all_movies_dict["netflix"] = netflix
            all_movies_dict["hulu"] = hulu
            all_movies_dict["prime_video"] = prime
            all_movies_dict["runtime"] = runtime
            all_movies_dict["year"] = year
            all_movies_dict["directors"] = directors
            all_movies_dict["rotten_tomatoes"] = rotten
            moviesDB.append(all_movies_dict)
    return jsonify(moviesDB)

if __name__ == '__main__':
 app.run()
