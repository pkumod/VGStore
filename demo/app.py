from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from gstore import GstoreConnector
from flask_cors import CORS

gStore_config = {
    'ip': '172.31.209.81',
    'port': '5001',
    'user': 'root',
    'password': '123456',
    'database': 'pkubase'
}
gc = GstoreConnector(gStore_config['ip'], gStore_config['port'], gStore_config['user'], gStore_config['password'], http_type='grpc')

app = Flask(__name__, static_url_path='', static_folder='./frontend/dist/')
app.config['threaded'] = True
CORS(app)


@app.route('/')
def server():
    return app.send_static_file('index.html')


@app.route('/query', methods=['POST'])
def query():
    query = request.get_json()['query']
    return gc.query(db_name=gStore_config['database'], format='json', sparql=query)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
