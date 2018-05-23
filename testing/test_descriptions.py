import unittest
import time
import sys
import os

import underworlds
import underworlds.server
from underworlds.tools.loader import ModelLoader
from underworlds.tools.spatial_relations import *

#Included until I setup an installer
sl = os.path.dirname(__file__)
sys.path.append(os.path.join(sl, '..', 'src'))

from spatial_desc import *

#Check that the descriptions generated are the ones expected.

class TestDescriptions(unittest.TestCase):
    
    # workaround for https://github.com/grpc/grpc/issues/14088
    @classmethod
    def setUpClass(cls):
        cls.server = underworlds.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(1).wait()

    def setUp(self):
        # workaround for https://github.com/grpc/grpc/issues/14088
        #self.server = underworlds.server.start()

        self.ctx = underworlds.Context("unittest - edit tools")

        # workaround for https://github.com/grpc/grpc/issues/14088
        self.ctx.reset()
    
    def test_simple_descriptions(self):
        
        worldName = "base"
        world = self.ctx.worlds[worldName]
        
        ModelLoader().load("res/spatialDescSimple.blend", world=worldName)
        time.sleep(1) # leave some time for the loader to finish
        
        inNode = world.scene.nodebyname("Inside")[0]
        description = gen_spatial_desc(worldName, inNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "Inside is in Main")
        
    def tearDown(self):
        self.ctx.close()
    
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDescriptions)
    return suite


if __name__ == '__main__':
    unittest.main()
