#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VisionProcessor(Node):
    def __init__(self):
        super().__init__('vision_processor_node')
        # Subscribe to the live camera feed topic coming out of Gazebo
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        
        # Initialize the CvBridge tool to safely convert images to OpenCV formats
        self.bridge = CvBridge()
        self.get_logger().info('OpenCV Vision Processor Node has been started successfully!')

    def image_callback(self, msg):
        try:
            # 1. Convert the ROS image message to a standard BGR OpenCV numpy array
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # 2. Run Computer Vision processing tasks (Edge Detection example)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)
            
            # 3. Pop open windows on your screen to display the results visually
            cv2.imshow("Robot Raw Camera Feed", cv_image)
            cv2.imshow("Robot OpenCV Edge Detection View", edges)
            
            # Force the display frame window to refresh
            cv2.waitKey(1)
            
        except Exception as e:
            self.get_logger().error(f'Failed to process incoming camera frame: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = VisionProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
