# 机器人的描述文件   
机器人的描述文件，用于描述机器人的物理属性、传感器、运动学参数等。

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
```
