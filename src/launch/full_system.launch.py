# 工程总启动文件

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 启动Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [FindPackageShare('gazebo_world'), '/launch/gazebo.launch.py']
            )
        ),
        # 相机/雷达驱动
        Node(package='camera_sim', executable='camera_node'),
        Node(package='lidar_sim', executable='lidar_node'),
        Node(package='radar_sim', executable='radar_node'),
        # 感知子系统
        Node(package='perception', executable='yolo_inference_node'),
        Node(package='perception', executable='fusion_node'),
        Node(package='perception', executable='bev_node'),
        Node(package='perception', executable='tracking_node'),
    ])
