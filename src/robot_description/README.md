# 机器人的描述文件   
机器人的描述文件，用于描述机器人的物理属性、传感器、运动学参数等。

### 1、仿真阶段
```bash
# 使用步骤：
# 编译
colcon build
# 更新环境变量
source install/setup.bash
# 将xacro生成urdf文件
xacro src/robot_description/urdf/NaviRobot/NaviRobot.urdf.xacro
# 启动机器人xacro描述文件（在rviz中显示）
ros2 launch robot_description display_robot.launch.py model:=src/robot_description/urdf/NaviRobot/NaviRobot.urdf.xacro

# 启动NaviRobot机器人在gazebo中运行
ros2 launch robot_description gazebo_sim.launch.py

# 列出当前在控制器管理器（Controller Manager）中注册的所有控制器及其状态
ros2 control load_controller NaviRobot_joint_state_broadcaster --set-state active
ros2 control list_controllers
# 键盘控制机器人运动
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
**注意：** 在关掉gazebo后，如果进程中仍然有残留的gazebo进程，请使用kill命令将其终止，否则影响下一次运行。

### 2、导航阶段
```bash
# 1、建图
sudo apt install ros-$ROS_DISTRO-slam-toolbox   # 安装slam工具包
rviz2           # 要先启动rviz
ros2 launch robot_description gazebo_sim.launch.py
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```