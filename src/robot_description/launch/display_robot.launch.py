import os
import launch
import launch_ros
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, PathJoinSubstitution

def generate_launch_description():
    # 获取 robot_description 包的路径
    pkg_path = get_package_share_directory('robot_description')
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf')
    rviz_config_path = os.path.join(pkg_path, 'config', 'display_robot_model.rviz')

    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        'model',
        default_value=str(urdf_file),
        description='Path to the mode configuration file'
    )

    # 通过文件路径，获取内容，并转换成参数值对象，以供传入 robot_state_publisher
    substitutions_command_result = launch.substitutions.Command(['xacro ',launch.substitutions.LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result,
        value_type=str
    )

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        # name='robot_state_publisher',
        # output='screen',
        parameters=[{'robot_description': robot_description_value}]
    )

    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    # 启动 RViz2 可视化工具
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path],
    )

    # robot_description = Command(['urdf ', urdf_file])

    return LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node,

        # 启动 Gazebo 仿真环境
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([
        #         os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'),
        #     ])
        # ),


        # # 加载机器人到 Gazebo 中
        # ExecuteProcess(
        #     cmd=[
        #         'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
        #         '-topic', 'robot_description',
        #         '-entity', 'robot',
        #         '-x', '0', '-y', '0', '-z', '0.1'
        #     ],
        #     output='screen'
        # )
    ])