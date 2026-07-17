FROM dtcpronto/ros-jazzy:full

RUN sudo apt update \
    && sudo apt-get install -y \
    python3-pip \
    python3-zmq \
    default-jre \
    iputils-ping \
    python3-lz4 \
    python3-defusedxml \
    python3-serial \
    ros-jazzy-smach \
    ros-jazzy-smach-ros \
    ros-jazzy-nav-msgs
RUN pip3 install --break-system-packages pyrtcm

WORKDIR /home/dtc
RUN mkdir -p ws/src
RUN cd ws/src && git clone https://github.com/tilk/rtcm_msgs -b ros2_test
RUN cd ws/src && git clone https://github.com/dtc-pronto/dtc-msgs.git

COPY rtk-correction ws/src/rtk-correction
COPY MOCHA ws/src/MOCHA
COPY config config

COPY ./entrypoint.bash entrypoint.bash
RUN sudo chmod +x entrypoint.bash

ENV MOCHA=false
ENV RTK=true
ENV BROADCASTER_IP=127.0.0.1
ENV BROADCASTER_PORT=7505

# Force ROS 2 to stay strictly on localhost and use FastRTPS (which natively supports daemon-less local discovery).
# This guarantees ROS 2 topics won't leak across the radio mesh and bypass MOCHA's synchronization.
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ENV ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST

RUN /bin/bash -c "\
    source /opt/ros/jazzy/setup.bash && \
    cd /home/dtc/ws && \
    colcon build --cmake-clean-cache"

RUN echo "source /home/dtc/ws/install/setup.bash" >> ~/.bashrc
