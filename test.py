import unittest
import pylanche
import azure.functions as func

from function_app import http_trigger

class TestFunction(unittest.TestCase):
    def test_http_trigger_receive(self):
        request = func.HttpRequest(method='POST',
                                   body = None,
                                   url='/api/http_trigger',
                                   params = {'operation': 'receive'}
        ) # input request

        f = http_trigger.build().get_user_function()

        response = f(request) # output response
        print(response.status_code)

'''
class TestClient(unittest.TestCase):
    def setUp(self):
        self.consumer = pylanche.Client(op="receive")
        self.producer = pylanche.Client(op="send")

    def test_receive(self):
        self.consumer.perform(op="receive")

    def test_send(self):
        self.producer.perform(op="send")
'''

class TestProcess(unittest.TestCase):
    def test_parse_valid(self):
        message = '{"id": "0"}' # input JSON message
        data_ans = {'id': "0"} # expected dict

        data_out = pylanche.process.parse(message) # output dict

        self.assertEqual(data_out, data_ans)

    def test_parse_invalid(self):
        message = "test" # input message
        value_ans = None # expected return value

        value_out = pylanche.process.parse(message) # output value

        self.assertEqual(value_out, value_ans)

if __name__ == "__main__":
    unittest.main()