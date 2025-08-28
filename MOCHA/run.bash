#!/bin/bash

xhost +

docker run --rm -it \
  --network=host \
  --privileged \
  -v "/tmp/.X11-unix:/tmp/.X11-unix" \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XAUTHORITY=$XAUTH \
  --name dtc-jackal-`hostname`-mocha \
  dtc-jackal-`hostname`:mocha \
  bash

xhost -

