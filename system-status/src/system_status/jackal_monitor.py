"""
    Jason Hughes
    July 2025

    Monitor the topics on the jackal
"""

import rospy
from typing import Dict
from rospy.timer import TimerEvent
from dtc_msgs.msg import JackalStatus
from sensor_msgs.msg import NavSatFix, Imu, Image, Joy
from audio_common_msgs.msg import AudioData

class JackalMonitor:

    def __init__(self) -> None:
        self.topics_ = rospy.get_param("/jackal_status/jackal/topics")
        self.rtk_ = False
        self.gps_ = False
        self.rgb_ = False
        self.joy_ = False
        self.ir_ = False
        self.ouster_ = False

        self.gps_time_ = rospy.Time.now()
        self.mic_time_ = rospy.Time.now()
        self.joy_time_ = rospy.Time.now()
        self.cam_time_ = rospy.Time.now()
        self.ir_time_ = rospy.Time.now()
        self.ouster_time_ = rospy.Time.now()

        rospy.Subscriber("/ublox/fix", NavSatFix, self.rtkCallback)
        rospy.Subscriber("/boson/image_raw", Image, self.bosonCallback)
        rospy.Subscriber("/camera/image_color", Image, self.cameraCallback)
        rospy.Subscriber("/joy", Joy, self.joyCallback)
        rospy.Subscriber("/audio/audio", AudioData, self.audioCallback)
        rospy.Subscriber("/ouster/imu", Imu, self.ousterCallback)
        
        self.timer_ = rospy.Timer(rospy.Duration(2.0), self.statusCallback)
        print("[JACKAL-STATUS] Using topics: ", self.topics_)
            
        self.pub_ = rospy.Publisher("/sensor_status", JackalStatus, queue_size=1)
        print("[JACKAL-STATUS] Jackal Status Monitor Initialized")


    def find_key_by_value(self, dictionary: Dict, value : str):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    def rtkCallback(self, msg : NavSatFix) -> None:
        if msg.position_covarinace[0] < 0.2 and msg.position_covariance[1] < 0.2:
            self.rtk_ = True
        else:
            self.rtk_ = False
        self.gps_time_ = rospy.Time.now()
    
    def bosonCallback(self, msg : Image) -> None:
        self.ir_time_ = rospy.Time.now()

    def cameraCallback(self, msg : Image) -> None:
        self.cam_time_ = rospy.Time.now()

    def joyCallback(self, msg : Joy) -> None:
        self.joy_time_ = rospy.Time.now()

    def audioCallback(self, msg : AudioData) -> None:
        self.mic_time_ = rospy.Time.now()

    def ousterCallback(self, msg : Imu) -> None:
        self.ouster_time_ = rospy.Time.now()

    def statusCallback(self, event : TimerEvent) -> None:
        msg = JackalStatus()

        msg.rgb = False
        msg.jeti = False
        msg.thermal = False
        msg.ouster = False
        msg.gps = False
        msg.rtk = False
        msg.mic = False

        if rospy.Time.now() - self.gps_time_ < rospy.Duration(10.0):
            msg.gps = True
            msg.rtk = self.rtk_
        if rospy.Time.now() - self.ir_time_ < rospy.Duration(10.0):
            msg.thermal = True 
        if rospy.Time.now() - self.cam_time_ < rospy.Duration(10.0):
            msg.rgb = True
        if rospy.Time.now() - self.joy_time_ < rospy.Duration(10.0):
            msg.jeti = True
        if rospy.Time.now() - self.mic_time_ < rospy.Duration(10.0):
            msg.mic = True 
        if rospy.Time.now() - self.ouster_time_ < rospy.Duration(10.0):
            msg.ouster = True

        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "jackal"

        self.pub_.publish(msg)
