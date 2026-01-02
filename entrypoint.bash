#!/bin/bash

HOSTNAME=$(hostname)
source /opt/ros/jazzy/setup.bash
source ws/install/setup.bash
if [ "$MOCHA" = true ]; then
    echo "[MOCHA] MOCHA NOT READY YET"
fi
if [ "$RTK" = true ]; then
    case "$HOSTNAME" in phobos|deimos|titania|oberon)
	echo "[RTK] Launching RTK for $HOSTNAME"
	ros2 launch rtk_correction receiver.launch.py ip:="${BROADCASTER_IP}" port:="${BROADCASTER_PORT}" &
	;;
    *)
	ros2 launch rtk_correction broadcaster.launch.py ip:="${BROADCASTER_IP}" port:="${BROADCASTER_PORT}" &
	;;
    esac
fi
wait
