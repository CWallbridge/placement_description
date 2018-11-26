import os
import sys
import math
import rospy
import numpy
import geometry_msgs.msg
import enchant
import gc
import random

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
        
def get_negation(lang="en_GB"):
    
    if lang=="en_GB":
        negate = ["no", "nope"]
    else:
        raise NotImplementedError
        
    return random.choice(negate)
    
def get_conjunction(lang="en_GB"):
    
    if lang=="en_GB":
        return " and"
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

def sr_desc(ctx, worldName, rel_list, iteration, lang="en_GB", two_dim = False):
    
    if iteration >= len(rel_list):
        return rel_list, "", ""
    
    rel_list = check_for_exclusions(ctx, worldName, rel_list, iteration)
    
    world = ctx.worlds[worldName]
    
    node2 = world.scene.nodes[rel_list[iteration][2]]
    amount2 = len(world.scene.nodebyname(node2.name))
    
    noun2 = add_noun_article(node2.name, amount2, lang)
    
    sr_desc = get_desc_relation(rel_list[iteration][3], lang, two_dim)
    
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

def non_ambig_desc(ctx, worldName, rel_list, camera, adt_node_chks=[], lang="en_GB", sub_desc_type="placement", two_dim = False):

    world = ctx.worlds[worldName]
    desc_node = world.scene.nodes[rel_list[0][1]]
    
    if sub_desc_type == "locate":
        node_list = world.scene.nodebyname(desc_node.name) + adt_node_chks
    else:
        node_list = world.scene.nodebyname("empty space") + adt_node_chks
    
    if desc_node in node_list:
        node_list.remove(desc_node)
    
    #Ensure no duplicates
    node_list = list(set(node_list))
    
    i = 0
    
    description = ""
    
    node_skip = []
    
    while len(node_list) > len(node_skip) and i < len(rel_list):
    
        rel_list, desc, part1 = sr_desc(ctx, worldName, rel_list, i, lang, two_dim)
        add_desc = False
        
        for node2 in node_list:
            
            if node2 in node_skip:
                continue
            
            try:
                rel_list2 = node2.relList
            except AttributeError:
                rel_list2 = sorted(get_node_sr(ctx, worldName, node2.id, camera))
        
            rel_list2 = check_for_exclusions(ctx, worldName, rel_list2, i)
            node_desc = world.scene.nodes[rel_list[i][2]]
            node_desc2 = world.scene.nodes[rel_list2[i][2]]
            
            if rel_list[i][3] == rel_list2[i][3] and node_desc.name == node_desc2.name:
                node2.relList = rel_list2
            else:
                node_skip.append(node2)
                add_desc = True
        
        if add_desc == True:
            if len(node_list) <= len(node_skip) and i != 0:
                description += get_conjunction(lang) + " " + desc
            else:
                description += part1 + desc
            
        i += 1
        
        gc.collect()
        
    return description
    
def mnt_vector_list(vect_list, vector_sum, k, new_vector):
    
    vect_list.append(new_vector)
    vector_sum = vector_sum + new_vector
    
    if len(vect_list) > k:
        old_vector = vector_list.pop(0)
        vector_sum = vector_sum - old_vector
        
    vector_avg = vector_sum/k
    
    return vect_list, vector_sum, vector_avg
    
def calc_angle_between_vectors(vector1, vector2, vector1_mag, vector2_mag):
    
    unit_vector_1 = vector1/vector1_mag
    unit_vector_2 = vector2/vector2_mag
    angle = numpy.arccos(numpy.clip(numpy.dot(unit_vector_1, unit_vector_2), -1.0, 1.0))
    
    return angle
    
    
def calc_feedback(vector_avg, cur_pos, target_pos, min_dist, threshold_mag, threshold_angle, potential_target_positions, calc_type="magnitude"):

    target_vector = target_pos - cur_pos
    magnitude_targ = numpy.linalg.norm(target_vector)
    
    if magnitude_targ < min_dist:
        #If the current position is too close calculations chance for incorrect calculation based on overshoot, plus likely to be within success range
        return "no action"
        
    magnitude_cur = numpy.linalg.norm(vector_avg)
    
    if calc_type == "magnitude" or calc_type == "both":
        #Based on the magnitude of the vector_avg we decide if a target has been chosen and then try to compare
        
        if magnitude_cur < threshold_mag:
            #User is likely undecided, may need prompting
            return "elaborate"
        
    angle = calc_angle_between_vectors(target_vector, vector_avg, magnitude_targ, magnitude_cur)
    
    if angle <= threshold_angle:
        #User is on target
        return "no action"
    elif calc_type == "magnitude":
        #Doing no further calculation, they are heading in the wrong direction
        return "negate"
                
    if calc_type == "potential_target" or calc_type == "both":
        
        for pot_targ_pos in potential_target_positions:
            pot_target_vector = pot_target_pos - cur_pos
                
            magnitude_pot = numpy.linalg.norm(pot_target_vector)
            angle = calc_angle_between_vectors(pot_target_vector, vector_avg, magnitude_pot, magnitude_cur)
            
            if angle <= threshold_angle:
                #We believe user has chosen the wrong target
                return "negate"
        
        #User does not appear to have chosen a target, may need prompting.
        
        return "elaborate"
        
    
def dynamic_desc(ctx, worldName, rel_list, nodeID, iteration, fb_type, camera=None, lang="en_gb"):
    
    world = ctx.worlds[worldName]
    desc_node = world.scene.nodes[rel_list[0][1]]
    
    if fb_type == "initial":
        rel_list, description, part1 = sr_desc(ctx, worldName, rel_list, 0, lang)
        description = part1 + description
        iteration = 1
    elif fb_type == "elaborate":
        rel_list, description, part1 = sr_desc(ctx, worldName, rel_list, iteration, lang)
        iteration += 1
    elif fb_type == "negate":
        description = get_negation(lang)
    else:
        #no action
        description = ""
    
    return description, rel_list, iteration
    

def gen_spatial_desc(ctx, worldName, nodeID, camera=None, add_node_chks=[], lang="en_GB", descType = "Simple", sub_desc_type = "placement", two_dim = False):
    
    #Retrieve the spatial relations and sort them by priority
    rel_list = sorted(get_node_sr(ctx, worldName, nodeID, camera))
    
    if len(rel_list) == 0:
        description = "No relations for Node %s" % nodeID
        return description
        
    if descType == "Simple":
        #Getting a simple one level description so only check the first relation
        rel_list, description, part1 = sr_desc(ctx, worldName, rel_list, 0, lang)
        description = part1 + description
    elif descType == "NonAmbig":
        description = non_ambig_desc(ctx, worldName, rel_list, camera, add_node_chks, lang, sub_desc_type, two_dim)
    else:
        raise NotImplementedError

    return description
    
if __name__ == "__main__":
    
    print("Finished")
