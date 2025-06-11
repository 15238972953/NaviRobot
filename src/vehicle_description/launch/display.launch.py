import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, PathJoinSubstitution

def generate_launch_description():
    pkg_path = get_package_share_directory('vehicle_description')
    xacro_file = os.path.join(pkg_path, 'urdf', 'car_with_sensors.xacro')

    robot_description = Command(['xacro ', xacro_file])

    return LaunchDescription([
        # 启动 Gazebo 仿真环境
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'),
            ])
        ),

        # 启动 robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description
            }]
        ),

        # 加载机器人到 Gazebo 中
        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
                '-topic', 'robot_description',
                '-entity', 'car_with_sensors',
                '-x', '0', '-y', '0', '-z', '0.1'
            ],
            output='screen'
        )
    ])
