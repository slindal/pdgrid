from src.server import app


def test_no_grouping_or_sorting():
    with app.test_client() as client:

        group_model = '{"startRow":0,"endRow":100,"rowGroupCols":[],"valueCols":[{"id":"gold","aggFunc":"sum","displayName":"Gold","field":"gold"},{"id":"silver","aggFunc":"sum","displayName":"Silver","field":"silver"},{"id":"bronze","aggFunc":"sum","displayName":"Bronze","field":"bronze"},{"id":"total","aggFunc":"sum","displayName":"Total","field":"total"}],"pivotCols":[],"pivotMode":false,"groupKeys":[],"filterModel":{},"sortModel":[]}'
        
        response = client.get("/api/olympicWinners", data=group_model)
        import ipdb; ipdb.set_trace()
        print(data)
        assert(data)
