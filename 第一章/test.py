import unittest
from procsmem import bytes2human


class TestPsutil(unittest.TestCase):
    """docstring for TestPsutil"""
    def test_bytes2human(self):
    	print(bytes2human(4096))
    	print(bytes2human(454525325))

if __name__ == '__main__':
    unittest.main()
