"""
    Jason Hughes
    July 2025 

    start the jackal node 
"""

import rospy
from system_status.jackal_monitor import JackalMonitor

if __name__ == "__main__":
    rospy.init_node("jackal_status")
    
    JackalMonitor()
    
    rospy.spin()

