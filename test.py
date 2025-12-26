import unittest
import pylanche
import azure.functions as func

from function_app import http_trigger

# end-to-end tests
class TestFunctionApp(unittest.TestCase):
    def test_http_trigger_receive(self):
        request = func.HttpRequest(method="POST",
                                   body=None,
                                   url="/api/http_trigger",
                                   params={"operation": "receive",
                                           "duration": 3}) # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 200)

    def test_http_trigger_send(self):
        request = func.HttpRequest(method="POST",
                                   body=None,
                                   url="/api/http_trigger",
                                   params={"operation": "send",
                                           "count": 3}) # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 200)

    def test_http_trigger_anonymize(self):
        request = func.HttpRequest(method="POST",
                                   body=None,
                                   url="/api/http_trigger",
                                   params={"operation": "anonymize",
                                           "text": "Konstantinos did a planche hold to press."}) # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 200)

    def test_http_trigger_no_op(self):
        request = func.HttpRequest(method="POST",
                                   body="{}".encode(),
                                   url="/api/http_trigger") # input request

        f = http_trigger.build().get_user_function()
        response = f(request) # output response

        self.assertEqual(response.status_code, 400)

# unit tests

class TestConfig(unittest.TestCase):
    def test_get_config_valid(self):
        config = {"BLOB_STORAGE_CONNECTION_STRING": "val1",
                  "BLOB_CONTAINER_NAME": "val2",
                  "EVENT_HUB_CONNECTION_STRING": "val3",
                  "EVENT_HUB_NAME": "val4",
                  "FILE_NAME": "val5",
                  "LANGUAGE_KEY": "val6",
                  "LANGUAGE_ENDPOINT": "val7"} # input dict
        ret_ans = ("val1", "val2", "val3", "val4", "val5", "val6", "val7") # expected tuple

        ret_out = pylanche.utils.get_config(config) # output return

        self.assertEqual(ret_out, ret_ans)
    
    def test_get_config_invalid(self):
        config = {"key": "value"} # input dict
        ret_ans = None # expected return

        ret_out = pylanche.utils.get_config(config) # output return

        self.assertEqual(ret_out, ret_ans)

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

class TestAnonymize(unittest.TestCase):
    def test_anonymize_text(self):
        text = "Konstantinos" # input text
        text_ans = "XXXXXXXXXXXX" # expected text

        text_out = pylanche.anonymize.anonymize_text(text) # output text

        self.assertEqual(text_out, text_ans)
    
    def test_replace_mapped(self):
        text = "Konstantinos did a planche hold to press." # input text
        map = {"Konstantinos": "XXXXXXXXXXXX"} # input dict
        text_ans = "XXXXXXXXXXXX did a planche hold to press." # expected text

        text_out = pylanche.anonymize.replace_mapped(text, map) # output text

        self.assertEqual(text_out, text_ans)

if __name__ == "__main__":
    unittest.main()