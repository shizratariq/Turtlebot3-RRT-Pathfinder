#!/bin/bash

# Open Terminal to Run Roscore
gnome-terminal -e "roscore"

# Open Terminal to SSH into Robot server
gnome-terminal -e "ssh ubuntu@192.168.1.151"

########################## Meanwhile Run these Commands Manually ######################
#roslaunch turtlebot3_bringup turtlebot3_robot.launch
sleep 60


# Open Terminal to Control Robot Movements using Teleop
gnome-terminal -e "roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch"
sleep 3

# Open Terminal to Perform Navigation and Mapping
gnome-terminal -e "roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml"
sleep 3

# Open Terminal to Run Manipulation Bringup Node
gnome-terminal -e "roslaunch turtlebot3_manipulation_bringup turtlebot3_manipulation_bringup.launch"
sleep 3

# Open Terminal to Start Planning
gnome-terminal -e "roslaunch turtlebot3_manipulation_moveit_config move_group.launch"
sleep 3

# Traverse the RRT Path
gnome-terminal -e "bash path.sh"