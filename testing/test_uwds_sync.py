import unittest
import time

#Check that uwds is syncing with published TF's. Check relations reported.

class TestUwdsSync(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def test_uwds_sync(self):
		self.assertTrue(False) #Not yet implemented
	
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUwdsSync)
    return suite


if __name__ == '__main__':
    unittest.main()
