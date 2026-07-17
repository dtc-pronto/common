#!/bin/bash

HOSTNAME=$(hostname)
source /opt/ros/jazzy/setup.bash
source ws/install/setup.bash
if [ "$MOCHA" = true ]; then
    # Read MOCHA Docker environment variables, providing default fallbacks if they aren't set
    WIFI_FALLBACK=${WIFI_FALLBACK:-"true"}
    WIFI_ALWAYS_ON=${WIFI_ALWAYS_ON:-"false"}
    WIFI_BACKUP_PERIOD=${WIFI_BACKUP_PERIOD:-"10.0"}
    RAJANT_TIMEOUT=${RAJANT_TIMEOUT:-"10.0"}
    ROBOT_CONFIGS=${ROBOT_CONFIGS:-"/home/dtc/config/robot_configs.yaml"}
    TOPIC_CONFIGS=${TOPIC_CONFIGS:-"/home/dtc/config/topic_configs.yaml"}
    RADIO_CONFIGS=${RADIO_CONFIGS:-"/home/dtc/config/radio_configs.yaml"}

    # Base launch arguments passed to the launch files
    MOCHA_ARGS="robot_name:=${HOSTNAME} wifi_fallback_enabled:=${WIFI_FALLBACK} wifi_backup_always_on:=${WIFI_ALWAYS_ON} wifi_backup_period:=${WIFI_BACKUP_PERIOD} rajant_signal_timeout:=${RAJANT_TIMEOUT} robot_configs:=${ROBOT_CONFIGS} topic_configs:=${TOPIC_CONFIGS} radio_configs:=${RADIO_CONFIGS}"

    if [ "$HOSTNAME" = "basestation" ]; then
        echo "[MOCHA] Launching MOCHA basestation"
        ros2 launch mocha_launch basestation.launch.py ${MOCHA_ARGS} &
    else
        echo "[MOCHA] Launching MOCHA for ${HOSTNAME}"
        ros2 launch mocha_launch jackal.launch.py ${MOCHA_ARGS} &
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
