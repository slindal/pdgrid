from src.server import app
import json


def test_no_grouping_or_sorting():
    with app.test_client() as client:

        group_model = '''{
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [
                {
                    "id": "gold",
                    "aggFunc": "sum",
                    "displayName": "Gold",
                    "field": "gold"
                },
                {
                    "id": "silver",
                    "aggFunc": "sum",
                    "displayName": "Silver",
                    "field": "silver"
                },
                {
                    "id": "bronze",
                    "aggFunc": "sum",
                    "displayName": "Bronze",
                    "field": "bronze"
                },
                {
                    "id": "total",
                    "aggFunc": "sum",
                    "displayName": "Total",
                    "field": "total"
                }
            ],
            "pivotCols": [],
            "pivotMode": false,
            "groupKeys": [],
            "filterModel": {},
            "sortModel": []
        }'''

        
        
        response = client.post("/api/olympicWinners/", data=group_model)
        rows = json.loads(response.data)['rows']
        assert(len(rows) == 100)
        assert(rows[0]['athlete'] == "Michael Phelps")
        assert(rows[-1]['athlete'] == "Jochem Uytdehaage")
                       

def test_sort_by_year():


    with app.test_client() as client:

        group_model = '''{
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [
                {
                    "id": "gold",
                    "aggFunc": "sum",
                    "displayName": "Gold",
                    "field": "gold"
                },
                {
                    "id": "silver",
                    "aggFunc": "sum",
                    "displayName": "Silver",
                    "field": "silver"
                },
                {
                    "id": "bronze",
                    "aggFunc": "sum",
                    "displayName": "Bronze",
                    "field": "bronze"
                },
                {
                    "id": "total",
                    "aggFunc": "sum",
                    "displayName": "Total",
                    "field": "total"
                }
            ],
            "pivotCols": [],
            "pivotMode": false,
            "groupKeys": [],
            "filterModel": {},
            "sortModel": [{"sort": "asc", "colId": "year"}, {"sort": "asc", "colId": "athlete"}]
        }'''

        
        
        response = client.post("/api/olympicWinners/", data=group_model)
        rows = json.loads(response.data)['rows']
        assert(len(rows) == 100)
        assert(rows[0]['athlete'] == "Adam Pine")


def test_groupby_country_sortby_gold():

    group_model = '''{"startRow":0,"endRow":100,"rowGroupCols":[{"id":"country","displayName":"Country","field":"country"}],"valueCols":[{"id":"gold","aggFunc":"sum","displayName":"Gold","field":"gold"},{"id":"silver","aggFunc":"sum","displayName":"Silver","field":"silver"},{"id":"bronze","aggFunc":"sum","displayName":"Bronze","field":"bronze"},{"id":"total","aggFunc":"sum","displayName":"Total","field":"total"}],"pivotCols":[],"pivotMode":false,"groupKeys":[],"filterModel":{},"sortModel":[{"sort":"asc","colId":"gold"}]}'''


    with app.test_client() as client:
        response = client.post("/api/olympicWinners/", data=group_model)
        rows = json.loads(response.data)
        
        angular_rows = {"rows":[{"country":"Costa Rica","gold":"0","silver":"0","bronze":"2","total":"2"},{"country":"Slovakia","gold":"0","silver":"2","bronze":"0","total":"2"},{"country":"Spain","gold":"0","silver":"8","bronze":"2","total":"10"},{"country":"Hungary","gold":"0","silver":"3","bronze":"0","total":"3"},{"country":"Singapore","gold":"0","silver":"0","bronze":"2","total":"2"},{"country":"Bulgaria","gold":"1","silver":"1","bronze":"2","total":"4"},{"country":"Brazil","gold":"1","silver":"0","bronze":"1","total":"2"},{"country":"Tunisia","gold":"1","silver":"0","bronze":"1","total":"2"},{"country":"Belarus","gold":"1","silver":"3","bronze":"2","total":"6"},{"country":"Zimbabwe","gold":"2","silver":"4","bronze":"1","total":"7"},{"country":"Sweden","gold":"2","silver":"2","bronze":"5","total":"9"},{"country":"Poland","gold":"2","silver":"6","bronze":"2","total":"10"},{"country":"South Africa","gold":"2","silver":"2","bronze":"1","total":"5"},{"country":"Croatia","gold":"3","silver":"1","bronze":"0","total":"4"},{"country":"Czech Republic","gold":"3","silver":"1","bronze":"1","total":"5"},{"country":"Finland","gold":"3","silver":"3","bronze":"1","total":"7"},{"country":"Chile","gold":"3","silver":"0","bronze":"1","total":"4"},{"country":"Ukraine","gold":"4","silver":"1","bronze":"2","total":"7"},{"country":"Switzerland","gold":"4","silver":"0","bronze":"0","total":"4"},{"country":"Japan","gold":"5","silver":"16","bronze":"12","total":"33"},{"country":"Italy","gold":"7","silver":"3","bronze":"3","total":"13"},{"country":"Great Britain","gold":"7","silver":"2","bronze":"3","total":"12"},{"country":"Austria","gold":"8","silver":"5","bronze":"7","total":"20"},{"country":"Canada","gold":"9","silver":"12","bronze":"7","total":"28"},{"country":"Jamaica","gold":"10","silver":"4","bronze":"1","total":"15"},{"country":"France","gold":"10","silver":"10","bronze":"5","total":"25"},{"country":"Norway","gold":"16","silver":"8","bronze":"9","total":"33"},{"country":"Romania","gold":"17","silver":"2","bronze":"6","total":"25"},{"country":"Netherlands","gold":"17","silver":"13","bronze":"13","total":"43"},{"country":"South Korea","gold":"18","silver":"17","bronze":"4","total":"39"},{"country":"Germany","gold":"19","silver":"14","bronze":"13","total":"46"},{"country":"Russia","gold":"27","silver":"12","bronze":"14","total":"53"},{"country":"Australia","gold":"41","silver":"46","bronze":"28","total":"115"},{"country":"China","gold":"42","silver":"20","bronze":"18","total":"80"},{"country":"United States","gold":"121","silver":"82","bronze":"54","total":"257"}],"lastRow":35}

        assert(len(rows['rows']) == len(angular_rows['rows']))
        rr = rows['rows']
        ar = angular_rows['rows']
        assert(all(r['gold'] == a['gold'] for r,a in zip(rr, ar)))
    
        
def test_groupby_country_sortby_gold_desc():

    group_model = '''{"startRow":0,"endRow":100,"rowGroupCols":[{"id":"country","displayName":"Country","field":"country"}],"valueCols":[{"id":"gold","aggFunc":"sum","displayName":"Gold","field":"gold"},{"id":"silver","aggFunc":"sum","displayName":"Silver","field":"silver"},{"id":"bronze","aggFunc":"sum","displayName":"Bronze","field":"bronze"},{"id":"total","aggFunc":"sum","displayName":"Total","field":"total"}],"pivotCols":[],"pivotMode":false,"groupKeys":[],"filterModel":{},"sortModel":[{"sort":"desc","colId":"gold"}]}'''


    with app.test_client() as client:
        response = client.post("/api/olympicWinners/", data=group_model)
        rows = json.loads(response.data)

        ar = ['121', '42', '41', '27', '19', '18', '17', '17', '16', '10', '10', '9', '8', '7', '7', '5', '4', '4', '3', '3', '3', '3', '2', '2', '2', '2', '1', '1', '1', '1', '0', '0', '0', '0', '0']
        
        assert(len(rows['rows']) == len(ar))
        rr = rows['rows']

        assert(all(r['gold'] == a for r,a in zip(rr, ar)))
    
