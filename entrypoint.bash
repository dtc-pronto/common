#!/bin/bash

HOSTNAME=$(hostname)
source /opt/ros/noetic/setup.bash
source ws/devel/setup.bash
if [ "$MOCHA" = true ]; then
    echo "[MOCHA] Launching MOCHA"
    case "$HOSTNAME" in phobos|deimos|titania|oberon)
	echo "Launching MOCHA for $HOSTNAME"
    	roslaunch mocha_launch jackal.launch robot_name:=$HOSTNAME --wait &
	;;
    *)
	roslaunch mocha_launch basestation.launch robot_name:=basestation --wait &
	;;
    esac
fi
if [ "$RTK" = true ]; then
    case "$HOSTNAME" in phobos|deimos|titania|oberon)
	echo "[RTK] Launching RTK for $HOSTNAME"
	roslaunch rtk_correction jackal.launch --wait &
	;;
    *)
	roslaunch rtk_correction broadcaster.launch --wait &
	;;
    esac
fi
