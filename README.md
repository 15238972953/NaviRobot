# 自动驾驶感知系统

工程目录：
```
autonomous_perception_ws/
├── src/
│   ├── description/                      # URDF/Xacro 模型描述
│   │   ├── urdf/
│   │   │   └── vehicle.urdf.xacro
│   │   └── launch/
│   │       └── display.launch.py
│   |
│   ├── sensors/
│   │   ├── camera_sim/                  # 相机模拟节点（可基于 gazebo_plugins 或自定义）
│   │   ├── lidar_sim/                   # 激光雷达模拟插件配置
│   │   └── radar_sim/                   # 毫米波雷达模拟数据（自定义或脚本）
│   |
│   ├── gazebo_world/
│   │   ├── worlds/
│   │   │   └── city_lane.world          # 仿真地图
│   │   └── launch/
│   │       └── gazebo.launch.py         # 启动 Gazebo 并加载 world 和机器人
│   |
│   ├── perception/
│   │   ├── detection/                   # YOLOv5 or BEVDet 推理节点
│   │   ├── fusion/                      # 多传感器融合节点（Kalman/UKF/Fusion）
│   │   ├── bev_view/                    # BEV转换模块
│   │   └── tracking/                    # DeepSORT / ByteTrack 跟踪模块
│   |
│   ├── utils/
│   │   └── data_logger/                 # 数据记录与分析脚本（rosbag，csv，video）
│   |
│   └── launch/
│       └── full_system.launch.py        # 一键启动全部模块
│
├── install/
├── build/
├── log/
└── ros2_ws.env                         # 环境变量设置脚本（如 GAZEBO_MODEL_PATH）

```

