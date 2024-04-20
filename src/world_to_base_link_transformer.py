#!/usr/bin/env python

import rospy
import tf2_ros
import geometry_msgs.msg
import tf.transformations

class WorldToBaseLinkTransformer:
    def __init__(self):
        rospy.init_node('world_to_base_link_transformer')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.pub = rospy.Publisher('/base_link', geometry_msgs.msg.PoseStamped, queue_size=10)

    def transform_world_to_base_link(self):
        rate = rospy.Rate(10)  # 10Hz

        while not rospy.is_shutdown():
            try:
                # Get the transform from world to base_link
                transform = self.tf_buffer.lookup_transform("base_link", "world", rospy.Time(0), rospy.Duration(1.0))

                # Create a PoseStamped message
                pose_world = geometry_msgs.msg.PoseStamped()
                pose_world.header.frame_id = "world"
                pose_world.pose.position.x = 0.0  # Set initial position to origin
                pose_world.pose.position.y = 0.0
                pose_world.pose.position.z = 0.0

                # Assuming you have IMU data for roll, pitch, and yaw
                roll = 0.0  # Replace with your IMU roll value
                pitch = 0.0  # Replace with your IMU pitch value
                yaw = 0.0  # Replace with your IMU yaw value

                # Convert Euler angles to quaternion
                quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
                pose_world.pose.orientation.x = quaternion[0]
                pose_world.pose.orientation.y = quaternion[1]
                pose_world.pose.orientation.z = quaternion[2]
                pose_world.pose.orientation.w = quaternion[3]

                # Transform the pose to base_link frame
                pose_base_link = self.tf_buffer.transform(pose_world, "base_link")

                # Publish the transformed pose
                self.pub.publish(pose_base_link)

            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rospy.logwarn("Failed to transform world to base_link")

            rate.sleep()

if __name__ == '__main__':
    try:
        transformer = WorldToBaseLinkTransformer()
        transformer.transform_world_to_base_link()
    except rospy.ROSInterruptException:
        pass

