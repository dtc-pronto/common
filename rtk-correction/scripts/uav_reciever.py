#!/usr/bin/env python3

# pyrtcm for parsing
# receive messsage with zmq subscriber
# zmq can decode the message (bytes)
# put it into an rtcm rosmsg
# publish this rtcm msg to the gps

import sys
import zmq
import rospy
from mavros_msgs.msg import RTCM
from rtcm_msgs.msg import Message

class Jackal:
    def __init__(self): 
        rospy.init_node('gps_corr_uav')
        
        ip = rospy.get_param("/rtk_reciever/ip")
        port = rospy.get_param("/rtk_reciever/port")

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{ip}:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")


        self.pub = rospy.Publisher('/mavros/gps_rtk/send_rtcm', RTCM, queue_size=1)

    def rtcm_pub_sub(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            try:
                rtcm_raw = self.socket.recv(flags=zmq.NOBLOCK)
                rospy.loginfo_once("[RTK] Recieved RTK correction")
                msg = RTCM()
                msg.header.stamp = rospy.Time.now()
                msg.data = rtcm_raw
                self.pub.publish(msg)
                print("Published to /rtcm . . . ") 

            except zmq.Again:
                continue
                #print("No RTCM reading available.")
                 
            rospy.sleep(0.1)

        finally:
            self.socket.close()
            self.context.term()




if __name__ == "__main__":
    Jackal().rtcm_pub_sub()
