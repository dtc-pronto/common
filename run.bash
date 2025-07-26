#!/bin/bash

xhost +
docker run -it --rm \
    --network=host \
    --privileged \
    -v "/dev:/dev" \
    -v "/tmp/.X11-unix:/tmp/.X11-unix" \
    -v "./dtc_msgs:/home/`whoami`/ws/src/dtc_msgs" \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=$XAUTH \
    --name dtc-common-test-container \
    dtc-common:test \
    bash
xhost -
