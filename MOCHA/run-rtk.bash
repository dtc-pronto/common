#!/bin/bash

xhost +

docker run --rm -it \
  --network=host \
  --privileged \
  -v "/tmp/.X11-unix:/tmp/.X11-unix" \
  -v "/home/dtc/Jackal/common/dtc_msgs:/home/dtc/ws/src/dtc_msgs" \
  -v "/home/dtc/Jackal/common/rtk-correction:/home/dtc/ws/src/rtk-correction" \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XAUTHORITY=$XAUTH \
  --name dtc-jackal-`hostname`-rtk \
  dtc-jackal-`hostname`:mocha \
  bash

xhost -

