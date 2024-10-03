import rclpy
import argparse
# Part 3: Import message types needed:
# For sending velocity commands to the robot: Twist
# For the sensors: Imu, LaserScan, and Odometry
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.time import Time
from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan

from utilities import Logger, euler_from_quaternion, convert_to_degrees

CIRCLE = 0;
SPIRAL = 1;
ACC_LINE = 2
motion_types = ['circle', 'spiral', 'line']


class MotionExecutioner(Node):

    def __init__(self, motion_type=0):

        super().__init__("motion_types")

        self.type = motion_type

        self.time_passed_ = 0

        self.successful_init = False
        self.imu_initialized = False
        self.odom_initialized = False
        self.laser_initialized = False

        # Part 3: Create a publisher to send velocity commands
        self.vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # loggers
        self.imu_logger = Logger('imu_content_' + str(motion_types[motion_type]) + '.csv',
                                 headers=["acc_x", "acc_y", "angular_z", "stamp"])
        self.odom_logger = Logger('odom_content_' + str(motion_types[motion_type]) + '.csv',
                                  headers=["x", "y", "th", "th_deg", "stamp"])
        self.laser_logger = Logger('laser_content_' + str(motion_types[motion_type]) + '.csv',
                                   headers=["ranges", "angle_increment", "stamp"])

        # Part 3: Create the QoS profile by setting the proper parameters
        # reliability = RELIABLE (2): messages are delivered to subscribers at least once (ack receipt)
        # durability = TRANSIENT_LOCAL (2): messages are stored for late-joining local subscribers
        # history = KEEP_LAST (1): history buffer keeps 1 latest msg
        # depth = 10: queue depth
        qos = QoSProfile(reliability=2, durability=2, history=1, depth=10)

        # Part 5: Create below the subscription to the topics corresponding to the respective sensors
        # Imu subscription
        self.create_subscription(Imu, "/imu", self.imu_callback, qos_profile=qos)
        self.imu_initialized = True

        # Encoder subscription
        self.create_subscription(Odometry, "/odom", self.odom_callback, qos_profile=qos)
        self.odom_initialized = True

        # LaserScan subscription 
        self.create_subscription(LaserScan, "/scan", self.laser_callback, qos_profile=qos)
        self.laser_initialized = True

        # Timer callback
        self.create_timer(0.1, self.timer_callback)

    # Part 5: Callback functions: callback functions of the three sensors to log the proper data.
    # To also log the time you need to use the rclpy Time class, each ros msg will come with a header, and then
    # inside the header you have a stamp that has the time in seconds and nanoseconds, you should log it in nanoseconds
    # as such: Time.from_msg(imu_msg.header.stamp).nanoseconds
    # You can save the needed fields into a list, and pass the list to the log_values function in utilities.py
    def imu_callback(self, imu_msg: Imu):
        # get timestamp
        timestamp = Time.from_msg(imu_msg.header.stamp).nanoseconds

        # get data: headers=["acc_x", "acc_y", "angular_z", "stamp"]
        imu_acc_x = imu_msg.linear_acceleration.x
        imu_acc_y = imu_msg.linear_acceleration.y
        imu_angular_z = imu_msg.angular_velocity.z

        # Consolidate data to list
        imu_data_list = [imu_acc_x, imu_acc_y, imu_angular_z, timestamp]

        self.imu_logger.log_values(imu_data_list)

    def odom_callback(self, odom_msg: Odometry):
        # get timestamp
        timestamp = Time.from_msg(odom_msg.header.stamp).nanoseconds

        # get data: headers=["x","y","th", "th_deg", "stamp"]
        odom_orientation = euler_from_quaternion(odom_msg.pose.pose.orientation)
        odom_orientation_deg = convert_to_degrees(odom_orientation)
        odom_x_pos = odom_msg.pose.pose.position.x
        odom_y_pos = odom_msg.pose.pose.position.y

        # Consolidate data to list
        data_list = [odom_x_pos, odom_y_pos, odom_orientation, odom_orientation_deg, timestamp]

        self.odom_logger.log_values(data_list)

    def laser_callback(self, laser_msg: LaserScan):
        # get timestamp
        timestamp = Time.from_msg(laser_msg.header.stamp).nanoseconds

        # get data: headers=["ranges", "angle_increment", "stamp"]
        ranges = laser_msg.ranges
        angle_increment = laser_msg.angle_increment

        # Consolidate data to list
        data_list = [ranges, angle_increment, timestamp]

        self.laser_logger.log_values(data_list)

    def timer_callback(self):

        if self.odom_initialized and self.laser_initialized and self.imu_initialized:
            self.successful_init = True

        if not self.successful_init:
            return

        cmd_vel_msg = Twist()

        if self.type == CIRCLE:
            cmd_vel_msg = self.make_circular_twist()

        elif self.type == SPIRAL:
            cmd_vel_msg = self.make_spiral_twist()

        elif self.type == ACC_LINE:
            cmd_vel_msg = self.make_acc_line_twist()

        else:
            print("type not set successfully, 0: CIRCLE 1: SPIRAL and 2: ACCELERATED LINE")
            raise SystemExit

        self.vel_publisher.publish(cmd_vel_msg)

    # Part 4: Motion functions: generates the proper messages corresponding to the desired motions of the robot
    # robot frame convention: x = forward, y = left, z = up
    def make_circular_twist(self):

        msg = Twist()

        msg.linear.x = 0.3
        msg.angular.z = 0.6

        self.vel_publisher.publish(msg)
        return msg

    def make_spiral_twist(self):
        msg = Twist()

        # These parameters will affect the spiral
        constant_linear_vel = 0.5
        rate_of_decrease = 0.05
        initial_radius = 1

        # If spiral radius is greater than 0, keep updating the angular velocity
        if initial_radius - rate_of_decrease * self.time_passed_ > 0:
            msg.linear.x = constant_linear_vel # Constant linear velocity
            msg.angular.z = constant_linear_vel / (initial_radius - rate_of_decrease * self.time_passed_) # Decreasing angular velocity
        else:
            # Stop the robot when the spiral radius becomes 0
            msg.linear.x = 0
            msg.angular.z = 0

        self.vel_publisher.publish(msg)
        self.time_passed_ += 0.1 # Increment time passed by 0.1 seconds everytime the callback runs
        return msg

    def make_acc_line_twist(self):
        msg = Twist()

        msg.linear.x = 0.3

        self.vel_publisher.publish(msg)
        return msg


if __name__ == "__main__":

    argParser = argparse.ArgumentParser(description="input the motion type")
    argParser.add_argument("--motion", type=str, default="circle")

    rclpy.init()

    args = argParser.parse_args()

    if args.motion.lower() == "circle":
        ME = MotionExecutioner(motion_type=CIRCLE)
    elif args.motion.lower() == "line":
        ME = MotionExecutioner(motion_type=ACC_LINE)
    elif args.motion.lower() == "spiral":
        ME = MotionExecutioner(motion_type=SPIRAL)
    else:
        print(f"we don't have {args.motion.lower()} motion type")

    try:
        rclpy.spin(ME)
    except KeyboardInterrupt:
        print("Exiting")
