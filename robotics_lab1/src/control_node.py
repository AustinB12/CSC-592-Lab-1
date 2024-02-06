#!/usr/bin/env python3

# import ROS for developing the node
import rospy

# import geometry_msgs/Twist for control commands
from geometry_msgs.msg import Twist

# we are going to read turtlesim/Pose messages this time
from turtlesim.msg import Pose

from robotics_lab1.msg import Turtlecontrol

# Instantiate the Turtlecontrol message
control_msg = Turtlecontrol()

# Instantiate the pose message
pos_msg = Pose()

def pose_callback(data):
	global pos_msg

	# Take in the x position; xt
	pos_msg.x = data.x

def control_callback(data):
	global control_msg
	
	# Set gain and desired X
	control_msg.kp = data.kp
	control_msg.xd = data.xd

if __name__ == "__main__":
	
	# Add a subscriber that reads in position information
	pose_sub = rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
	
	# Add a subscriber to listen to the topic we just made
	control_params_sub = rospy.Subscriber("/turtle1/control_params", Turtlecontrol, control_callback)

	# Add a publisher for updating velocity
	velocity_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
	
	# Initialize the node
	rospy.init_node('control_node', anonymous = True)
	
	# set a 10Hz frequency for this loop
	loop_rate = rospy.Rate(10)
	
	# Declare a variable of type Twist for sending control commands
	vel_cmd = Twist()
	
	while not rospy.is_shutdown():
		# Calculate new velocity
		velo = control_msg.kp * (control_msg.xd - pos_msg.x)
		
		# Set the velocity
		vel_cmd.linear.x = velo
		
		# publish the message
		velocity_pub.publish(vel_cmd)
		
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
