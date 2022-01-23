from flask import Flask, render_template, abort
import requests
import json


app = Flask(__name__)

api_server_addr = 'flask-api'
api_server_port = 5000

@app.route("/") 
def index():
  response = requests.get(f'http://{api_server_addr}:{api_server_port}/api/movies')
  data = response.json()
  data = data['movie_info']
  return render_template('index.html', data=data)

@app.route("/movies/<int:movie_id>") 
def info(movie_id):
  response = requests.get(f'http://{api_server_addr}:{api_server_port}/api/movies/{movie_id}')
  if response.status_code == 404:
    abort(404, description=f"Movie ID {movie_id} already exists")
  data = response.json()

  return render_template('info.html', data=data)
  


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)