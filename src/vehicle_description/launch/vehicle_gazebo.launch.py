from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    pkg_share = get_package_share_directory('vehicle_description')

    # 参数定义
    vehicle_model = LaunchConfiguration('vehicle_model')
    sensor_model = LaunchConfiguration('sensor_model')

    xacro_file = os.path.join(pkg_share, 'urdf', 'vehicle_with_sensors.xacro')

    return LaunchDescription([
        # 声明传入参数
        DeclareLaunchArgument('vehicle_model', default_value='vehicle'),
        DeclareLaunchArgument('sensor_model', default_value='sensor'),

        # 启动 Gazebo 环境
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),

        # 发布 robot_state（xacro生成）
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command([
                    'xacro ', xacro_file,
                    ' vehicle_model:=', vehicle_model,
                    ' sensor_model:=', sensor_model
                ])
            }]
        ),

        # joint_state 发布器（可选 GUI 版）
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),

        # 向 Gazebo 中加入机器人实体
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'my_vehicle',
                '-x', '0', '-y', '0', '-z', '0.1'
            ],
            output='screen'
        ),
    ])
