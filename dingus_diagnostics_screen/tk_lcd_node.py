import tkinter as tk
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from PIL import ImageFont

from render import Canvas
from display_interfaces.tk.lcd_canvas import LcdCanvas
from mode_change_interfaces.tk import TkButton


class DiagnosticsScreenNode(Node):
    def __init__(self, root):
        super().__init__("diagnostics_screen_tk")
        self._root = root
        self._root.title("diagnostics_screen_tk")
        self._root.geometry("640x480")
        self._i = 0
        self._label = ""

        self._lcd_canvas = LcdCanvas(self._root, 380, 180)
        self._tk_button = TkButton(self._root, self.button_cb)

        self._subscriber = self.create_subscription(
            String, "/some_topic", self.ros_cb, 10
        )

        self._root.after(100, self.spin_ros)
        self._root.after(100, self.update_label)

    def button_cb(self, _now):
        self._i += 1

    def ros_cb(self, msg):
        self.get_logger().info(f"Received: {msg.data}")
        self._label = msg.data
        self._root.after(0, self.update_label)

    def draw(self, text):
        font = ImageFont.load_default()
        with Canvas(self._lcd_canvas) as draw:
            draw.text((0, 0), text, font=font, fill=255)

    def update_label(self):
        if self._i % 2 == 0:
            self.draw("even")
        else:
            self.draw(self._label)
        self._root.after(100, self.update_label)

    def spin_ros(self):
        rclpy.spin_once(self, timeout_sec=0.1)
        self._root.after(100, self.spin_ros)


def main():
    rclpy.init()
    root = tk.Tk()
    node = DiagnosticsScreenNode(root)
    root.mainloop()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
