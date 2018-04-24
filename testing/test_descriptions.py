import unittest
import time

#Check that the descriptions generated are the ones expected.

class TestDescriptions(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def test_descriptions(self):
		self.assertTrue(False) #Not yet implemented
	
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDescriptions)
    return suite


if __name__ == '__main__':
    unittest.main()
