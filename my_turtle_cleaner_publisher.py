#!/usr/bin/env python
import queue

import rosdep2
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

x=0
y=0
theta=0

def callback_function(my_pose_message):
    global x
    global y
    global theta
    x=my_pose_message.x
    y=my_pose_message.y
    theta=my_pose_message.theta


def move(speed, distance_to_be_moved, is_forward):
    pub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    # rospy.init_node('my_turtle_cleaner', anonymous=True)
    rate=rospy.Rate(10)
    distance_moved=0
    x_0=x
    y_0=y
    my_message=Twist()
    if (is_forward==True):
        my_message.linear.x=speed
    else:
        my_message.linear.x=-speed
    while (distance_moved<distance_to_be_moved):
        pub.publish(my_message)
        distance_moved=math.sqrt((x-x_0)**2+(y-y_0)**2)
        rospy.loginfo(distance_moved)
        rospy.loginfo("Moving forward")
        rate.sleep()
    my_message.linear.x=0
    pub.publish(my_message)
    rospy.loginfo("Goal Reached")

def rotate(angular_speed_degree,angle_to_be_moved_degree,is_clockwise):
    pub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate=rospy.Rate(10) 
    my_message=Twist()
    angular_speed_radians=math.radians(angular_speed_degree)
    angle_covered_degree=0
    t_0=rospy.Time.now().to_sec()
    if (is_clockwise==True):
        my_message.angular.z=-angular_speed_radians
    else:
        my_message.angular.z=angular_speed_radians
    while (angle_covered_degree<angle_to_be_moved_degree):
        pub.publish(my_message)
        t_1=rospy.Time.now().to_sec()
        angle_covered_degree=(t_1-t_0)*angular_speed_degree
        rospy.loginfo(angle_covered_degree)
        rospy.loginfo("Rotating")
        rate.sleep()
    my_message.angular.z=0
    pub.publish(my_message)
    rospy.loginfo("Goal Reached!!")

def go_to_goal(final_pos_x,final_pos_y):
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rate=rospy.Rate(10)
    my_message=Twist()
    distance_to_be_covered=10
    while (distance_to_be_covered>0.01):
        linear_constant=0.5
        distance_to_be_covered=math.sqrt((final_pos_x-x)**2+(final_pos_y-y)**2)
        linear_speed=distance_to_be_covered*linear_constant
        print('current_x:',x,'current_y:',y,'distance_to_be_covered:',distance_to_be_covered)
        angular_constant=4.0
        angle_to_be_rotated_for_goal=math.atan2(final_pos_y-y, final_pos_x-x)
        angular_speed=(angle_to_be_rotated_for_goal-theta)*angular_constant
        my_message.linear.x=linear_speed
        my_message.angular.z=angular_speed
        pub.publish(my_message)
        rate.sleep()
    my_message.linear.x=0
    my_message.angular.z=0
    pub.publish(my_message)

def spiral_motion(linear_velocity, angular_velocity):
    pub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate=rospy.Rate(1)
    my_message=Twist()
    while (x<10.5 and y<10.5):
        my_message.linear.x=linear_velocity
        my_message.linear.y=0
        my_message.linear.z=0
        my_message.angular.x=0
        my_message.angular.y=0
        my_message.angular.z=angular_velocity
        pub.publish(my_message)
        linear_velocity=linear_velocity+0.5
        rate.sleep()
    my_message.linear.x=0
    my_message.angular.z=0
    pub.publish(my_message)

def grid_clean():
    desired_pose=Pose()
    desired_pose.x=1
    desired_pose.y=1
    desired_pose.theta=0
    go_to_goal(1.0,1.0)
    rotate(30,143,False)
    rospy.loginfo("---Scanning Started---")
    for i in range(5):
    	move(2.0,1.0,True)
    	rotate(20,90,False)
    	move(2.0,9.0,True)
    	rotate(20,90,True)
    	move(2.0,1.0,True)
    	rotate(20,90,True)
    	move(2.0,9.0,True)
    	rotate(20,90,False)
    rospy.loginfo("---Scanning Completed---")

if __name__=='__main__':
    try:
        rospy.Subscriber('/turtle1/pose', Pose, callback_function)
        rospy.init_node('my_turtle_cleaner', anonymous=True)
        # move(1.0,10.0,True)
        # rotate(30,90,True)
        # go_to_goal(10.5,10.5)
        # spiral_motion(0.0,2.0)
        grid_clean()
    except rospy.ROSInterruptException:
        pass
