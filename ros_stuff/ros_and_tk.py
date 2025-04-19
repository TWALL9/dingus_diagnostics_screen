# From ChatGPT...

import tkinter as tk
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyROS2App(Node):
    def __init__(self, root):
        super().__init__("tkinter_ros2_example")
        self.root = root
        self.root.title("ROS 2 and Tkinter Example")

        # Label to display ROS messages
        self.label = tk.Label(root, text="Waiting for ROS 2 messages...")
        self.label.pack()

        # Create a subscriber for ROS 2
        self.subscriber = self.create_subscription(
            String, "/ros2_topic", self.ros_callback, 10
        )

        # Periodically call spin_once() without blocking Tkinter
        self.root.after(100, self.spin_ros)

    def ros_callback(self, msg):
        """Callback function for ROS 2 topic."""
        self.get_logger().info(f"Received message: {msg.data}")
        # Update the Tkinter label safely in the main thread
        self.root.after(0, self.update_label, msg.data)

    def update_label(self, msg):
        """Update Tkinter label with received message."""
        self.label.config(text=f"Received: {msg}")

    def spin_ros(self):
        """Process ROS 2 callbacks without blocking the Tkinter event loop."""
        rclpy.spin_once(self, timeout_sec=0.1)  # Check for ROS 2 messages
        self.root.after(100, self.spin_ros)  # Continue spinning periodically


def main():
    rclpy.init()  # Initialize the ROS 2 client library
    root = tk.Tk()
    app = MyROS2App(root)  # Create the app instance
    root.mainloop()  # Start the Tkinter main loop
    rclpy.shutdown()  # Shutdown ROS 2 when Tkinter exits


if __name__ == "__main__":
    main()
