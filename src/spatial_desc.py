import os
import sys
import math
import rospy
import numpy
import geometry_msgs.msg
import enchant
import gc

import underworlds
from underworlds.helpers.geometry import get_bounding_box_for_node
from underworlds.tools.spatial_relations import *

import logging; logger = logging.getLogger("spatial_description")

def isindesc(lang="en_GB"):

    if lang=="en_GB":
        return "in"
    else:
        raise NotImplementedError
        
def isontopdesc(lang="en_GB"):

    if lang=="en_GB":
        return "on top of"
    else:
        raise NotImplementedError
        
def isabovedesc(lang="en_GB"):

    if lang=="en_GB":
        return "above"
    else:
        raise NotImplementedError
        
def isbelowdesc(lang="en_GB"):
    
    if lang=="en_GB":
        return "below"
    else:
        raise NotImplementedError
        
def isclosedesc(lang="en_GB"):

    if lang=="en_GB":
        return "close to"
    else:
        raise NotImplementedError

def istobackdesc(lang="en_GB", two_dim = False):

    if lang=="en_GB":
        if two_dim == False:
            return "to the back of"
        else:
            return "above"
    else:
        raise NotImplementedError
        
def istorightdesc(lang="en_GB"):

    if lang=="en_GB":
        return "to the right of"
    else:
        raise NotImplementedError
        
def istofrontdesc(lang="en_GB", two_dim = False):
    if lang=="en_GB":
        if two_dim == False:
            return "to the front of"
        else:
            return "below"
    else:
        raise NotImplementedError
        
def istoleftdesc(lang="en_GB"):

    if lang=="en_GB":
        return "to the left of"
    else:
        raise NotImplementedError
      
def istonorthdesc(lang="en_GB"):

    if lang=="en_GB":
        return "to the north of"
    else:
        raise NotImplementedError
        
def istoeastdesc(lang="en_GB"):

    if lang=="en_GB":
        return "to the east of"
    else:
        raise NotImplementedError
        
def istosouthdesc(lang="en_GB"):

    if lang=="en_GB":
        return "to the south of"
    else:
        raise NotImplementedError
        
def istowestdesc(lang="en_GB"):

    if lang=="en_GB":
        return "to the west of"
    else:
        raise NotImplementedError

def get_desc_relation(relation, lang="en_GB", two_dim=False):
    
    if relation == "in":
        return isindesc(lang)
        
    elif relation == "onTop":
        return isontopdesc(lang)
        
    elif relation == "above":
        return isabovedesc(lang)
        
    elif relation == "below":
        return isbelowdesc(lang)
        
    elif relation == "close":
        return isclosedesc(lang)
        
    elif relation == "toBack":
        return istobackdesc(lang, two_dim)
        
    elif relation == "toRight":
        return istorightdesc(lang)
        
    elif relation == "toFront":
        return istofrontdesc(lang, two_dim)
        
    elif relation == "toLeft":
        return istoleftdesc(lang)
        
    elif relation == "toNorth":
        return istonorthdesc(lang)
        
    elif relation == "toEast":
        return istoeastdesc(lang)
        
    elif relation == "toSouth":
        return istosouthdesc(lang)
        
    elif relation == "toWest":
        return istowestdesc(lang)
        
    else:
        raise NotImplementedError

def add_noun_article(noun, amount, lang="en_GB"):
    
    if noun[0] == "_":
        return noun
    
    d = enchant.Dict(lang)
    
    nouns = noun.split(" ")
    
    if noun[0].isupper() or d.check(nouns[0]) == False:
        #assume that it is a proper noun
        return noun
    elif lang=="en_GB":
        #regular noun
        vowels = ["a", "e", "i", "o", "u"]
        if amount == 1:
            return "the %s" % (noun)
        else:
            if noun[0] in vowels:
                return "an %s" % (noun)
            else:
                return "a %s" % (noun)
                
    else:
        raise NotImplementedError

def sr_desc(worldName, rel_list, iteration, lang="en_GB"):
    
    if iteration >= len(rel_list):
        return rel_list, "", ""
    
    rel_list = check_for_exclusions(worldName, rel_list, iteration)
    
    with underworlds.Context("spatial_description") as ctx:
        world = ctx.worlds[worldName]
        
        node2 = world.scene.nodes[rel_list[iteration][2]]
        amount2 = len(world.scene.nodebyname(node2.name))
        
        noun2 = add_noun_article(node2.name, amount2, lang)
        
        sr_desc = get_desc_relation(rel_list[iteration][3], lang)
        
        if lang=="en_GB":
            description = sr_desc + " " + noun2 
        else:
            raise NotImplementedError
        
        part1 = ", "
        
        if iteration == 0:
            node1 = world.scene.nodes[rel_list[iteration][1]]
            amount1 = len(world.scene.nodebyname(node1.name))
            
            if lang=="en_GB":
                part1 = add_noun_article(node1.name, amount1, lang) + " is "
            else:
                raise NotImplementedError   
    
    return rel_list, description, part1

def non_ambig_desc(worldName, rel_list, camera, add_node_chks=[], lang="en_GB"):

    with underworlds.Context("spatial_description") as ctx:
        world = ctx.worlds[worldName]
        desc_node = world.scene.nodes[rel_list[0][1]]
        
        node_list = world.scene.nodebyname(desc_node.name) + add_node_chks
        
        node_list.remove(desc_node)
        
        i = 0
        
        description = ""
        
        node_skip = []
        
        while len(node_list) > len(node_skip) and i < len(rel_list):
        
            rel_list, desc, part1 = sr_desc(worldName, rel_list, i, lang)
            
            for node2 in node_list:
                
                if node2 in node_skip:
                    continue
                
                try:
                    rel_list2 = node2.relList
                except AttributeError:
                    rel_list2 = sorted(get_node_sr(worldName, node2.id, camera))
            
                rel_list2, desc2, _ = sr_desc(worldName, rel_list2, i, lang)
                
                if desc == desc2:
                    node2.relList = rel_list2
                else:
                    node_skip.append(node2)
            
            description += part1 + desc
                
            i += 1
            
            gc.collect()

    return description

def gen_spatial_desc(worldName, nodeID, camera=None, add_node_chks=[], lang="en_GB", descType = "Simple"):
    
    #Retrieve the spatial relations and sort them by priority    
    rel_list = sorted(get_node_sr(worldName, nodeID, camera))
    
    if len(rel_list) == 0:
        description = "No relations for Node %s" % nodeID
        return description
        
    if descType == "Simple":
        #Getting a simple one level description so only check the first relation
        rel_list, description, part1 = sr_desc(worldName, rel_list, 0, lang)
        description = part1 + description
    elif descType == "NonAmbig":
        description = non_ambig_desc(worldName, rel_list, camera, add_node_chks, lang)
    else:
        raise NotImplementedError
    
    return description
    
if __name__ == "__main__":
    
    print("Finished")
