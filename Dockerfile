FROM dtcpronto/ros-jazzy:full

RUN sudo apt update \
 && sudo apt-get install -y python3-pip

#RUN pip3 install rospkg defusedxml
RUN sudo apt install -y \
 python3-zmq \
 default-jre \
 iputils-ping \
 python3-lz4 \
 python3-defusedxml \
 python3-serial
RUN pip3 install --break-system-packages pyrtcm

WORKDIR /home/dtc
RUN mkdir -p ws/src
RUN cd ws/src && mkdir MOCHA
RUN cd ws/src && git clone https://github.com/tilk/rtcm_msgs -b ros2_test

COPY rtk-correction ws/src/rtk-correction

COPY ./entrypoint.bash entrypoint.bash
RUN sudo chmod +x entrypoint.bash

ENV MOCHA=false
ENV RTK=false

RUN /bin/bash -c "\
    source /opt/ros/jazzy/setup.bash && \
    cd /home/dtc/ws && \
    colcon build --cmake-clean-cache"
