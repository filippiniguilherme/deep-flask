from flask import Flask, render_template, jsonify, request, redirect
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

import constants as const

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = const.MONGO_URI

mongo = PyMongo(app)

@app.route('/addVideo', methods=['POST'])
def add_video():
  _name = request.form['inputVideoName']
  _theme = request.form['inputVideoTheme']
  _likes = 0
  _unlikes = 0
  _score = (_likes - (_unlikes / 2))

  if _name and _theme and request.method == 'POST':
    id = mongo.db.video.insert({'name': _name, 'theme': _theme, 'likes': _likes, 'unlikes': _unlikes, 'score': _score})
    return render_template('home.html', success=True)
  else:
    return not_found()

@app.route('/videos', methods=['GET'])
def videos():
  try:
    list_videos = mongo.db.video.find()
    return render_template('list_videos.html', list_videos=list_videos)
  except Exception as e:
    return dumps({'error': str(e)})

@app.route('/video/<id>', methods=['GET', 'DELETE'])
def delete_video(id):
  try:
    mongo.db.video.delete_one({'_id': ObjectId(id)})
    return redirect('/videos')
  except Exception as e:
    return dumps({'error': str(e)})

@app.route('/like/<id>', methods=['GET', 'PUT'])
def likeVideo(id):
  try:
    _id = id
    mongo.db.video.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$inc': {'likes': 1}})
    return redirect('/videos')
  except Exception as e:
    return dumps({'error': str(e)})

@app.route('/unlike/<id>', methods=['GET', 'PUT'])
def unlikeVideo(id):
  try:
    _id = id
    mongo.db.video.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$inc': {'unlikes': 1}})
    return redirect('/videos')
  except Exception as e:
    return dumps({'error': str(e)})

def list_of_videos():
  videos_list = mongo.db.video.find()
  return videos_list

@app.route('/ranking', methods=['GET','PUT'])
def test_ranking():
  videos_list = mongo.db.video.find()
  videos_list_with_score = []
  for item in videos_list:
    ranking_calc = (item['likes'] - (item['unlikes'] / 2))
    videos_list_with_score.append((item, ranking_calc))
    videos_list_with_score.sort(key=lambda x: x[1], reverse=True)
    mongo.db.video.update_many({'_id': item['_id']},{'$set': {'score': ranking_calc}})
  return render_template('ranking.html', videos_list=videos_list_with_score)

@app.errorhandler(404)
def not_found(error=None):
  message = {
    'status': 404,
    'message': 'Not Found' + request.url
  }
  resp = jsonify(message)

  resp.status_code = 404

  return resp

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
  app.run(debug=True)