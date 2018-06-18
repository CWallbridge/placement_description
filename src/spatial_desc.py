import os
import sys
import math
import rospy
import numpy
import geometry_msgs.msg
import enchant

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

def get_desc_relation(relation, lang="en_GB"):
    
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
             
def check_for_exclusions(worldname, rel_list, iteration):

    i = 0
    relation = rel_list[iteration][3]
    
    if iteration > 0:
        if relation == rel_list[iteration - 1][3]:
            #These relations should have already been checked in a previous iteration.
            return rel_list
    
    rel_poss_excl = []
    
    #Get a list of all the nodes that have the same relation to our current node
    while  (iteration + i) < len(rel_list) and rel_list[iteration + i][3] == relation:
        rel_poss_excl.append([rel_list[iteration + i][2], i])
        i += 1
    
    length = len(rel_poss_excl)
        
    if length > 1:
        i = 0
        rel_excl = []
        while(i < length):
            
            j = 0
            
            with underworlds.Context("spatial_description") as ctx:
                world = ctx.worlds[worldname]
                
                node1 = world.scene.nodes[rel_poss_excl[i][0]]
                bb1 = get_bounding_box_for_node(world.scene, node1)
                
                while (j < length):
                    
                    if i == j or j in rel_excl:
                        j += 1
                        continue
                        
                    node2 = world.scene.nodes[rel_poss_excl[j][0]]
                    bb2 = get_bounding_box_for_node(world.scene, node2)
                    
                    if relation == "in":
                        if isin(bb1, bb2):
                            rel_excl.append(j) #Append to list to be deleted afterward
                            
                    elif relation == "onTop":
                        pass
                        
                    elif relation == "above":
                        if isin(bb2, bb1) or isabove(bb2, bb1):
                            rel_excl.append(j)
                        
                    elif relation == "below":
                        if isin(bb2, bb1) or isbelow(bb2, bb1) or isontop(bb2, bb1):
                            rel_excl.append(j)
                        
                    elif relation == "close":
                        pass
                        
                    elif relation == "toNorth":
                        if isin(bb2, bb1) or istonorth(bb2, bb1):
                            rel_excl.append(j)
                        
                    elif relation == "toEast":
                        if isin(bb2, bb1) or istoeast(bb2, bb1):
                            rel_excl.append(j)
                        
                    elif relation == "toSouth":
                        if isin(bb2, bb1) or istoeast(bb2, bb1):
                            rel_excl.append(j)
                        
                    elif relation == "toWest":
                        if isin(bb2, bb1) or istowest(bb2, bb1):
                            rel_excl.append(j)
                            
                    else:
                        raise NotImplementedError
                        
                    j += 1
            i += 1
            
        for j in reversed(sorted(rel_excl)):
            del rel_list[iteration + j]
            
    return rel_list

def amb_desc(worldName, rel_list, iteration, lang="en_GB"):
    
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
        
        if iteration == 0:
            node1 = world.scene.nodes[rel_list[iteration][1]]
            amount1 = len(world.scene.nodebyname(node1.name))
            
            noun1 = add_noun_article(node1.name, amount1, lang)
            
            description = noun1 + " is " + description
    
    return rel_list, description

def gen_spatial_desc(worldName, nodeID, lang="en_GB", descType = "Simple"):
    
    #Retrieve the spatial relations and sort them by priority    
    rel_list = sorted(get_node_sr(worldName, nodeID))
    
    if len(rel_list) == 0:
        description = "No relations for Node %s" % nodeID
        return description
        
    if descType == "Simple":
        #Getting a simple one level description so only check the first relation
        rel_list, description = amb_desc(worldName, rel_list, 0, lang)
    else:
        raise NotImplementedError
    
    return description
    
if __name__ == "__main__":
    
    print("Finished")
