"""
    Jason Hughes
    September 2025

"""

import rospy

from spoofer.drone import DroneSpoofer
from spoofer.jackal import JackalSpoofer

if __name__ == "__main__":
    rospy.init_node("spoofer_node")

    robot = rospy.get_param("/robot")

    if robot == "jackal": 
        JackalSpoofer()
    if robot == "drone":
        DroneSpoofer()

    rospy.spin()

