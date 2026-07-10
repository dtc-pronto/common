#!/bin/bash

HOSTNAME=$(hostname)
source /opt/ros/jazzy/setup.bash
source ws/install/setup.bash
if [ "$MOCHA" = true ]; then
    echo "[MOCHA] MOCHA NOT READY YET"
fi
if [ "$RTK" = true ]; then
    case "$HOSTNAME" in phobos|deimos|titania|oberon)
	echo "[RTK] Launching RTK reciever for $HOSTNAME"
	ros2 launch rtk_correction receiver.launch.py rtk_ip:="${RTK_IP}" rtk_port:="${RTK_PORT}" &
	;;
    *)
        echo "[RTK] Launching RTK broadcaster"
	ros2 launch rtk_correction broadcaster.launch.py rtk_ip:="${RTK_IP}" rtk_port:="${RTK_PORT}" &
	;;
    esac
fi
wait
