#!/usr/bin/env python
import rospy
from champ_msgs.msg import Joints
from sensor_msgs.msg import JointState
import rosparam
import os, sys

class JointsRelay:
    def __init__(self):
        rospy.Subscriber("/champ/joint_states/raw", Joints, self.joint_states_callback)
        rospy.Subscriber("/champ/joint_states/gui", JointState, self.joint_states_gui_callback)

        self.joint_states_pub = rospy.Publisher('/champ/joint_states', JointState, queue_size = 100)
        self.joint_states_calibrate_pub = rospy.Publisher('/champ/joint_states/calibrate', Joints, queue_size = 100)

        self.joint_names = []
        
        leg_map = [None,None,None,None]
        leg_map[3] = rospy.get_param('/joints_relay/left_front')
        leg_map[2] = rospy.get_param('/joints_relay/right_front')
        leg_map[1] = rospy.get_param('/joints_relay/left_hind')
        leg_map[0] = rospy.get_param('/joints_relay/right_hind')

        for leg in reversed(leg_map):
            for joint in leg:
                self.joint_names.append(joint) 

    def joint_states_callback(self, joints):
        joint_states = JointState()
        joint_states.header.stamp = rospy.Time.now()
        joint_states.name = self.joint_names

        joint_states.position = joints.position
        self.joint_states_pub.publish(joint_states)


    def joint_states_gui_callback(self, joints):
        joint_states_calibrate = Joints()
        
        for i in range(12):
            joint_states_calibrate.position.append(joints.position[i])

        self.joint_states_calibrate_pub.publish(joint_states_calibrate)

if __name__ == "__main__":
    rospy.init_node('champ_joints_relay', anonymous=True)
    j = JointsRelay()
    rospy.spin()


    