import unittest
import time
import sys
import os

import underworlds
import underworlds.server
from underworlds.tools.loader import ModelLoader
from underworlds.tools.spatial_relations import *
from underworlds.tools.edit import *

from placement_description import *

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
        description = gen_spatial_desc(self.ctx, worldName, inNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "Inside is in Main")
        
        onNode = world.scene.nodebyname("OnTop")[0]
        description = gen_spatial_desc(self.ctx, worldName, onNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "OnTop is on top of Main")
        
        mainNode = world.scene.nodebyname("Main")[0]
        description = gen_spatial_desc(self.ctx, worldName, mainNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "Main is above Below")
        
        belowNode = world.scene.nodebyname("Below")[0]
        description = gen_spatial_desc(self.ctx, worldName, belowNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "Below is below Main") 
        
        southNode = world.scene.nodebyname("object")[0]
        description = gen_spatial_desc(self.ctx, worldName, southNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "the object is to the south of Main")
        
        description = gen_spatial_desc(self.ctx, worldName, southNode.id, "default", [], "en_GB", "Simple")
        print(description)
        self.assertTrue(description == "the object is to the front of Main")
        
        
        northNode = world.scene.nodebyname("ToNorth")[0]
        northNode.name = "object"
        world.scene.nodes.update(northNode)
        description = gen_spatial_desc(self.ctx, worldName, northNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "an object is to the north of Main")
        
        description = gen_spatial_desc(self.ctx, worldName, northNode.id, "default", [], "en_GB", "Simple")
        print(description)
        self.assertTrue(description == "an object is to the back of Main")
        
        eastNode = world.scene.nodebyname("cube")[0]
        description = gen_spatial_desc(self.ctx, worldName, eastNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "the cube is to the east of Main")
        
        description = gen_spatial_desc(self.ctx, worldName, eastNode.id, "default", [], "en_GB", "Simple")
        print(description)
        self.assertTrue(description == "the cube is to the right of Main")
        
        westNode = world.scene.nodebyname("ToWest")[0]
        westNode.name = "cube"
        world.scene.nodes.update(westNode)
        description = gen_spatial_desc(self.ctx, worldName, westNode.id, None, [], "en_GB", "Simple")
        
        print(description)
        self.assertTrue(description == "a cube is to the west of Main")
        
        description = gen_spatial_desc(self.ctx, worldName, westNode.id, "default", [], "en_GB", "Simple")
        print(description)
        self.assertTrue(description == "a cube is to the left of Main")
        
    def test_non_ambig_descriptions(self):
        
        worldName = "base"
        world = self.ctx.worlds[worldName]
        
        ModelLoader().load("../map/map_wEmpty.blend", world=worldName)
        time.sleep(2) # leave some time for the loader to finish
        
        target_node = world.scene.nodebyname("empty_space-2")[0]
        target_node2 = world.scene.nodebyname("police_department")[0]
        for node in world.scene.nodes:
            format_name(worldName, node.id)
            
        description = gen_spatial_desc(self.ctx, worldName, target_node.id, "default", [], "en_GB", "NonAmbig")
        print description
        
        description = gen_spatial_desc(self.ctx, worldName, target_node2.id, "default", [], "en_GB", "NonAmbig")
        print description
        
    def tearDown(self):
        self.ctx.close()
    
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDescriptions)
    return suite


if __name__ == '__main__':
    unittest.main()
