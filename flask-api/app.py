from flask import Flask, request, Response
from flask_restx import Resource, Api, fields
from flask import abort


app = Flask(__name__)
api = Api(app)

api_movies = api.namespace('api', description='Movie APIs')

movie_data = api.model(
    'Movie Data',
    {
      "title": fields.String(description="movie title", required=True),
      "description": fields.String(description="movie description", required=True),
      "rating": fields.Integer(description="movie rating", required=True),
      "poster_url": fields.String(description="movie poster", required=False),
    }
)

movie_info = {}
number_of_movies = 0

@api_movies.route('/movies')
class movies(Resource):
  def get(self):
    return {
        'number_of_movies': number_of_movies,
        'movie_info': movie_info
    }


@api_movies.route('/movies/<int:movie_id>')
class movies_model(Resource):
  def get(self, movie_id):
    if not movie_id in movie_info.keys():
      abort(404, description=f"Movie ID {movie_id} doesn't exists")

    return movie_info[movie_id], 200


  @api.expect(movie_data)
  def post(self, movie_id):
    if movie_id in movie_info.keys():
      abort(409, description=f"Movie ID {movie_id} already exists")

    params = request.get_json() # get body json
    movie_info[movie_id] = params
    global number_of_movies
    number_of_movies += 1
  
    return Response(status=200)


  def delete(self, movie_id):
    if not movie_id in movie_info.keys():
      abort(404, description=f"Movie ID {movie_id} doesn't exists")

    del movie_info[movie_id]
    global number_of_movies
    number_of_movies -= 1

    return Response(status=200)


  @api.expect(movie_data)
  def put(self, movie_id):
    global movie_info

    if not movie_id in movie_info.keys():
      abort(404, description=f"Movie ID {movie_id} doesn't exists")
    
    params = request.get_json()
    movie_info[movie_id] = params
    
    return Response(status=200)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)