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
        self.rtk_ = False
        self.timer_ = rospy.Timer(rospy.Duration(2.0), self.statusCallback)
        rospy.Subscriber("/ublox/fix", NavSatFix, self.rtkCallback)

        print("[JACKAL-STATUS] Using topics: ", self.topics_)
            
        self.pub_ = rospy.Publisher("/status", JackalStatus, queue_size=1)
        print("[JACKAL-STATUS] Jackal Status Monitor Initialized")


    def find_key_by_value(self, dictionary: Dict, value : str):
        for key, val in dictionary.items():
            if val == value:
                return key
            return None

    def rtkCallback(self, msg : NavSatFix) -> None:
        if msg.position_covarinace[0] < 1.0 and msg.position_covariance[1] < 1.0:
            self.rtk_ = True
        else:
            self.rtk_ = False

    def statusCallback(self, event : TimerEvent) -> None:
        active_topics = rospy.get_published_topics()
        
        active_topic_list = [topic[0] for topic in active_topics]

        msg = JackalStatus()

        msg.rgb = False
        msg.jeti = False
        msg.thermal = False
        msg.ouster = False
        msg.gps = False
        msg.rtk = False
        msg.mic = False

        for topic in self.topics_:
            if topic in self.topics_:
                key = self.find_key_by_value(self.topics_, topic)
                if key == "rgb":
                    msg.rgb = True
                elif key == "thermal":
                    msg.thermal = True
                elif key == "gps":
                    msg.gps = True
                elif key == "mic":
                    msg.mic = True
                elif key == "controller":
                    msg.jeti = True
                elif key == "ouster":
                    msg.ouster = True

        msg.rtk = self.rtk_

        msg.header.stamp = rospy.Timer.now()
        msg.header.frame_id = "jackal"

        self.pub_.publish(msg)
