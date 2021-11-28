import json
import pandas as pd
import redis
import io

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from flask import current_app

from pdgrid import unique_values, aggrid_values


from flask import Flask
app = Flask(__name__)
from flaskext.mysql import MySQL

CORS(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'grigri'
app.config['MYSQL_DATABASE_DB'] = 'sample_data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

app.config['CACHE_TYPE'] = 'RedisCache'

cache = Cache(app)

def load_from_db(dataset):
    conn = mysql.connect()
    df = pd.read_sql_query("SELECT athlete, age, country, year, date, sport, gold, silver, bronze, total from athletes", conn)
    return df
        

def load_dataframe(dataset):
    buffer = cache.get(dataset)
    if buffer:
        df = pd.read_parquet(io.BytesIO(buffer))
        return df
    else:
        df = load_from_db(dataset)
        buffer = io.BytesIO()
        df.to_parquet(buffer)
        buffer.seek(0)
        res = cache.set(dataset, buffer.read())
        return df
    

@app.route("/api/<dataset>", methods=['POST'])
def server(dataset):
    request_body = json.loads(request.data)
    df = load_dataframe(dataset)
    data = aggrid_values(df, request_body)
    return jsonify(data)


@app.route("/api/<dataset>/<filter_field>", methods=['GET'])
def filter_field(dataset, filter_field):
    df = load_dataframe(dataset)
    data = unique_values(df, filter_field)
    return jsonify(data)

