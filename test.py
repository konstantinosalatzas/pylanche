import unittest
import pylanche

class TestClient(unittest.TestCase):
    def setUp(self):
        self.consumer = pylanche.Client(op="receive")
        self.producer = pylanche.Client(op="send")

    def test_receive(self):
        self.consumer.perform(op="receive")

    def test_send(self):
        self.producer.perform(op="send")

class TestProcess(unittest.TestCase):
    def test_parse_valid(self):
        message = '{"id": "0"}' # input JSON message
        data_ans = {'id': "0"} # expected dict

        data_out = pylanche.process.parse(message) # output dict

        self.assertEqual(data_out, data_ans)

if __name__ == "__main__":
    unittest.main()