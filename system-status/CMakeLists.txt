cmake_minimum_required(VERSION 3.0.2)
project(system_status)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  nav_msgs
  geometry_msgs
  std_msgs
  dtc_msgs
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS rospy sensor_msgs nav_msgs geometry_msgs std_msgs dtc_msgs
)

catkin_install_python(PROGRAMS
  scripts/jackal_node.py
  scripts/falcon_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
