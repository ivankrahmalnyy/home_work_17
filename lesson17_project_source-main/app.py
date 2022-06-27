# app.py
from flask import request, Flask
from flask_restx import Api, Resource
from schemas import movie_schema, movies_schema
from models import *
from setup_db import db

app = Flask(__name__)


app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app. config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}

db.init_app(app)
api = Api(app)
movie_ns = api.namespace("movies")

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_with_genre_and_director = db.session.query(Movie.id,Movie.title, Movie.description, Movie.trailer, Movie.year, Movie.rating,
                                  Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director)

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            movies_with_genre_and_director =  movies_with_genre_and_director.filter(Movie.director_id == director_id)
        if genre_id:
            movies_with_genre_and_director=  movies_with_genre_and_director.filter(Movie.genre_id == genre_id)

        movies = movies_with_genre_and_director.all()
        return movies_schema.dump(movies)

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
        return f"Объект с  id {new_movie.id} создан "


@movie_ns.route("/<int:movie_id>")
class MovieView(Resource):
    def get(self, movie_id):
        movie = db.session.query(Movie).get(movie_id)
        return movie_schema.dump(movie)

    def delete(self,movie_id):
        movie = Movie.query.get(movie_id)
        db.session.delete(movie)
        return f"Объект с  id {movie.id} удален "

if __name__ == '__main__':
    app.run(debug=True)
