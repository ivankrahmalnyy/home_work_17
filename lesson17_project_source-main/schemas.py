from marshmallow import Schema, fields
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Str()
    director = fields.Str()

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()