###################################################################
#|                                                 @sonwezali    |#
#|                                                               |#
#| this script takes the coordinate [(x, y, z)] of a tx and some |#
#| angle in degrees as the inputs and then computes a new tx     |#
#| coordinate according to the inputs                            |#
#|                                                               |#
#|                                                               |#
###################################################################
import numpy as np

def enter_valid():
    print(
         "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n >>>ERROR: enter a valid value<<<\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
         )

def take_coordinate_input():
    x_coordinate, y_coordinate, z_coordinate = 0, 0, 0

    is_input_true = False
    while (not is_input_true):
        x_coordinate = input("enter the x-coordinate of the tx: ")
        if (len(x_coordinate) == 0):
            enter_valid()
            continue

        dot_index = x_coordinate.find(".")
        if (dot_index > 0):
            if (not x_coordinate[:dot_index].isnumeric()) or (not x_coordinate[dot_index + 1:].isnumeric()):
                enter_valid()
                continue

        if (not x_coordinate.isnumeric()):
            enter_valid()
            continue

        x_coordinate = float(x_coordinate)
    
        y_coordinate = input("enter the y-coordinate of the tx: ")
        if (len(y_coordinate) == 0):
            enter_valid()
            continue

        dot_index = y_coordinate.find(".")
        if (dot_index > 0):
            if (not y_coordinate[:dot_index].isnumeric()) or (not y_coordinate[dot_index + 1:].isnumeric()):
                enter_valid()
                continue

        if (not y_coordinate.isnumeric()):
            enter_valid()
            continue

        y_coordinate = float(y_coordinate)
    
        z_coordinate = input("enter the z-coordinate of the tx: ")
        if (len(z_coordinate) == 0):
            enter_valid()
            continue

        dot_index = z_coordinate.find(".")
        if (dot_index > 0):
            if (not z_coordinate[:dot_index].isnumeric()) or (not z_coordinate[dot_index + 1:].isnumeric()):
                enter_valid()
                continue

        if (not z_coordinate.isnumeric()):
            enter_valid()
            continue

        z_coordinate = float(z_coordinate)
        is_input_true = True

    return x_coordinate, y_coordinate, z_coordinate

def take_angle_input():
    angle = 0

    is_input_true = False
    while (not is_input_true):
        angle = input("enter the angle between txs in degrees (an integer): ")
        if (not angle.isnumeric()):
            enter_valid()
            continue
        elif (int(angle) < 0):
            enter_valid()
            continue

        angle = int(angle)
        is_input_true = True

    if (int(angle) > 360):
        angle %= 360

    return angle

def take_distance_input(default_distance):
    distance = default_distance 

    is_input_true = False
    while (not is_input_true):
        distance = input("enter the distance between the second tx and the center of the rx: ") 
        if (len(distance) == 0):
            print("\n~~~~~~choosing the distance same as the distance between the first tx and the rx~~~~~~\n")
            distance = default_distance
            is_input_true = True
            continue

        dot_index = distance.find(".")
        if (dot_index > 0):
            if (not distance[:dot_index].isnumeric()) or (not distance[dot_index + 1:].isnumeric()):
                enter_valid()
                continue

        if (not distance.isnumeric()):
            enter_valid()
            continue

        distance = float(distance)
        is_input_true = True
        
    return distance

def calculate_new_tx(x0, y0, z0, alpha, d):
    beta = np.rad2deg(np.arctan(y0/x0))
    new_tx_angle_rad = (alpha + beta) * np.pi/180.0
    x = np.sqrt(d**2 - z0**2) * np.cos(new_tx_angle_rad)
    y = np.sqrt(d**2 - z0**2) * np.sin(new_tx_angle_rad)
    z = z0

    return x, y, z

def main():
    tx_x, tx_y, tx_z = take_coordinate_input()
    tx0_coordinate = np.array([tx_x, tx_y, tx_z])
    print()

    angle = take_angle_input()
    print()

    distance = take_distance_input(np.linalg.norm(tx0_coordinate))
    print()

    x, y, z = calculate_new_tx(tx_x, tx_y, tx_z, angle, distance)
    print(f"x: {x} ------- y: {y} ------- z: {z}")

if __name__ == "__main__":
    main()
