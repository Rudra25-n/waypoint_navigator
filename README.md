# ROS 2 Waypoint Navigator

A ROS 2 node that drives a simulated TurtleBot3 through a list of waypoints using the Nav2 navigation stack. It sends each goal in turn, checks the real outcome, and reports a mission summary.

[![Watch the demo on YouTube](https://img.youtube.com/vi/AupuNN1-x7s/hqdefault.jpg)](https://youtu.be/AupuNN1-x7s)

*Click the image to watch the demo.*

## What it does

- Loads a list of (x, y) waypoints from a YAML parameter file
- Sends them one at a time to Nav2's `NavigateToPose` action server
- Checks the result status of every goal, so an aborted goal is logged as a failure and skipped rather than reported as reached
- Times each leg in simulation time and prints a final success count

## How it works

Nav2 does the path planning and obstacle avoidance. This node is the mission layer on top: an action client that sends a goal, waits asynchronously for the result, then sends the next one. Before starting, it waits for the simulator's clock so that goal timestamps and timings are valid.

Note that Nav2 reports success when the robot is within its goal tolerance, which is not always the exact point requested.

## Requirements

- Ubuntu 26.04 (tested on WSL2 under Windows 11)
- ROS 2 Lyrical Luth
- Nav2 and its TurtleBot3 simulation:

```bash
sudo apt install ros-lyrical-navigation2 ros-lyrical-nav2-bringup
```

## Build

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/Rudra25-n/waypoint_navigator.git
cd ~/ros2_ws && colcon build && source install/setup.bash
```

## Run

Terminal 1, start Gazebo, Nav2 and RViz:

```bash
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```

Terminal 2, give Nav2 the robot's starting position as soon as RViz opens:

```bash
ros2 topic pub --once /initialpose geometry_msgs/msg/PoseWithCovarianceStamped "{header: {frame_id: map}, pose: {pose: {position: {x: -2.0, y: -0.5}, orientation: {w: 1.0}}}}"
```

When RViz shows "Navigation: active", run the node:

```bash
ros2 run waypoint_navigator waypoint_navigator --ros-args --params-file ~/ros2_ws/src/waypoint_navigator/config/waypoints.yaml
```

On WSL2, if RViz crashes on startup, run `export QT_QPA_PLATFORM=xcb` first.

## Configuration

Waypoints live in `config/waypoints.yaml` as a flat list read in x, y pairs:

```yaml
waypoint_navigator:
  ros__parameters:
    use_sim_time: true
    waypoints: [0.5, 0.5,
                0.5, -0.5,
                -0.5, -0.5,
                -0.5, 0.5]
```

## Example output

```
Loaded 4 waypoints
Navigating to waypoint1: (0.5,0.5)
Waypoint 1 reached in 2.7s
Navigating to waypoint2: (0.5,-0.5)
Waypoint 2 reached in 7.1s
Navigating to waypoint3: (-0.5,-0.5)
Waypoint 3 reached in 13.1s
Navigating to waypoint4: (-0.5,0.5)
Waypoint 4 reached in 6.8s
Mission complete: 4/4 waypoints reached
```

## Failure handling

When Nav2 aborts a goal, the node logs it, skips that waypoint and carries on. From a run where the controller could not get through a narrow gap:

```
Waypoint 2 FAILED after 61.4s (status 6), skipping
Navigating to waypoint3: (-0.5,-0.5)
Waypoint 3 reached in 10.7s
Mission complete: 3/4 waypoints reached
```

## Author

Rudra Bhosale

## License

MIT
