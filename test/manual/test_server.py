import requests
import json

request_fields = {"startRow":0,"endRow":100,"rowGroupCols":[],"valueCols":[{"id":"gold","aggFunc":"sum","displayName":"Gold","field":"gold"},{"id":"silver","aggFunc":"sum","displayName":"Silver","field":"silver"},{"id":"bronze","aggFunc":"sum","displayName":"Bronze","field":"bronze"},{"id":"total","aggFunc":"sum","displayName":"Total","field":"total"}],"pivotCols":[],"pivotMode":False,"groupKeys":[],"filterModel":{},"sortModel":[]}


response = requests.get("http://localhost:8000/api/olympicWinners", data=json.dumps(request_fields))
response_json = response.json()
print(response_json)
