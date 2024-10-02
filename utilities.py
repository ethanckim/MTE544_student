from math import atan2, asin, sqrt

M_PI=3.1415926535

class Logger:
    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        self.filename = filename

        with open(self.filename, 'w') as file:
            header_str=""

            for header in headers:
                header_str+=header
                header_str+=", "
            
            header_str+="\n"
            
            file.write(header_str)


    def log_values(self, values_list):

        with open(self.filename, 'a') as file:
            vals_str=""

            # Part 5: Write the values from the list to the file
            for item in values_list:
                if isinstance(item, list):
                    # If item is a list, convert it to a list of strings and add to vals_str
                    vals_str += ", ".join(map(str, item)) + ", "
                else:
                    vals_str += str(item) + ", "
            
            # Remove trailing comma and add new line
            vals_str = vals_str.rstrip(", ") + "\n"
            
            file.write(vals_str)
            

    def save_log(self):
        pass

class FileReader:
    def __init__(self, filename):
        
        self.filename = filename
        
        
    def read_file(self):
        
        read_headers=False

        table=[]
        headers=[]
        with open(self.filename, 'r') as file:
            # Skip the header line

            if not read_headers:
                for line in file:
                    values=line.strip().split(',')

                    for val in values:
                        if val=='':
                            break
                        headers.append(val.strip())

                    read_headers=True
                    break
            
            next(file)
            
            # Read each line and extract values
            for line in file:
                values = line.strip().split(',')
                
                row=[]                
                
                for val in values:
                    if val=='':
                        break
                    row.append(float(val.strip()))

                table.append(row)
        
        return headers, table


# Part 5: Convert from Quaternion to Euler Angles
def euler_from_quaternion(quat):
    """
    Convert quaternion (w in last place) to euler roll, pitch, yaw.
    quat = [x, y, z, w]
    """

    x, y, z, w = normalize_quaternion(quat)

    # Note that we are choosing not to handle gimbal lock because it is very unlikely to happen in our case
    # the pitch shouldn't be changing much
    # If needed, we could test for gimbal lock

    # Calculate Roll - commented as not used
    # roll = calculate_roll(x, y, z, w)

    # Calculate Pitch - commented as not used
    # pitch = calculate_pitch(x, y, z, w)

    # Calculate Yaw
    yaw = calculate_yaw(x, y, z, w)

    # return yaw in degrees (can be changed to radians if wanted)
    return yaw


def normalize_quaternion(quat):
    x = quat.x
    y = quat.y
    z = quat.z
    w = quat.w

    # normalize the quaternion to make sure it represents a valid rotation
    # this shouldn't be necessary because ROS should give you a normalized quaternion, but its good practice
    norm = sqrt(x**2 + y**2 + z**2 + w**2)
    x /= norm
    y /= norm
    z /= norm
    w /= norm

    return x, y, z, w


def calculate_roll(x, y, z, w):
    sin_roll_cos_pitch = 2.0 * (w * x + y * z)
    cos_roll_cos_pitch = 1.0 - 2.0 * (x**2 + y**2)
    roll = atan2(sin_roll_cos_pitch, cos_roll_cos_pitch)
    return roll


def calculate_pitch(x, y, z, w):
    sin_pitch = sqrt(1.0 + 2.0 * (w * y - x * z))
    cos_pitch = sqrt(1.0 - 2.0 * (w * y - x * z))
    pitch = 2.0 * atan2(sin_pitch, cos_pitch) - M_PI/2.0
    return pitch


def calculate_yaw(x, y, z, w):
    sin_yaw_cos_pitch = 2.0 * (w * z + x * y)
    cos_yaw_cos_pitch = 1.0 - 2.0 * (y * y + z * z)
    yaw = atan2(sin_yaw_cos_pitch, cos_yaw_cos_pitch)
    return yaw


def convert_to_degrees(radians):
    return radians * 180 / M_PI
