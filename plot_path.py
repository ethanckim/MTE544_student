from turtle import color
import matplotlib.pyplot as plt
from utilities import FileReader

def plot_path():
    
    robotPose_headers, robotPose_values=FileReader("robot_pose.csv").read_file()
    plannedPath_headers, plannedPath_values=FileReader("planner_path.csv").read_file()
    obstacles_headers, obstacles_values=FileReader("planner_obstacles.csv").read_file()
    staticPoses_headers, staticPoses_values=FileReader("planner_poses.csv").read_file()
    
    plt.plot([x[8] for x in robotPose_values], [y[9] for y in robotPose_values], label='Odom Localization')
    plt.plot([x[0] for x in plannedPath_values], [y[1] for y in plannedPath_values], '-*', label="planned path")
    plt.plot([x[0] for x in staticPoses_values], [y[1] for y in staticPoses_values],'*', label="start_pose")
    plt.plot([x[2] for x in staticPoses_values], [y[3] for y in staticPoses_values], '*', label="end_pose")
    plt.plot([x[6] for x in robotPose_values], [y[7] for y in robotPose_values], label='EKF Localization')
    plt.plot([x[0] for x in obstacles_values], [y[1] for y in obstacles_values], '.', color="black")

    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')

    plt.legend()
    plt.grid()

    plt.show()


if __name__=="__main__":
    plot_path()