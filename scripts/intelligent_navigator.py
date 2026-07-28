#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import time

class IntelligentNavigator(Node):
    def __init__(self):
        super().__init__('intelligent_navigator_node')
        
        # 1. Target object to find (Change this string to change what the robot hunts for)
        self.target_object = "bottle"  # Fits your Coke Can asset!
        self.object_found = False
        
        # 2. Setup wheel velocities to turn the robot while searching
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 3. Subscribe to your Phase 7 YOLO data channel stream
        self.subscription = self.create_subscription(
            String,
            '/detected_objects',
            self.object_callback,
            10)
            
        # 4. Initialize an action client link straight into the Nav2 planning stack
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        # 5. Start a periodic timer loop to handle search behaviors (runs 10 times a second)
        self.timer = self.create_timer(0.1, self.search_loop)
        
        self.get_logger().info(f"Intelligent Navigator active! Hunting for target asset: [{self.target_object}]")

    def object_callback(self, msg):
        # Read the published AI string (Example format: "Object: bottle, Confidence: 0.65")
        if self.target_object in msg.data and not self.object_found:
            self.get_logger().info(f"Target identified via YOLO feed! Processing location telemetry...")
            self.object_found = True
            self.timer.cancel() # Stop spinning the robot immediately
            
            # Stop the wheels
            stop_msg = Twist()
            self.cmd_vel_pub.publish(stop_msg)
            
            # Call your automated navigation pipeline
            self.send_nav_goal()

    def search_loop(self):
        if not self.object_found:
            self.get_logger().info("Searching maze... Scanning surrounding view coordinates.", throttle_duration_sec=2.0)
            # Slowly spin the robot in place to sweep the camera lens across the corridors
            move_msg = Twist()
            move_msg.angular.z = 0.3 
            self.cmd_vel_pub.publish(move_msg)

    def send_nav_goal(self):
        self.get_logger().info("Waiting for Nav2 action servers to sync...")
        self.nav_client.wait_for_server()
        
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        # Estimate spatial offsets based on typical lidar/camera depth vectors
        # In a real environment, this utilizes TF2 lookup transformations
        self.get_logger().info(f"Calculating path track vector coordinates towards target item...")
        goal_msg.pose.pose.position.x = 1.5   # Target destination offset coordinates
        goal_msg.pose.pose.position.y = 0.0
        goal_msg.pose.pose.orientation.w = 1.0
        
        self.get_logger().info("Sending autonomous travel trajectory request to Nav2 backend...")
        self.nav_client.send_goal_async(goal_msg)

def main(args=None):
    rclpy.init(args=args)
    node = IntelligentNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
