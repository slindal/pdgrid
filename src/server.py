from flask import Flask, request, jsonify
from src.pdgrid import unique_values, grid_values
import json
import pandas as pd

app = Flask(__name__)


def load_dataframe(dataset, request):
    """ Stubbed loading from file. FIXME"""
    jsons = json.loads(open('/home/slindal/dev/pdgrid/test/manual/olympic-winners.json').read())
    df = pd.DataFrame(data=jsons)
    return df


@app.route("/filter_values/{dataset}")
def unique_values(request):
    request_body = json.loads(request.data)
    fields = request_body.get('fieldNames')
    df = load_dataframe(request_body)
    return unique_values(df, fields)
    

@app.route("/api/olympicWinners")
def server():
    request_body = json.loads(request.data)
    df = load_dataframe(None, request_body)
    data = grid_values(df, request_body)

    response = {'status': 0,
                'message': "SUCCESS",
                "data": data}
    
    return jsonify(response)
