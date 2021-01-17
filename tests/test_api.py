try:
    from app import create_app
except ModuleNotFoundError:
    import os,sys
    from os.path import dirname, join, abspath
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))    
    from app import create_app

import unittest
import json

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_header_form_data(self):
        return {'Content-Type': 'multipart/form-data'}

    def get_header_json_data(self):
        return {'Content-Type': 'application/json'}

    def test_get_method_form_data(self):
        response = self.client.get('/',headers=self.get_header_form_data())
        self.assertTrue(response.status_code == 405)

    def test_post_method_form_data(self):
        response = self.client.post('/',headers=self.get_header_form_data())
        self.assertTrue(response.status_code == 400)

    def test_put_method_form_data(self):
        response = self.client.put('/',headers=self.get_header_form_data())
        self.assertTrue(response.status_code == 405)

    def test_delete_method_form_data(self):
        response = self.client.delete('/',headers=self.get_header_form_data())
        self.assertTrue(response.status_code == 405)

    def test_get_hello_json_data(self):
        response = self.client.get('/hello',headers=self.get_header_json_data())
        self.assertTrue(response.status_code == 404)

    def test_post_payment_empty_json_data(self):
        response = self.client.post('/',headers=self.get_header_json_data(),data=json.dumps({}))
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),4)
        self.assertIn('CreditCardNumber',resp_json)
        self.assertIn('CardHolder',resp_json)
        self.assertIn('ExpirationDate',resp_json)
        self.assertIn('Amount',resp_json)

    def test_payment_mandatory_CreditCardNumber(self):
        _data = json.dumps({
            "CreditCardNumber":"",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('CreditCardNumber',resp_json)

    def test_payment_CreditCardNumber_length_15(self):
        _data = json.dumps({
            "CreditCardNumber":"123456781234567",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('CreditCardNumber',resp_json)

    def test_payment_CreditCardNumber_length_17(self):
        _data = json.dumps({
            "CreditCardNumber":"12345678123456789",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('CreditCardNumber',resp_json)


    def test_payment_mandatory_CardHolder(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('CardHolder',resp_json)

    def test_payment_mandatory_ExpirationDate(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('ExpirationDate',resp_json)

    def test_payment_ExpirationDate_format(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"01-22",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('ExpirationDate',resp_json)

    def test_payment_ExpirationDate_past(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"01/21",
            "SecurityCode":"123",
            "Amount": 150.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('ExpirationDate',resp_json)

    def test_payment_mandatory_Amount(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": None
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('Amount',resp_json)

    def test_payment_Amount_not_positive(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": -10
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('Amount',resp_json)

    def test_payment_Amount_zero_positive(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 0
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 400)
        resp_json = response.get_json()
        self.assertEqual(len(resp_json),1)
        self.assertIn('Amount',resp_json)

    def test_payment_with_data_amount_less_than_20(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 19.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 200)

    def test_payment_with_data_amount_greater_than_20(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 21.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 200)

    def test_payment_with_data_amount_between_20_500(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 250.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 200)

    def test_payment_with_data_amount_equal_to_500(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 500.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 200)

    def test_payment_with_data_amount_greater_than_500(self):
        _data = json.dumps({
            "CreditCardNumber":"1234567812345678",
            "CardHolder":"Name",
            "ExpirationDate":"02/22",
            "SecurityCode":"123",
            "Amount": 501.00
        },indent=4)
        response = self.client.post('/',headers=self.get_header_json_data(),data=_data)
        self.assertTrue(response.status_code == 200)

if __name__ == '__main__':
    unittest.main()