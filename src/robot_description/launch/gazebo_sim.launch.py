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
    xacro_file = os.path.join(pkg_path, 'urdf', 'NaviRobot/NaviRobot.urdf.xacro')
    # rviz_config_path = os.path.join(pkg_path, 'config', 'display_robot_model.rviz')
    gazebo_world_path = os.path.join(pkg_path, 'gazebo_world', 'myroom.world')

    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        'model',
        default_value=str(xacro_file),
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

    # 通过 IncludeLaunchDescription 包含另外一个 launch 文件
    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'gazebo_ros'), '/launch', '/gazebo.launch.py']),
      	# 传递参数
        launch_arguments=[('world', gazebo_world_path),('verbose','true')]
    )

    # 请求 Gazebo 加载机器人
    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description',
                   '-entity', 'NaviRobot', ]
    )

    # 加载并激活 NaviRobot_joint_state_broadcaster 控制器
    load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'NaviRobot_joint_state_broadcaster'],
        output='screen'
    )

    return LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        launch_gazebo,
        spawn_entity_node,
        # 事件动作，当加载机器人结束后执行    
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=spawn_entity_node,
                on_exit=[load_joint_state_controller],)
        ),
    ])