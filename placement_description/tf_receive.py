#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import math
import rospy
import tf
import geometry_msgs.msg

import logging; logger = logging.getLogger("placement_description.tf_receive")
logging.basicConfig(level=logging.INFO)

def tfReceiver(source='/world'):
	
	listener = tf.TransformListener()

	while not rospy.is_shutdown():
		try:
			for frame in listener.getFrameStrings:
				(trans,rot) = listener.lookupTransform(frame, source, rospy.Time(0))
		except(tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue

if __name__ == "__main__":
    
    tfReceiver()
    print("Finished")
