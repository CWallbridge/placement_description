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
        
        onNode = world.scene.nodebyname("OnTop")[0]
        description = gen_spatial_desc(worldName, onNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "OnTop is on top of Main")
        
        mainNode = world.scene.nodebyname("Main")[0]
        description = gen_spatial_desc(worldName, mainNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "Main is above Below")
        
        belowNode = world.scene.nodebyname("Below")[0]
        description = gen_spatial_desc(worldName, belowNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "Below is below Main") 
        #Technically correct but unlikely and even confusing that someone would say the second two. Need to think about how this would prioritise for complex description.
        
        southNode = world.scene.nodebyname("object")[0]
        description = gen_spatial_desc(worldName, southNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "the object is to the south of Main")
        
        northNode = world.scene.nodebyname("ToNorth")[0]
        northNode.name = "object"
        world.scene.nodes.update(northNode)
        description = gen_spatial_desc(worldName, northNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "an object is to the north of Main")
        
        eastNode = world.scene.nodebyname("cube")[0]
        description = gen_spatial_desc(worldName, eastNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "the cube is to the east of Main")
        
        westNode = world.scene.nodebyname("ToWest")[0]
        westNode.name = "cube"
        world.scene.nodes.update(westNode)
        description = gen_spatial_desc(worldName, westNode.id, "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "a cube is to the west of Main")
        
    def tearDown(self):
        self.ctx.close()
    
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDescriptions)
    return suite


if __name__ == '__main__':
    unittest.main()
