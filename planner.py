# Type of planner
import numpy as np

POINT_PLANNER=0; TRAJECTORY_PLANNER=1

PARABOLA_TRAJECTORY=0; SIGMOID_TRAJECTORY=1

class planner:
    def __init__(self, type_):

        self.type=type_
        self.trajectoryType = PARABOLA_TRAJECTORY

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
    def sigmoid_trajectory_planner(self):
        trajectory_points = []
        x_values = np.linspace(0, 2.5, num=25)
        for x in x_values:
            y = 2 / (1 + np.exp(-2 * x)) - 1
            trajectory_points.append([x, y])
        return trajectory_points

    def parabola_trajectory_planner(self):
        trajectory_points = []
        x_values = np.linspace(0, 1.5, num=15)
        for x in x_values:
            y = x ** 2
            trajectory_points.append([x, y])
        return trajectory_points