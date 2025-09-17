import unittest
import pylanche

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = pylanche.client()

    def test_receive(self):
        self.client.receive()

    def test_send(self):
        self.client.send()

if __name__ == "__main__":
    unittest.main()