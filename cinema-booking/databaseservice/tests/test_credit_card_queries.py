import json
from unittest.mock import patch

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_test_database_uri'  # Update this to your test database URI


def test_add_credit_card():
    with app.test_client() as client:
        with patch('your_module.db', db):
            data = {
                'userId': 'example_user_id',
                'blob': 'example_blob',
            }
            response = client.post('/add_credit_card', data=json.dumps(data), content_type='application/json')
            assert response.status_code == 201
            assert json.loads(response.data) == {'message': 'CreditCard added successfully'}


def test_get_credit_card_by_id():
    with app.test_client() as client:
        with patch('your_module.db', db):
            response = client.get('/get_credit_card_by_id/example_user_id/1')
            assert response.status_code in [200, 403, 404]


def test_get_all_credit_cards():
    with app.test_client() as client:
        with patch('your_module.db', db):
            response = client.get('/get_all_credit_cards/example_user_id')
            assert response.status_code in [200, 404]


def test_update_credit_card():
    with app.test_client() as client:
        with patch('your_module.db', db):
            data = {
                'creditCardId': 1,
                'userId': 'example_user_id',
                'blob': 'example_blob_updated',
            }
            response = client.put('/update_credit_card', data=json.dumps(data), content_type='application/json')
            assert response.status_code in [200, 403]


def test_delete_credit_card_by_id():
    with app.test_client() as client:
        with patch('your_module.db', db):
            response = client.delete('/delete_credit_card_by_id/example_user_id/1')
            assert response.status_code in [200, 403]
