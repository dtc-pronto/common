#!/bin/bash

HOSTNAME=$(hostname)
source /opt/ros/jazzy/setup.bash
source ws/install/setup.bash
if [ "$MOCHA" = true ]; then
    if [ "$HOSTNAME" = "basestation" ]; then
        echo "[MOCHA] Launching MOCHA basestation"
        ros2 launch mocha_launch basestation.launch.py robot_name:="${HOSTNAME}" &
    else
        echo "[MOCHA] Launching MOCHA for ${HOSTNAME}"
        ros2 launch mocha_launch jackal.launch.py robot_name:="${HOSTNAME}" &
    fi
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
