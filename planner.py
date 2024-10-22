# Type of planner
import numpy as np

POINT_PLANNER=0; TRAJECTORY_PLANNER=1

PARABOLA_TRAJECTORY=0; SIGMOID_TRAJECTORY=1

class planner:
    def __init__(self, type_):

        self.type=type_
        self.trajectoryType = SIGMOID_TRAJECTORY

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
    # Regular Sigmoid
    def sigmoid_trajectory_planner(self):
        trajectory_points = []
        x_values = np.linspace(0, 2.5, num=25)
        for x in x_values:
            y = 2 / (1 + np.exp(-2 * x)) - 1
            trajectory_points.append([x, y])
        return trajectory_points

    # Simulation Sigmoid
    def sigmoid_trajectory_planner(self):
        trajectory_points = []
        x_values = np.linspace(-2, 0.5, num=25)

        # Robot in sim starts off at these coordinates so it was required
        starting_x = -2
        starting_y = -0.5

        for x in x_values:
            y = 2 / (1 + np.exp(-2 * (x-starting_x))) - 1 + starting_y
            trajectory_points.append([x, y])
        return trajectory_points

    # Regular parabola
    # def parabola_trajectory_planner(self):
    #     trajectory_points = []
    #     x_values = np.linspace(0, 1.5, num=15)
    #     for x in x_values:
    #         y = x ** 2
    #         trajectory_points.append([x, y])
    #     return trajectory_points

    # Simulation Parabola
    def parabola_trajectory_planner(self):
        trajectory_points = []
        x_values = np.linspace(-2, -0.5, num=15)

        # Robot in sim starts off at these coordinates so it was required
        starting_x = -2
        starting_y = -0.5

        for x in x_values:
            y = ((x-starting_x) ** 2) + starting_y
            trajectory_points.append([x, y])
        return trajectory_points