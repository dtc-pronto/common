"""
    Jason Hughes
    September 2025


"""
import yaml
import rospy
from dtc_msgs.msg import CasualtyFix, CasualtyFixArray

from spoofer.spoofer import Spoofer

class DroneSpoofer(Spoofer):

    def __init__(self) -> None:
        super().__init__()

        path = rospy.get_param("~robot_path")

        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

        rospy.Timer(rospy.Duration(self.config["rate"]), self.drone_callback)

        self.pub_ = rospy.Publisher("/casualty_info", CasualtyFixArray, queue_size=1)

        self.count_ = 0
        self.cas_ = self.config["casualties"]
        self.fix_arr_ = list()
        rospy.loginfo("[SPOOFER] Drone Node Initialized")
                
    def drone_callback(self, event) -> None:
        if self.count_ == len(self.coords_):
            rospy.loginfo("Recorded all targets")
            return
        rospy.loginfo("[SPOOFER] Spoofing drone") 
        # TODO add casualty to fix array
        msg = CasualtyFix()
        msg.casualty_id  = self.count_
        
        msg.location.latitude = self.coords_[self.cas_[self.count_]][0]
        msg.location.longitude = self.coords_[self.cas_[self.count_]][1]
        msg.time_ago = rospy.Time.now()
        msg.header.stamp = msg.time_ago

        self.fix_arr_.append(msg)
        arr_msg = CasualtyFixArray()
        arr_msg.casualties = arr_msg
        arr_msg.header.stamp = rospy.Time.now()

        self.pub_.publish(arr_msg)
        self.count_ += 1
