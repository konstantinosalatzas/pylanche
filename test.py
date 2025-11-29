import unittest
import pylanche
import azure.functions as func

from function_app import http_trigger

class TestFunctionApp(unittest.TestCase):
    def test_http_trigger_receive(self):
        request = func.HttpRequest(method="POST",
                                   body=None,
                                   url="/api/http_trigger",
                                   params={"operation": "receive"}
        ) # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 200)

    def test_http_trigger_send(self):
        request = func.HttpRequest(method="POST",
                                   body=None,
                                   url="/api/http_trigger",
                                   params={"operation": "send"}
        ) # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 200)

    def test_http_trigger_no_op(self):
        request = func.HttpRequest(method="POST",
                                   body="{}".encode(),
                                   url="/api/http_trigger"
        ) # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 400)

class TestProcess(unittest.TestCase):
    def test_parse_valid(self):
        message = '{"id": "test"}' # input JSON message
        data_ans = {"id": "test"} # expected dict

        data_out = pylanche.process.parse(message) # output dict

        self.assertEqual(data_out, data_ans)

    def test_parse_invalid(self):
        message = "test" # input message
        value_ans = None # expected return value

        value_out = pylanche.process.parse(message) # output value

        self.assertEqual(value_out, value_ans)

class TestConfig(unittest.TestCase):
    def test_get_config_valid(self):
        config = {"BLOB_STORAGE_CONNECTION_STRING": "value1",
                  "BLOB_CONTAINER_NAME": "value2",
                  "EVENT_HUB_CONNECTION_STRING": "value3",
                  "EVENT_HUB_NAME": "value4",
                  "RECEIVE_DURATION": "value5",
                  "SEND_COUNT": "value6"} # input dict
        ret_ans = ("value1", "value2", "value3", "value4", "value5", "value6") # expected return tuple

        ret_out = pylanche.get_config(config) # output tuple

        self.assertEqual(ret_out, ret_ans)
    
    def test_get_config_invalid(self):
        config = {"key": "value"} # input dict
        ret_ans = None # expected return

        ret_out = pylanche.get_config(config) # output return

        self.assertEqual(ret_out, ret_ans)

if __name__ == "__main__":
    unittest.main()