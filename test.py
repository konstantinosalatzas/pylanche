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

if __name__ == "__main__":
    unittest.main()