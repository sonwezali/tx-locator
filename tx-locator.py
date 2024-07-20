###################################################################
#|                                                 @sonwezali    |#
#|                                                               |#
#| this script takes the coordinates [(x, y, z)] of a tx and some|#
#| angle in degrees as the inputs and then computes a new tx     |#
#| coordinates according to the inputs                           |#
#|                                                               |#
#|                                                               |#
###################################################################
import numpy as np

def enter_valid():
    print(
         "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n >>>ERROR: enter a valid value<<<\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
         )

def take_coordinate_input():
    def parse_float_input(prompt):
        while True:
            value = input(prompt)
            try:
                return float(value)
            except ValueError:
                enter_valid()

    x_coordinate = parse_float_input("enter the x-coordinate of the tx: ")
    y_coordinate = parse_float_input("enter the y-coordinate of the tx: ")
    z_coordinate = parse_float_input("enter the z-coordinate of the tx: ")

    return x_coordinate, y_coordinate, z_coordinate

def take_angle_input():
    while True:
        angle = input("enter the angle between txs in degrees (an integer): ")
        try:
            angle = int(angle)
            if angle < 0:
                raise ValueError
            return angle % 360
        except ValueError:
            enter_valid()

def take_distance_input(default_distance):
    while True:
        distance = input("enter the distance between the second tx and the center of the rx: ")
        if len(distance) == 0:
            print("\n~~~~~~choosing the distance same as the distance between the first tx and the rx~~~~~~\n")
            return default_distance
        try:
            return float(distance)
        except ValueError:
            enter_valid()

def calculate_new_tx(x0, y0, z0, alpha, d):
    initial_vector = np.array([x0, y0, z0])
    initial_distance = np.linalg.norm(initial_vector)
    initial_vector_normalized = initial_vector/initial_distance

    # calculate rotation axis (cross product of initial vector and z-axis)
    rotation_axis = np.cross(initial_vector_normalized, np.array([0, 0, 1]))
    if np.linalg.norm(rotation_axis) == 0:
        # arbitrary orthogonal axis if initial vector is along z-axis (x-axis in this case)
        rotation_axis = np.array([1, 0, 0])  
    rotation_axis_normalized = rotation_axis / np.linalg.norm(rotation_axis)

    # calculate rotation matrix using Rodrigues' rotation formula
    alpha_rad = np.deg2rad(alpha)
    K = np.array([[0, -rotation_axis_normalized[2], rotation_axis_normalized[1]],
                  [rotation_axis_normalized[2], 0, -rotation_axis_normalized[0]],
                  [-rotation_axis_normalized[1], rotation_axis_normalized[0], 0]])
    R = np.eye(3) + np.sin(alpha_rad) * K + (1 - np.cos(alpha_rad)) * np.dot(K, K)

    # calculate new vector and scale it to the desired distance
    new_vector = np.dot(R, initial_vector_normalized) * d
    return new_vector

def angle_between_vectors(a, b):
    dot_product = np.dot(a, b)
    
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    cos_theta = dot_product / (norm_a * norm_b)
    
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    
    angle_rad = np.arccos(cos_theta)
    
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg

def main():
    tx_x, tx_y, tx_z = take_coordinate_input()
    tx0_coordinate = np.array([tx_x, tx_y, tx_z])
    print()

    angle = take_angle_input()
    print()

    distance = take_distance_input(np.linalg.norm(tx0_coordinate))
    print()

    x, y, z = calculate_new_tx(tx_x, tx_y, tx_z, angle, distance)
    print("coordinates of the new tx")
    print(f"x: {x}\ny: {y}\nz: {z}\n")

    # # some debug lines
    # print()
    # print(f"Angle between vectors: {angle_between_vectors(tx0_coordinate, np.array([x, y, z]))} degrees")
    # print(np.linalg.norm(tx0_coordinate), np.linalg.norm(np.array([x, y, z])))

if __name__ == "__main__":
    main()

