"""
    Jason Hughes
    July 2025 

    This function is used to parse the custom 
    ScoreCard.msg from dtc_msgs
"""

from typing import Dict
from dtc_msgs.msg import ScoreCard
from std_msgs.msg import Time

class ScoreCardParser:

    def __init__(self) -> None:
        pass

    def rostime_to_darpatime(self, msg : Time) -> None:
        # TODO
        pass

    @staticmethod
    def parse_to_dict(msg : ScoreCard) -> Dict:
        data = {
            "casualty_id": msg.casualty_id,  
            "team": "PennPronto",  
            "system": "string",  
            "location": {
                "latitude": msg.location.location.latitude,
                "longitude": msg.location.location.longitude,
                "time_ago": ""  
            },
            "hr": {
                "value": msg.heart_rate.rate,
                "time_ago": ""  
            },
            "rr": {
                "value": msg.respiratory_rate.rate,
                "time_ago": ""  
            },
            "alertness_ocular": {
                "value": msg.alertness_ocular.value,
                "time_ago": ""  
            },
            "alertness_verbal": {
                "value": msg.alterness_verbal.value,  
                "time_ago": ""  
            },
            "alertness_motor": {
                "value": msg.alterness_motor.value,  
                "time_ago": ""  
            },
            "severe_hemorrhage": int(msg.severe_hemorrhage.value),  
            "respiratory_distress": int(msg.respiratory_distress.value),  
            "trauma_head": msg.trauma_head.value,
            "trauma_torso": msg.trauma_torso.value,
            "trauma_lower_ext": msg.trauma_lower_extremity.value,
            "trauma_upper_ext": msg.trauma_upper_extremity.value,
            
        }
        return data
