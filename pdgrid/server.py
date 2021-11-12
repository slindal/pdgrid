import json
import pandas as pd

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

from pdgrid.pdgrid import unique_values, grid_values


from flask import Flask
app = Flask(__name__)
from flaskext.mysql import MySQL

CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DATABASE_DB'] = 'sample_data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


         

def load_dataframe(dataset, request):
    conn = mysql.connect()
    df = pd.read_sql_query("SELECT athlete, age, country, year, date, sport, gold, silver, bronze, total from athletes", conn)
    return df


@app.route("/api/<dataset>/", methods=['POST'])
def server(dataset):
    request_body = json.loads(request.data)
    df = load_dataframe(dataset, request_body)
    data = grid_values(df, request_body)
    return jsonify(data)


@app.route("/api/<dataset>/<filter_field>/", methods=['GET'])
def filter_field(dataset, filter_field):
    df = load_dataframe(dataset, None)
    data = df[filter_field].drop_duplicates().sort_values().astype(str).tolist()
    return jsonify(data)
