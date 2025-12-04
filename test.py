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
        message = '{"id": "test"}' # input JSON string message
        data_ans = {"id": "test"} # expected dict

        ret_out = pylanche.process.parse(message) # output return

        self.assertEqual(ret_out, data_ans)

    def test_parse_invalid(self):
        message = "test" # input message
        ret_ans = None # expected return

        ret_out = pylanche.process.parse(message) # output return

        self.assertEqual(ret_out, ret_ans)

class TestConfig(unittest.TestCase):
    def test_get_config_valid(self):
        config = {"BLOB_STORAGE_CONNECTION_STRING": "value1",
                  "BLOB_CONTAINER_NAME": "value2",
                  "EVENT_HUB_CONNECTION_STRING": "value3",
                  "EVENT_HUB_NAME": "value4",
                  "RECEIVE_DURATION": "value5",
                  "SEND_COUNT": "value6"} # input dict
        ret_ans = ("value1", "value2", "value3", "value4", "value5", "value6") # expected tuple

        ret_out = pylanche.get_config(config) # output return

        self.assertEqual(ret_out, ret_ans)
    
    def test_get_config_invalid(self):
        config = {"key": "value"} # input dict
        ret_ans = None # expected return

        ret_out = pylanche.get_config(config) # output return

        self.assertEqual(ret_out, ret_ans)

class TestState(unittest.TestCase):
    def setUp(self):
        self.state = pylanche.State(id="id")

if __name__ == "__main__":
    unittest.main()