# Type of planner
import numpy as np

POINT_PLANNER=0; TRAJECTORY_PLANNER=1

# Type of trajectory
PARABOLA_TRAJECTORY=0; SIGMOID_TRAJECTORY=1

class planner:
    def __init__(self, type_):

        self.type=type_
        self.trajectoryType = SIGMOID_TRAJECTORY
        self.simulation = False # Set to True if running in simulation

    def plan(self, goalPoint=[-1.0, -1.0]):
        # NOTE: goalPoint is used only for the pointPlanner
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            if self.trajectoryType == SIGMOID_TRAJECTORY:
                return self.sigmoid_trajectory_planner()
            elif self.trajectoryType == PARABOLA_TRAJECTORY:
                return self.parabola_trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # Part 6: Implement the trajectories here
    # Generate sigmoid trajectory using given equation
    def sigmoid_trajectory_planner(self):
        if self.simulation:
            starting_x = -2
            starting_y = -0.5
        else:
            starting_x=0
            starting_y=0

        trajectory_points = []
        x_values = np.linspace(float(0 + starting_x), float(2.5 + starting_x), num=25)
        for x in x_values:
            y = 2 / (1 + np.exp(-2 * (x - starting_x))) - 1 + starting_y
            trajectory_points.append([x, y])
        return trajectory_points


    # Generate parabola trajectory using given equation
    def parabola_trajectory_planner(self):
        if self.simulation:
            starting_x = -2
            starting_y = -0.5
        else:
            starting_x=0
            starting_y=0

        trajectory_points = []
        x_values = np.linspace(float(0 + starting_x), float(1.5 + starting_x), num=15)
        for x in x_values:
            y = (x - starting_x) ** 2 + starting_y
            trajectory_points.append([x, y])
        return trajectory_points