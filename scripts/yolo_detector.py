#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2

class YOLODetector(Node):
    def __init__(self):
        super().__init__('yolo_detector_node')
        self.get_logger().info('Loading YOLOv8 AI Model weight matrices...')
        self.model = YOLO('yolov8n.pt') 
        
        # Create the ROS2 publisher channel for object tracking data
        self.publisher_ = self.create_publisher(String, '/detected_objects', 10)
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        self.bridge = CvBridge()
        self.get_logger().info('YOLO AI Object Recognition + Publishing Node is operational!')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            results = self.model(cv_image, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0].item() if hasattr(box.cls, '__len__') else box.cls.item())
                    label = self.model.names[class_id]
                    confidence = float(box.conf[0].item() if hasattr(box.conf, '__len__') else box.conf.item())
                    
                    if confidence > 0.35:
                        # Fix: Extract the inner 1D array explicitly to prevent list unpacking crashes
                        coords = box.xyxy[0].tolist()
                        x1, y1, x2, y2 = map(int, coords)
                        
                        # Draw visual feedback elements
                        cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        caption = f"{label.upper()} {confidence:.2f}"
                        cv2.putText(cv_image, caption, (x1, y1 - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Pack and broadcast the ROS2 metadata stream string
                        ros_msg = String()
                        ros_msg.data = f"Object: {label}, Confidence: {confidence:.2f}"
                        self.publisher_.publish(ros_msg)
                        self.get_logger().info(f"Published: {ros_msg.data}")
            
            cv2.imshow("Robot AI Vision - YOLO Recognition View", cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f'YOLO inference module pipeline exception: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = YOLODetector()
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
