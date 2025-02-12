#! /usr/bin/env python

# Import Necessary Libraries
from geometry_msgs.msg import Twist
import rospy
import numpy as np
import math
import time
import os


# Define a Function to Calculate Direction of Motion
def calculate_direction(x1, y1, x2, y2):
    
    # Compute the Angle in Degrees and Return
    angle = math.atan2(y2 - y1, x2 - x1)
    angle = angle * 180 / math.pi
    return round(angle, 2)
 
 
# Define a Function to Calculate Distance of Motion
def calculate_distance(x1, y1, x2, y2):
    
    # Compute the Distance and Return
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return round(dist, 2)


# Define a Function to Goto a Location with given Linear velocity and Stop
def go_straight(linear_vel, dist_scale = 18):
        
    # Set the Linear Velocity and Publish Messages
    if linear_vel is not None:
        
        # Set the Linear velocity according to Distance value > 0 and Compute Duration
        if linear_vel > 0:
            move.linear.x = 0.1
        else:
            move.linear.x = -0.1
    duration = dist_scale * abs(linear_vel)
    print("Dist Duration", duration)
    
    # Start Timer
    start_time = time.time()
    
    # Until countdown reached
    while not rospy.is_shutdown() and (time.time() - start_time < duration):
        
        # Publish Messages
        pub.publish(move)
        rate.sleep()
    
    # Stop the Robot
    move.linear.x = 0
    pub.publish(move)
    rate.sleep()
    

# Define a Function to Turn with given Angular velocity and Stop
def turn(angle_deg, angle_scale = 8):
        
    # Set the Angular Velocity and Publish Messages
    if angle_deg is not None:
    	
    	# Set the Angular velocity according to Angle value > 180 and Compute Duration
    	if angle_deg < -180:
    	    angle_deg = 360 + angle_deg
    	if (angle_deg > 180 and angle_deg < 360) or (angle_deg < 0 and angle_deg > - 180):
    	    move.angular.z = -0.25
    	    if angle_deg > 180 and angle_deg < 360:
    	    	duration = abs(angle_deg - 360) / angle_scale
    	    else:
    	    	duration = -angle_deg / angle_scale
    	else:
    	    move.angular.z = 0.25
    	    duration = angle_deg / angle_scale
    print("Turn Duration", duration)
    # Start Timer
    start_time = time.time()
    
    # Until countdown reached
    while not rospy.is_shutdown() and (time.time() - start_time < duration):
        
        # Publish Messages
        pub.publish(move)
        rate.sleep()  
    
    # Stop the Robot
    move.angular.z = 0
    pub.publish(move)
    rate.sleep()


# Define a Function to Traverse Node Coordinates
def traverse(coordinates):

    # Save First Node as Current Position
    curr_pos_x, curr_pos_y = coordinates[0]
    curr_angle = 90

    # For every Coordinate
    for ind in range(1, len(coordinates)):
    
        # Get the Next Coordinates
        next_pos_x, next_pos_y = coordinates[ind]
    
        # Compute Distance vector and Angle Direction
        print(curr_pos_x, curr_pos_y, next_pos_x, next_pos_y)
        distance = calculate_distance(curr_pos_x, curr_pos_y, next_pos_x, next_pos_y)
        angle = calculate_direction(curr_pos_x, curr_pos_y, next_pos_x, next_pos_y)
        print("Distance", distance)
        print("Angle", curr_angle - angle)
    
        # Go straight to that Coordinates and Turn
        turn(curr_angle - angle)
        go_straight(distance)
    
        # Update Current Position and Angle
        curr_pos_x, curr_pos_y = coordinates[ind]
        curr_angle = angle
        time.sleep(0.5)
        print()



# Define a list to hold the coordinates
coordinates = []

# Open the Path file and Store Coordinates
with open('path.txt', 'r') as file:
    for line in file:
    
        # Split each line into parts
        parts = line.split()
        
        # Get the Coordinates
        coords = [float(parts[0]), float(parts[1])]
        
        # Append it into Coordinates list and Reverse Coordinates
        coordinates.append(coords)


# Initialize ROS node with Subscriber and Publisher
rospy.init_node('topic_publisher')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
rate = rospy.Rate(15)
move = Twist()

# Traverse the Nodes Coordinates
traverse(coordinates)
