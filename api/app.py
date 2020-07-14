from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
    return 'root route of API'

@app.route('/business', methods=['GET'])
def index():
    return 'Index'

@app.route('/business/<business_name>', methods=['GET'])
def show(business_name):
    return 'Show business %s' % business_name

@app.route('/business', methods=['POST'])
def create():
    return 'Create business'

@app.route('/business/<business_name>', methods=['DELETE'])
def delete(business_name):
    return 'Delete business %s' % business_name
