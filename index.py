import requests
import pprint

class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, data=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True

            pprint.pprint(f'{request_type} example')
            pprint.pprint(response.url)
            pprint.pprint(response.status_code)
            pprint.pprint(response.reason)
            pprint.pprint(response.text)
            pprint.pprint(response.json())
            pprint.pprint('**********')
            return response

    def get(self, entity, entity_id, expected_error=False):
        url = f'{self.base_url}/{entity}/{entity_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json()

    def post(self, entity, entity_id, body):
        url = f'{self.base_url}/{entity}/{entity_id}'
        response = self._request(url, 'POST', data=body)
        return response.json()['message']

    def delete(self, entity, entity_id):
        url = f'{self.base_url}/{entity}/{entity_id}'
        response = self._request(url, 'DELETE')
        return response.json()['message']

BASE_URL_API = 'https://your-api-url.com'  # Замените 'https://your-api-url.com' на ваш URL
base_request = BaseRequest(BASE_URL_API)

user_info = base_request.get('user', 'user123')
pprint.pprint(user_info)

new_user_data = {
    'id': 123,
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'phone': '1234567890'
}
response_message = base_request.post('user', 'create', new_user_data)
print(response_message)

delete_response_message = base_request.delete('user', 'delete', entity_id=123)
print(delete_response_message)

store_info = base_request.get('store', 'store123')
pprint.pprint(store_info)

new_order_data = {
    'id': 456,
    'product': 'Product Name',
    'quantity': 1,
    'order_date': '2023-10-06T10:00:00Z',
    'status': 'placed'
}
response_message = base_request.post('store', 'order', new_order_data)
print(response_message)

delete_response_message = base_request.delete('store', 'delete', entity_id=456)
print(delete_response_message)
