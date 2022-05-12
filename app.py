import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from plaid import Plaid
from helper import get_sorted_pivots

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['POST', 'GET'])
def get_png() :
   if request.method == 'POST':
      record = json.loads(request.data)
      colors = record['colors']
      size = record['size']
      twill = record['twill']
      pivots = record['pivots']
      width = record['width']
      height = record['height']
      
      if not pivots:
         pivots = get_sorted_pivots(len(colors))
      try:
         plaid = Plaid(colors, pivots, size, twill)
         data = {
            'colors': colors,
            'size': size,
            'twill': twill,
            'pivots': pivots,
            'image': plaid.get_png(width, height),
         }
         return data, 200
      except Exception as e:
         return e, 400
   else:
      return 'hello'


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)