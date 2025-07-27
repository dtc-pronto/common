"""
    Jason Hughes
    July 2025 

    start the jackal node 
"""

import rospy
from system_status.falcon_monitor import FalconMonitor

if __name__ == "__main__":
    rospy.init_node("falcon_status")
    
    FalconMonitor()
    
    rospy.spin()

