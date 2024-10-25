# Imports


import sys

from utilities import euler_from_quaternion, calculate_angular_error, calculate_linear_error
from pid import PID_ctrl

from rclpy import init, spin, spin_once
from rclpy.node import Node
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, QoSHistoryPolicy
from nav_msgs.msg import Odometry as odom

from localization import localization, rawSensor

from planner import TRAJECTORY_PLANNER, POINT_PLANNER, planner
from controller import controller, trajectoryController

# You may add any other imports you may need/want to use below
# import ...


class decision_maker(Node):
    
    def __init__(self, publisher_msg, publishing_topic, qos_publisher, goal_point=None, rate=10, motion_type=POINT_PLANNER):

        super().__init__("decision_maker")

        # Part 4: Create a publisher for the topic responsible for robot's motion
        self.publisher=self.create_publisher(publisher_msg, publishing_topic, qos_publisher)

        publishing_period=1/rate
        
        # Instantiate the controller
        # TODO Part 5: Tune your parameters here
    
        if motion_type == POINT_PLANNER:
            # self.controller=controller(klp=0.5, kap=1.0, controller_type=0) # P

            # self.controller=controller(klp=0.5, klv=1.0, kli=5.0, kap=1.0, kav=0.25, kai=1.0, controller_type=1) # PD

            # self.controller=controller(klp=0.5, klv=1.0, kli=1.0, kap=1.0, kav=0.25, kai=0.2, controller_type=2) # PI

            self.controller=controller(klp=0.5, klv=1.0, kli=1.0, kap=1.0, kav=0.25, kai=0.2, controller_type=3) # PID


            self.planner=planner(POINT_PLANNER)    
    
    
        elif motion_type==TRAJECTORY_PLANNER:
            # PARABOLA
            # self.controller=trajectoryController(klp=0.5, klv=1.0, kli=1.0, kap=1.3, kav=0.3, kai=1.0, controller_type=3) # PID
            # SIGMOID
            self.controller=trajectoryController(klp=0.4, klv=0.3, kli=0.3, kap=1.1, kav=1.5, kai=1.0, controller_type=3) # PID

            self.planner=planner(TRAJECTORY_PLANNER)

        else:
            print("Error! you don't have this planner", file=sys.stderr)


        # Instantiate the localization, use rawSensor for now  
        self.localizer=localization(rawSensor)

        # Instantiate the planner
        self.goal=self.planner.plan()

        # Error thresholds for evaluating if goal is reached
        self.linear_threshold = 0.1 # m
        self.angular_threshold = 0.05 # rad

        self.create_timer(publishing_period, self.timerCallback)


    def timerCallback(self):
        
        # Part 3: Run the localization node
        spin_once(self.localizer)

        if self.localizer.getPose() is None:
            print("waiting for odom msgs ....")
            return

        vel_msg=Twist()
        
        # Part 3: Check if you reached the goal
        currPose = self.localizer.getPose()
        if type(self.goal) == list: # Trajectory planner
            reached_goal = (abs(calculate_linear_error(currPose, self.goal[-1])) < self.linear_threshold and
                            abs(calculate_angular_error(currPose, self.goal[-1])) < self.angular_threshold)
        else: # Point planner
            reached_goal = (abs(calculate_linear_error(currPose, self.goal)) < self.linear_threshold and
                            abs(calculate_angular_error(currPose, self.goal)) < self.angular_threshold)

        if reached_goal:
            print("reached goal")
            self.publisher.publish(vel_msg)
            
            self.controller.PID_angular.logger.save_log()
            self.controller.PID_linear.logger.save_log()
            
            # Part 3: exit the spin
            raise SystemExit
        
        velocity, yaw_rate = self.controller.vel_request(currPose, self.goal, True)

        # Part 4: Publish the velocity to move the robot
        vel_msg.linear.x = velocity
        vel_msg.angular.z = yaw_rate

        self.publisher.publish(vel_msg)

import argparse


def main(args=None):
    
    init()

    # Part 3: You might need to change the QoS profile based on whether you're using the real robot or in simulation.

    # Turtle Bot 4 CMD VEL QOS
    cmd_vel_qos=QoSProfile(reliability=QoSReliabilityPolicy.RELIABLE,
                        durability=QoSDurabilityPolicy.VOLATILE,
                        history=QoSHistoryPolicy.KEEP_LAST,
                        depth=10)

    # Turtle Bot 3 CMD VEL QOS
    # cmd_vel_qos = QoSProfile(reliability=QoSReliabilityPolicy.RELIABLE,
    #                          durability=QoSDurabilityPolicy.VOLATILE,
    #                          history=QoSHistoryPolicy.KEEP_LAST,
    #                          depth=10)
    

    # Part 4: instantiate the decision_maker with the proper parameters for moving the robot
    if args.motion.lower() == "point":
        DM=decision_maker(Twist, "/cmd_vel", cmd_vel_qos, motion_type=POINT_PLANNER)
    elif args.motion.lower() == "trajectory":
        DM=decision_maker(Twist, "/cmd_vel", cmd_vel_qos, motion_type=TRAJECTORY_PLANNER)
    else:
        print("invalid motion type", file=sys.stderr)
    
    
    try:
        spin(DM)
    except SystemExit:
        print(f"reached there successfully {DM.localizer.pose}")


if __name__=="__main__":

    argParser=argparse.ArgumentParser(description="point or trajectory") 
    argParser.add_argument("--motion", type=str, default="point")
    args = argParser.parse_args()

    main(args)
