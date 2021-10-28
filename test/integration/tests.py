from flaskr import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'DATABASE': db_path})
    with app.test_client() as client:
        yield client


def test_1(client):
    data = client.get()
    assert(data)
