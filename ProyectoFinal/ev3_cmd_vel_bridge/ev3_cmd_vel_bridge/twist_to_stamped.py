#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node


class TwistToStamped(Node):
    """Convierte geometry_msgs/Twist en geometry_msgs/TwistStamped."""

    def __init__(self) -> None:
        super().__init__('twist_to_stamped')

        self.declare_parameter('input_topic', '/cmd_vel')
        self.declare_parameter(
            'output_topic',
            '/bicycle_steering_controller/reference'
        )
        self.declare_parameter('frame_id', 'base_link')

        input_topic = str(
            self.get_parameter('input_topic').value
        )
        output_topic = str(
            self.get_parameter('output_topic').value
        )
        self.frame_id = str(
            self.get_parameter('frame_id').value
        )

        self.publisher = self.create_publisher(
            TwistStamped,
            output_topic,
            10
        )

        self.subscription = self.create_subscription(
            Twist,
            input_topic,
            self.twist_callback,
            10
        )

        self.get_logger().info(
            f'Convirtiendo Twist: {input_topic} -> '
            f'TwistStamped: {output_topic}'
        )

    def twist_callback(self, msg: Twist) -> None:
        stamped = TwistStamped()
        stamped.header.stamp = self.get_clock().now().to_msg()
        stamped.header.frame_id = self.frame_id
        stamped.twist = msg

        self.publisher.publish(stamped)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = TwistToStamped()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
