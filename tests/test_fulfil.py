import requests


def test_example_fulfil(url):
    payload = {
      "lines": [
        {
          "sku": 'abc',
          "quantity": 12
        },
        {
          "sku": 'def',
          "quantity": 2
        }
      ]
    }
    r = requests.post(url + '/api/fulfil', json=payload)
    assert r.status_code == 200

