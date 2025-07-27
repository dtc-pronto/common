"""
    Jason Hughes
    July 2025

    Monitor the topics on the jackal
"""

import rospy
from typing import Dict
from rospy.timer import TimerEvent
from dtc_msgs.msg import JackalStatus


class JackalMonitor:

    def __init__(self) -> None:
        self.topics_ = rospy.get_param("/jackal_status/jackal/topics")
        self.timer_ = rospy.Timer(rospy.Duration(2.0), self.statusCallback)

        print("[JACKAL-STATUS] Using topics: ", self.topics_)
            
        self.pub_ = rospy.Publisher("/status", JackalStatus, queue_size=1)
        print("[JACKAL-STATUS] Jackal Status Monitor Initialized")


    def find_key_by_value(self, dictionary: Dict, value : str):
        for key, val in dictionary.items():
            if val == value:
                return key
            return None

    def statusCallback(self, event : TimerEvent) -> None:
        active_topics = rospy.get_published_topics()
        
        active_topic_list = [topic[0] for topic in active_topics]

        msg = JackalStatus()

        for topic in self.topics_:
            if topic in self.topics_:
                key = self.find_key_by_value(self.topics_, topic)
                if key == "rgb":
                    msg.rgb = True
                elif key == "thermal":
                    msg.thermal = True
                elif key == "gps":
                    msg.gps = True
                elif key == "rtk":
                    msg.rtk = True    
                elif key == "radar":
                    msg.radar = True

        self.pub_.publish(msg)
