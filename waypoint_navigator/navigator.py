import rclpy
from rclpy.node import Node
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('waypoint_navigator')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        #defining waypoints As (x,y)
        self.waypoints = [
            (0.5, 0.5),
            (0.5, -0.5),
            (5.0, 5.0),
            (-0.5, -0.5),
            (-0.5, 0.5),
        
         ]
        self.current = 0
        self.succeeded = 0 

    def send_next_waypoint(self):
        if self.current >= len(self.waypoints):
            self.get_logger().info(f'Mission complete: {self.succeeded}/{len(self.waypoints)} waypoints reached') 
            return

        x,y = self.waypoints[self.current]
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'Navigating to waypoint{self.current + 1}: ({x},{y})')
        self._client.wait_for_server()
        future = self._client.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)


    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warning('Goal rejected')
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)


    def result_callback(self, future):
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f'Waypoint {self.current + 1} reached!')
            self.succeeded += 1
        else:
            self.get_logger().warning(f'Waypoint {self.current + 1} FAILED (status {status}), skipping')
        self.current += 1
        self.send_next_waypoint()



def main(args=None):
    rclpy.init(args=args)
    navigator = WaypointNavigator()
    navigator.send_next_waypoint()
    rclpy.spin(navigator)
    rclpy.shutdown()

if __name__ == '__main__':
    main()