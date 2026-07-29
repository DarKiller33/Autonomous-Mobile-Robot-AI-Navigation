# Custom Autonomous Mobile Robot (AMR) Navigation & AI Vision Pipeline

An advanced Autonomous Mobile Robot simulation framework built on **ROS 2 Humble** and **Gazebo Classic**. This repository features real-time asynchronous 2D SLAM mapping, reactive 3D obstacle avoidance using simulated depth cameras, real-time object tracking via deep learning pipelines (YOLOv8), and autonomous target coordination.

## 📁 Repository Structure
* **`launch/`**: Master ROS 2 scripts coordinating simulator environments.
* **`description/`**: Core hardware chassis frameworks and 3D depth sensor macros.
* **`config/`**: Localized SLAM mapping parameters and Nav2 costmap configurations.
* **`scripts/`**: Central python engine nodes handling OpenCV, YOLOv8 tracking, and action client coordination layers.
* **`videos/`** & **`docs/`**: Media demonstrations and engineering system architecture logs.

# Simulation Media
<img width="1883" height="987" alt="Yolo message" src="https://github.com/user-attachments/assets/f21bd7f3-4f50-490c-84d2-a6dd2206737d" />
<img width="1437" height="1011" alt="Sim 1" src="https://github.com/user-attachments/assets/52847e8a-f4a8-4edd-bb7b-2649e6c08269" />

## 🛠️ Installation & Dependency Setup

To run this project on your system, ensure you are using **Ubuntu 22.04 LTS** with **ROS 2 Humble** installed.

1. **Clone and Setup Workspace Directories:**
   ```bash
   mkdir -p ~/my_portfolio_ws/src
   cd ~/my_portfolio_ws/src
   # Clone this repository folder directly into your workspace src directory
   ```

2. **Install Python AI and Computer Vision Dependencies:**
   Navigate into the cloned package folder and run the pip installer targeting the requirements manifest:
   ```bash
   cd ~/my_portfolio_ws/src/my_amr_core
   pip3 install -r requirements.txt
   ```

3. **Build the Workspace:**
   ```bash
   cd ~/my_portfolio_ws
   colcon build --symlink-install
   source install/setup.bash
   ```

## 🚀 Complete Step-by-Step Execution Guide

Execute these commands across **9 separate terminal tabs or windows** in the exact sequential order listed below to launch the fully integrated system:

### Terminal 1: Launch Gazebo Simulation Environment
```bash
cd ~/my_portfolio_ws && source install/setup.bash
export LIBGL_ALWAYS_SOFTWARE=1  # Required for graphics stability on WSL2 instances
ros2 launch my_amr_core launch_sim.launch.py world:=\$HOME/my_portfolio_ws/src/my_amr_core/worlds/maze.world
```
*(Make sure to click the **Play** icon at the bottom center toolbar of Gazebo to start the physics server if it spawns paused).*

### Terminal 2: Launch Asynchronous SLAM Mapping
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

### Terminal 3: Launch Nav2 Navigation Stack
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true params_file:=/opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml
```

### Terminal 4: Launch RViz Visualization Panel
```bash
cd ~/my_portfolio_ws && source install/setup.bash
rviz2 -d src/my_amr_core/config/main.rviz
```
*(To view the 3D obstacle sensors field, click Add -> PointCloud2 -> select the `/camera/depth/color/points` topic. Use 2D Pose Estimate to resolve any localization alarms).*

### Terminal 5: Launch OpenCV Edge Detection Frame View (Phase 6)
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 run my_amr_core vision_processor.py
```

### Terminal 6: Launch YOLO AI Detection Node (Phase 6 & 7)
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 run my_amr_core yolo_detector.py
```

### Terminal 7: Audit AI Object Messaging Topic (Phase 7 Debug/Echo)
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 topic echo /detected_objects
```

### Terminal 8: Launch Intelligent Target Coordinator (Phase 9 Automation)
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 run my_amr_core intelligent_navigator.py
```

### Terminal 9: Launch Manual Keyboard Steering Node (Teleop)
```bash
cd ~/my_portfolio_ws && source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
*(Keep this terminal active to manually steer the robot chassis in front of obstacles to verify vision captures and 3D costmap expansions).*

---
*Note: This architecture is engineered as a standalone, portfolio-ready deployment module. All core physics macros, tracking loops, and sensor configurations are completely unified under independent package namespaces.*
