from flask import Flask, request, jsonify
import os
from tinydb import TinyDB, Query
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = TinyDB('./util/db.json')
port = int( os.getenv( 'PORT', 5000 ) )

def verify_body(body):
    try:
        return body['name'] and body['domain'] and type(body['blackOwned']) == bool and body['logo'] and body['categories'] and body['photos']
    except:
        return False

@app.route('/')
@cross_origin()
def root():
    return 'root route of API'

@app.route('/business', methods=['GET'])
@cross_origin()
def index():
    Business = Query()
    businesses = db.search(Business['type'] == 'business')
    return jsonify(businesses), 200

@app.route('/business/<business_name>', methods=['GET'])
@cross_origin()
def show(business_name):
    Business = Query()
    businesses = db.search((Business['type'] == 'business') & (Business['name'] == business_name))
    resp = businesses[0] if len(businesses) > 0 else {}
    if resp == {}:
        return jsonify({'msg': 'business with that name not found'}), 404
    return jsonify(resp), 200

@app.route('/business', methods=['POST'])
@cross_origin()
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
@cross_origin()
def delete(business_name):
    Business = Query()
    q = db.search((Business['type'] == 'business') & (Business['name'] == business_name))
    if len(q) == 0:
        return jsonify({'msg': 'business with that name not found'}), 404
    
    db.remove((Business['type'] == 'business') & (Business['name'] == business_name))
    return jsonify({'msg': 'business deleted'}), 200

@app.route('/domain/<domain_name>', methods=['GET'])
@cross_origin()
def get_by_domain(domain_name):
    Business = Query()
    q = db.search(
        (Business['type'] == 'business')
        & (Business['domain'] == domain_name)
        )
    if len(q) == 0:
        return jsonify({'msg': 'business with that domain not found'}), 404

    if q[0]['blackOwned']:
        return jsonify({
            'blackOwned': True,
            'alternatives': []}), 200
    else: 
        q2 = db.search(
            (Business['type'] == 'business')
            & (Business['blackOwned'] == True)
        )

        def doesIntersect(bus):
            return len(list(set(bus['categories']) & set(q[0]['categories']))) > 0


        alternatives = filter(doesIntersect, q2)
        res_alternatives = []
        for alt in alternatives:
            res_alternatives.append(alt)

        return jsonify({
            'blackOwned': False,
            'alternatives': res_alternatives
        }), 200

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
