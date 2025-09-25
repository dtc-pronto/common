"""
    Jason Hughes
    September 2025

    spoof casualty fix array
"""

import numpy as np
import rospy 

from spoofer.load import load_kml

from dtc_msgs.msg import CasualtyFix, CasualtyFixArray


class Spoofer:

    def __init__(self) -> None:

        path = rospy.get_param("~kml_path")
        self.coords_ = load_kml(path)
