from flask import Flask
from src.pdgrid import unique_values, grid_values

app = Flask(__name__)

@app.route("/filter_values/{dataset}")
def unique_values(request):
    request_body = json.loads(request.data)
    fields = request_body.get('fieldNames')
    df = load_dataframe(request_body)
    return unique_values(df, fields)
    


@app.route("/data/{dataset}")
    request_body = json.loads(request.data)
    df = load_dataframe(dataset, request_body)
    return grid_values(df, request_body)
