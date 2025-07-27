# base station broadcaster
# pyrtcm for serial connection
# read gps on basestation with pyrtcm through serial connection
# pyrtcm reads the serial connection and gives me some bytes
# the bytes i multicast it with zmq

import serial
import zmq
import rospy
from pyrtcm import RTCMReader

class Basestation:
    def __init__(self):
        rospy.init_node("rtk_broadcaster")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        
        ip = rospy.get_param("/rtk_broadcaster/ip")
        port = rospy.get_param("/rtk_broadcaster/port")
        self.socket.bind(f"tcp://{ip}:{port}")

    def broadcast(self):
        with serial.Serial('/dev/ublox', 38400, timeout=3) as stream:
            rtr = RTCMReader(stream)
            rospy.loginfo_once("[RTK] Connected to GPS")
            while not rospy.is_shutdown():
                raw_data, parsed_data = rtr.read()
                #print(raw_data, parsed_data)
                if parsed_data is not None:
                    # Broadcast raw data
                    rospy.loginfo_once("[RTK] Broadcasting corrections")
                    self.socket.send(raw_data)


if __name__ == "__main__":
    basestation = Basestation()
    basestation.broadcast()
