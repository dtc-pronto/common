"""
    Jason Hughes
    September 2025

    spoofer node for the jackal
"""
import cv2
import json
import yaml
import rospy
import numpy as np
from dtc_msgs.msg import ScoreCardString
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

from spoofer.spoofer import Spoofer

from typing import Dict

def initReport() -> Dict:
    return {
      "hr": {
        "value": 0,
        "time_ago": rospy.Time.now().to_sec()
      },
      "rr": {
        "value": 0,
        "time_ago": rospy.Time.now().to_sec()
      },
      "alertness_ocular": {
        "value": 0,
        "time_ago":  rospy.Time.now().to_sec()
      },
      "alertness_verbal": {
        "value": 0,
        "time_ago":  rospy.Time.now().to_sec()
      },
      "alertness_motor": {
        "value": 0,
        "time_ago":  rospy.Time.now().to_sec()
      },
      "severe_hemorrhage": {
        "value": 0,
        "time_ago":  rospy.Time.now().to_sec()
      },
      "respiratory_distress": {
        "value": 0,
        "time_ago":  rospy.Time.now().to_sec()
      },
      "trauma_head": 0,
      "trauma_torso": 0,
      "trauma_lower_ext": 0,
      "trauma_upper_ext": 0,
      "temp": {
        "value": 98,
        "time_ago":  rospy.Time.now().to_sec()
      },
      "casualty_id": 2,
      "team": "PennPronto",
      "system": "JackalNVILA",
      "location": {
        "latitude": 0.0,
        "longitude": 0.0,
        "time_ago":  rospy.Time.now().to_sec()
      }}


class JackalSpoofer(Spoofer):

    def __init__(self) -> None:
        super().__init__()

        path = rospy.get_param("/spoofer_node/robot_path")

        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

        rospy.Timer(rospy.Duration(self.config["rate"]), self.jackal_callback)

        self.pub_ = rospy.Publisher("/report_status", ScoreCardString, queue_size=1)

        self.count_ = 0
        self.cas_ = self.config["casualties"]
        rospy.loginfo("[SPOOFER] Jackal Spoofer Initialized")
        
    def create_compressed_image_msg(self, image : np.ndarray ) -> CompressedImage:
        compressed_img = CompressedImage()
        compressed_img.header.stamp = rospy.Time.now()
        compressed_img.header.frame_id = "camera_frame"
        
        # Set format
        compressed_img.format = 'jpg'
        
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 90]
        _, compressed_data = cv2.imencode('.jpg', image, encode_params)
        
        compressed_img.data = compressed_data.tobytes()
        
        return compressed_img

    def jackal_callback(self, event) -> None:
        if self.count_ == len(self.cas_):
            rospy.loginfo("Recorded all targets")
            return
        rospy.loginfo("[SPOOFER] Spoofing scorecard")
        coord = self.coords_[self.cas_[self.count_]]

        msg = ScoreCardString()
        string = initReport()
        string["latitude"] = coord[0]
        string["longitude"] = coord[1]
        
        msg.scorecard = json.dumps(string)
        image = np.random.randint(0, 256, (480, 480, 3), dtype=np.uint8)
        msg.image = self.create_compressed_image_msg(image)

        self.pub_.publish(msg)
        self.count_ += 1
