#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class VelocityPublisher:
    def _init_(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def publish(self, linear_x, angular_z):
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        self.pub.publish(twist)

class VelocitySubscriber:
    def _init_(self):
        self.sub = rospy.Subscriber('/cmd_vel', Twist, self.callback)

    def callback(self, data):
        print('Received velocity command: linear_x = {}, angular_z = {}'.format(data.linear.x, data.angular.z))

if __name__ == '__main__':
    rospy.init_node('velocity_publisher_subscriber')

    publisher = VelocityPublisher()
    subscriber = VelocitySubscriber()

    # Publish a velocity command
    publisher.publish(1.0, 0.0)

    # Wait for a velocity command to be received
    rospy.spin()
