#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')

        # Subscribers
        self.sub1 = self.create_subscription(Int32MultiArray, '/input/array1', self.callback1, 10)
        self.sub2 = self.create_subscription(Int32MultiArray, '/input/array2', self.callback2, 10)

        # Publisher
        self.pub = self.create_publisher(Int32MultiArray, '/output/array', 10)

        self.array1 = []
        self.array2 = []

    def callback1(self, msg):
        self.array1 = msg.data
        self.publish_merged()

    def callback2(self, msg):
        self.array2 = msg.data
        self.publish_merged()

    def publish_merged(self):
        if self.array1 is not None and self.array2 is not None:
            # convert to list
            merged = sorted(list(self.array1) + list(self.array2))
            msg = Int32MultiArray()
            msg.data = merged
            self.pub.publish(msg)
            self.get_logger().info(f'Published merged array: {merged}')


def main(args=None):
    rclpy.init(args=args)
    node = MergeArraysNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()