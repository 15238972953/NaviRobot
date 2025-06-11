import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 设置你的包名
    pkg_name = 'vehicle_description'  # ← 修改为你自己的包名
    urdf_filename = 'car.urdf'       # ← 修改为你自己的 URDF 文件名

    # 绝对路径
    urdf_path = os.path.join(
        get_package_share_directory(pkg_name),
        'urdf',
        urdf_filename
    )

    # 读取 URDF 文件内容
    with open(urdf_path, 'r') as infp:
        robot_description_content = infp.read()

    # 启动 Gazebo（空世界）
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ])
    )

    # 启动 robot_state_publisher，发布 TF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_content
        }]
    )

    # 把机器人实体 spawn 到 Gazebo 中
    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
            '-topic', 'robot_description',
            '-entity', 'my_robot',
            '-x', '0', '-y', '0', '-z', '0.2',
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity
    ])
