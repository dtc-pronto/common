#!/bin/bash

xhost +

docker run --rm -it \
  --network=host \
  --privileged \
  --hostname `hostname` \
  -v "/tmp/.X11-unix:/tmp/.X11-unix" \
  -v "/dev:/dev" \
  --env-file ~/basestation/.env \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XAUTHORITY=$XAUTH \
  --name dtc-platform-`hostname`-common \
  dtc-platform-`hostname`:common \
  bash

xhost -

