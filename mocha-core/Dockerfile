FROM osrf/ros:noetic-desktop

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 vim \
 tmux \
 cmake \
 gcc \
 g++ \
 git \
 build-essential \
 sudo \
 wget \
 curl \
 zip \
 unzip

ARG user_id
ARG USER dtc
RUN useradd -U --uid ${user_id} -ms /bin/bash $USER \
 && echo "$USER:$USER" | chpasswd \
 && adduser $USER sudo \
 && echo "$USER ALL=NOPASSWD: ALL" >> /etc/sudoers.d/$USER

USER $USER
WORKDIR /home/$USER

RUN sudo apt update \
 && sudo apt-get install -y python3-pip

RUN pip3 install rospkg defusedxml
RUN sudo apt install -y python3-zmq python3-catkin-tools default-jre iputils-ping
RUN pip3 install lz4

RUN sudo apt-get install -y ros-noetic-vision-msgs

RUN mkdir -p ws/src
RUN cd ws/src && mkdir MOCHA

COPY MOCHA/ ws/src/MOCHA/
#RUN mkdir -p ws/src
#RUN cd ws/src && mkdir MOCHA

#COPY MOCHA/ ws/src/MOCHA/


RUN cd ws \
 && catkin config --extend /opt/ros/noetic \
 && catkin build --no-status

RUN sudo chown $USER:$USER ~/.bashrc \
 && /bin/sh -c 'echo ". /opt/ros/noetic/setup.bash" >> ~/.bashrc' \
 && /bin/sh -c 'echo "source ~/ws/devel/setup.bash" >> ~/.bashrc' \
 && echo 'export PS1="\[$(tput setaf 2; tput bold)\]\u\[$(tput setaf 7)\]@\[$(tput setaf 3)\]\h\[$(tput setaf 7)\]:\[$(tput setaf 4)\]\W\[$(tput setaf 7)\]$ \[$(tput sgr0)\]"' >> ~/.bashrc
