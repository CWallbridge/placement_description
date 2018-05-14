#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import math
import rospy
import tf
import numpy
import geometry_msgs.msg

import underworlds
from underworlds.tools.edit

import logging; logger = logging.getLogger("placement_description.uwds_sync")
logging.basicConfig(level=logging.INFO)

class NodeFrame(object)
    
    def __init__(self, idFrame, trans, rot, world, model=None, parent="root"):
        self.id = idFrame
        self._world = world
        self._frameNode = self._create_mesh_node(world, idFrame, model, parent)
        self.transform_node(trans, rot)
        
    def _create_mesh_node(self, world, node, model, parent):
        if model is None:
            mesh_ids = create_box_mesh(world, 0.02, 0.02, 0.02)
        else:
            mesh_ids = load_mesh(world, model)
            
        create_mesh_node(world, node, mesh_ids, parent)
        frameNode = world.scene.nodebyname(node)
        
        if len(frameNode) > 1:
			logger.warning("More than one node of the same name found.")
		
        return frameNode[0].id
        
    def transform_node(self, trans, rot):
		self._trans = trans
		self._rot = rot
		
		tfMatrix = tf.TransformerROS.fromTranslationRotation(trans, rot)
		
		with underworlds.Context("uwds_sync") as ctx:
            world = ctx.worlds[self._world]
            node = world.scene.nodes[self._frameNode]
            
            node.transformation = tfMatrix
            scene.nodes.update(node)		
		  
    @property    
    def trans(self)
		return self._trans
	
	@property
	def rot(self)
		return self._rot
	
	@property
	def 

        

class UwdsSync(object):
    
    def __init__(self)
        self.nodeFrames = {}
    

if __name__ == "__main__":
    
    print("Finished")
