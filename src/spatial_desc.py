import os
import sys
import math
import rospy
import numpy
import geometry_msgs.msg
import enchant

import underworlds
from underworlds.tools.spatial_relations import *

import logging; logger = logging.getLogger("spatial_description")

def isin(lang="en_GB"):

    if lang=="en_GB":
        return "in"
    else:
        raise NotImplementedError
        
def isontop(lang="en_GB"):

    if lang=="en_GB":
        return "on top of"
    else:
        raise NotImplementedError
        
def isabove(lang="en_GB"):

    if lang=="en_GB":
        return "above"
    else:
        raise NotImplementedError
        
def isbelow(lang="en_GB"):
    
    if lang=="en_GB":
        return "below"
    else:
        raise NotImplementedError
        
def isclose(lang="en_GB"):

    if lang=="en_GB":
        return "close to"
    else:
        raise NotImplementedError
        
def istonorth(lang="en_GB"):

    if lang=="en_GB":
        return "to the north of"
    else:
        raise NotImplementedError
        
def istoeast(lang="en_GB"):

    if lang=="en_GB":
        return "to the east of"
    else:
        raise NotImplementedError
        
def istosouth(lang="en_GB"):

    if lang=="en_GB":
        return "to the south of"
    else:
        raise NotImplementedError
        
def istowest(lang="en_GB"):

    if lang=="en_GB":
        return "to the west of"
    else:
        raise NotImplementedError

def get_desc_relation(relation, lang="en_GB"):
    
    if relation == "in":
        return isin(lang)
        
    elif relation == "onTop":
        return isontop(lang)
        
    elif relation == "above":
        return isabove(lang)
        
    elif relation == "below":
		return isbelow(lang)
        
    elif relation == "close":
        return isclose(lang)
        
    elif relation == "toNorth":
        return istonorth(lang)
        
    elif relation == "toEast":
        return istoeast(lang)
        
    elif relation == "toSouth":
        return istosouth(lang)
        
    elif relation == "toWest":
        return istowest(lang)
        
    else:
        raise NotImplementedError

def add_noun_article(noun, amount, lang="en_GB"):
    
    d = enchant.Dict(lang)
    
    if noun[0].isupper() or d.check(noun) == False:
        #assume that it is a proper noun
        return noun
    elif lang=="en_GB":
        #regular noun
        vowels = ["a", "e", "i", "o", "u"]
        if amount == 1:
            return "the %s" % noun
        else:
            if noun[0] in vowels:
                return "an %s" % noun
            else:
                return "a %s" % noun
                
    else:
        raise NotImplementedError
        
        
def amb_desc(worldName, rel_list, iteration, lang="en_GB"):
    
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
        
        if iteration == 0:
            node1 = world.scene.nodes[rel_list[iteration][1]]
            amount1 = len(world.scene.nodebyname(node1.name))
            
            noun1 = add_noun_article(node1.name, amount1, lang)
            
            description = noun1 + " is " + description
    
    return description

def gen_spatial_desc(worldName, nodeID, lang="en_GB", descType = "Simple"):
    
    #Retrieve the spatial relations and sort them by priority    
    rel_list = sorted(get_node_sr(worldName, nodeID))
        
    if descType == "Simple":
        #Getting a simple one word description so only check the first relation
        description = amb_desc(worldName, rel_list, 0, lang)
    else:
        raise NotImplementedError
    
    return description
    
if __name__ == "__main__":
    
    print("Finished")
