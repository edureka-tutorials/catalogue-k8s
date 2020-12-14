from flask import Flask, Response, jsonify, request
import os
import logging
import json
import pymongo
import jwt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

#client = MongoClient('cataloguedb', 27017)
#db = client.productDb
#client = pymongo.MongoClient("mongodb://appAdmin:*****@172.31.27.52:27017/")

mongourl = os.environ['MONGO_URL']
mongoid = os.environ['MONGO_ID']
mongopass = os.environ['MONGO_PASS']
client = pymongo.MongoClient('mongodb://%s:%s@%s:27017/' % (mongoid, mongopass, mongourl))

db = client["productDb"]

@app.route('/', methods=['POST'])
def catalogue():
   logger.info('Entered Catalogue service to list the products')
   try:
    logger.info("Authenticating token")
    token = request.headers['access-token']
    jwt.decode(token, app.config['SECRET_KEY'])
    logger.info("Token authentication successful")
    try:
       products = list(db.product.find())
       logger.info("Fetched products {}".format(products))
       return jsonify({'productDetails': products}), 200
    except:
        logger.warning("Failed to execute query. Leaving Catalogue service")
        response = Response(status=500)
        return response

   except:
      logger.warning("Token authentication failed. Leavng Catalogue")    
      response = Response(status=500)
      return response

@app.route('/price', methods=['POST'])
def price():
   logger.info("Entered the Catalogue service to fetch price of products")
   data = json.loads(request.data)
   productId = data['productId']
   try:
      product = db.product.find_one({'_id': productId})
      price = product['price']
      return jsonify({"price": price}), 200
   except:
      logger.warning("Execution failed")
      response.status = 500
      return response

app.run(port=5001, debug=True, host='0.0.0.0')
