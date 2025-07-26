# DTC Msgs

This repo should contain any custom message types used for the DTC project. This will make `MOCHA` configuration significantly easier. 

## Message Definitions

### ScoreCard
This uses the exact layout of the scorecard from DARPA
```
std_msgs/Header header

sensor_msgs/NavSatFix location

bool severe_hemorrhage
bool respiratory_distress

float64 heart_rate
float64 respiratory_rate

# 0 => Normal, 1 => Wound, 2 => Not Testable (NT)
uint8 trauma_head
# 0 => Normal, 1 => Wound, 2 => Not Testable (NT)
uint8 trauma_torso
# 0 => Normal, 1 => Wound, 2 => Not Testable (NT) 3 => Amputation
uint8 trauma_upper_extremity
# 0 => Normal, 1 => Wound, 2 => Not Testable (NT) 3 => Amputation
uint8 trauma_lower_extremity

# 0 => Open, 1 => Closed, 2 => NT
uint8 alertness_ocular
# 0 => Normal, 1 => Abnormal, 2 => Absent, 3 => NT
uint8 alterness_verbal
# 0 => Normal, 1 => Abnormal, 2 => Absent, 3 => NT
uint8 alterness_motor
```
### NavSatFixArray
```
std_msgs/Header header
sensor_msgs/NavSatFix[] coordinates
```
### RespirationRate
```
std_msgs/Header header
std_msgs/UInt64 casualty_id
std_msgs/Float64 rate
```
### HeartRate
```
std_msgs/Header header
std_msgs/UInt64 casualty_id
std_msgs/Float64 rate
```

### GroundDetection
```
std_msgs/Header header

sensor_msgs/NavSatFix gps

std_msgs/UInt64 casualty_id

std_msgs/String whisper

dtc_msgs/RespirationRate acconeer
dtc_msgs/RespirationRate mtts_resp

dtc_msgs/HeartRate mtts_hr
```
### GroundImage
```
std_msgs/Header header

sensor_msgs/NavSatFix gps

sensor_msgs/CompressedImage image1
sensor_msgs/CompressedImage image2
sensor_msgs/CompressedImage image3

std_msgs/UInt64 casualty_id
```
