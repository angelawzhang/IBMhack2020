from flask import Flask, request, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('./db.json')

def verify_body(body):
    try:
        return body['name'] and body['domain'] and bool(body['blackOwned']) and body['logo'] and body['categories'] and body['photos']
    except:
        return False

@app.route('/')
def root():
    return 'root route of API'

@app.route('/business', methods=['GET'])
def index():
    Business = Query()
    businesses = db.search(Business['type'] == 'business')
    return jsonify(businesses), 200

@app.route('/business/<business_name>', methods=['GET'])
def show(business_name):
    Business = Query()
    businesses = db.search((Business['type'] == 'business') & (Business['name'] == business_name))
    resp = businesses[0] if len(businesses) > 0 else {}
    status = 200
    if resp == {}:
        status = 404
    return jsonify(resp), status

@app.route('/business', methods=['POST'])
def create():
    body = request.json
    valid = verify_body(body)
    if not valid:
        return jsonify({'msg': 'invalid request body'}), 400
    
    Business = Query()
    q = db.search((Business['type'] == 'business') & ((Business['name'] == body['name']) | (Business['domain'] == body['domain'])))
    if len(q) != 0:
        return jsonify({'msg': 'business with that name or domain already exists'}), 409
    
    new_business = {
        'type': 'business',
        'name': body['name'],
        'domain': body['domain'],
        'blackOwned': bool(body['blackOwned']),
        'logo': body['logo'],
        'categories': body['categories'],
        'photos': body['photos']
    }
    db.insert(new_business)

    return jsonify(new_business), 200

@app.route('/business/<business_name>', methods=['DELETE'])
def delete(business_name):
    Business = Query()
    q = db.search((Business['type'] == 'business') & (Business['name'] == business_name))
    if len(q) == 0:
        return jsonify({'msg': 'business with that name not found'}), 404
    
    db.remove((Business['type'] == 'business') & (Business['name'] == business_name))
    return jsonify({'msg': 'business deleted'}), 200