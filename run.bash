#!/bin/bash

xhost +

docker run --rm -it \
  --network=host \
  --privileged \
  -v "/tmp/.X11-unix:/tmp/.X11-unix" \
  -v "./config:/home/`whoami`/ws/src/MOCHA/mocha_core/config" \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XAUTHORITY=$XAUTH \
  --name dtc-platform-`hostname`-common \
  dtc-platform-`hostname`:common \
  bash

xhost -

