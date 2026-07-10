from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    ip_arg = DeclareLaunchArgument('rtk_ip', default_value='10.10.10.10')
    port_arg = DeclareLaunchArgument('rtk_port', default_value='7507')

    ip_lc = LaunchConfiguration('rtk_ip')
    port_lc = LaunchConfiguration('rtk_port')

    node = Node(package='rtk_correction',
                executable='receiver',
                name='rtk_receiver',
                output='screen',
                emulate_tty=True,
                parameters=[{'rtk_ip': ip_lc, 'rtk_port': port_lc}])

    return LaunchDescription([ip_arg, port_arg, node])


