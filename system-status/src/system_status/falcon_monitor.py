"""
    Jason Hughes
    July 2025

    Monitor the topics on the jackal
"""

import rospy
from typing import Dict
from rospy.timer import TimerEvent
from dtc_msgs.msg import FalconStatus
from sensor_msgs.msg import Image, NavSatFix

class FalconMonitor:

    def __init__(self) -> None:
        self.topics_ = rospy.get_param("/falcon_status/falcon/topics")
    
        self.rtk_ = False
        self.cam_time_ = rospy.Time.now()
        self.ir_time_ = rospy.Time.now()
        self.gps_time_ = rospy.Time.now()    
    
        rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, self.rtkCallback)
        rospy.Subscriber("/boson/image_raw", Image, self.bosonCallback)
        rospy.Subscriber("/camera/image_color", Image, self.cameraCallback)
    
        self.timer_ = rospy.Timer(rospy.Duration(2.0), self.statusCallback)

        print("[FALCON-STATUS] Using topics: ", self.topics_)

        self.pub_ = rospy.Publisher("/sensor_status", FalconStatus, queue_size=1)
        print("[FALCON-STATUS] Falcon Status Monitor Initialized")

    def rtkCallback(self, msg : NavSatFix) -> None:
        if msg.position_covariance[0] < 0.2 and msg.position_covariance[1] < 0.2:
            self.rtk_ = True
        else:
            self.rtk_ = False
        self.gps_time_ = rospy.Time.now()
    
    def bosonCallback(self, msg : Image) -> None:
        self.ir_time_ = rospy.Time.now()

    def cameraCallback(self, msg : Image) -> None:
        self.cam_time_ = rospy.Time.now()

    def statusCallback(self, event : TimerEvent) -> None:
        msg = FalconStatus()

        msg.rgb = False
        msg.thermal = False
        msg.rtk = False
        msg.gps = False

        if rospy.Time.now() - self.gps_time_ < rospy.Duration(10.0):
            msg.gps = True
            msg.rtk = self.rtk_
        if rospy.Time.now() - self.ir_time_ < rospy.Duration(10.0):
            msg.thermal = True 
        if rospy.Time.now() - self.cam_time_ < rospy.Duration(10.0):
            msg.rgb = True

        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "falcon"

        self.pub_.publish(msg)
