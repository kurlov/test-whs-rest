import requests


def test_search_order(url):
    requests.post(url + '/api/orders', json=dict(customer='Thomas Müller'))
    response = requests.get(url + '/api/search?q=muller')
    assert response.json() == {'result': 'Thomas Müller'}

    # exact name
    response = requests.get(url + '/api/search?q=Müller')
    assert response.json() == {'result': 'Thomas Müller'}

    # unknown name
    response = requests.get(url + '/api/search?q=sasha')
    assert response.json() == {'message': 'no orders for sasha'}
