from flask import Flask, request, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/crawl', methods=['GET'])
def do_crawling():  
  if request.method == 'GET':
    query_params = request.args.to_dict()
    print(query_params)
    
    # 크롤링 수행
    result = json.dumps(
      {
        'brand': [
          '투썸플레이스'
        ],
        'product': [
          '아이스박스 패밀리'
        ],
        'price': [
          '45,000P'
        ],
        'url': [
          'bogo.co.kr'
        ]
      }
    )
    response = Response(result, 200)
    return response

if __name__ == "__main__":
  app.run(host='220.149.242.12', port=50008, debug=False)