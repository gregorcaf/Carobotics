import math
import numpy as np
import random


def read_data(name):
    all_points = []
    points_to_choose = []
    arr_p = []
    arr_t = []

    times = []

    sums = []

    results = []

    file = open(name, "r")
    num_of_points = int(file.readline())

    for i in range(num_of_points):
        line = file.readline()
        num_split = line.split(" ")
        map_object = map(float, num_split)
        coordinates = list(map_object)
        all_points.append(np.array([coordinates[0], coordinates[1], coordinates[2]]))

    while 1:
        line = file.readline()

        if line == '':
            break

        num_of_points = int(line)

        for i in range(num_of_points):
            line = file.readline()
            num_split = line.split(" ")
            map_object = map(float, num_split)
            coordinates = list(map_object)

            # v polji dodamo postajo in cas
            index = int(coordinates[0])
            points_to_choose.append(all_points[index])
            times.append(coordinates[1])

        # dodamo prvi element => najmanjsa vrednost !!!!!
        arr_p.append(points_to_choose[0])
        arr_t.append(times[0])

        p0 = points_to_choose.pop(0)
        t0 = times.pop(0)

        # print("points to choose: \n", points_to_choose)

        choices = list(range(len(points_to_choose)))

        # dokler ne izberemo 4 tock (ena tocka je ze dodana v list)
        while len(sums) != 4:
            random.shuffle(choices)
            sum_value = sum(choices[:4])

            if sum_value not in sums:
                sums.append(sum_value)
                arr_p = [p0, points_to_choose[choices[0]], points_to_choose[choices[1]], points_to_choose[choices[2]], points_to_choose[choices[3]]]
                arr_t = [t0, times[choices[0]], times[choices[1]], times[choices[2]], times[choices[3]]]

                print("ARRAYS TO SEND:")
                print(arr_p)
                print(arr_t)
                results.append(trilateration(arr_p, arr_t))

        points_to_choose.clear()
        times.clear()
        arr_p.clear()
        arr_t.clear()
        sums.clear()
    for i in range(len(results)):
        print(i + 1, ") ", results[i])


def trilateration(arr_points, arr_times):
    point_4 = 0
    r_4 = 0

    num_of_points = len(arr_points)
    point_0 = np.float64(arr_points[0])
    point_1 = np.float64(arr_points[1])
    point_2 = np.float64(arr_points[2])
    point_3 = np.float64(arr_points[3])
    point_4 = np.float64(arr_points[4])

    # TODO TODO kako izracunas r_0 ??????
    # TODO TODO kako izracunas r_0 ??????
    # TODO TODO kako izracunas r_0 ??????
    r_0 = math.sqrt(math.pow(point_0[0], 2) + math.pow(point_0[1], 2) + math.pow(point_0[2], 2))

    r_delta_1 = 343 * np.float64(arr_times[1] - arr_times[0])
    r_delta_2 = 343 * np.float64(arr_times[2] - arr_times[0])
    r_delta_3 = 343 * np.float64(arr_times[3] - arr_times[0])
    r_delta_4 = 343 * np.float64(arr_times[4] - arr_times[0])

    x_delta_1 = point_1[0] - point_0[0]
    x_delta_2 = point_2[0] - point_0[0]
    x_delta_3 = point_3[0] - point_0[0]
    x_delta_4 = point_4[0] - point_0[0]

    y_delta_1 = point_1[1] - point_0[1]
    y_delta_2 = point_2[1] - point_0[1]
    y_delta_3 = point_3[1] - point_0[1]
    y_delta_4 = point_4[1] - point_0[1]

    z_delta_1 = point_1[2] - point_0[2]
    z_delta_2 = point_2[2] - point_0[2]
    z_delta_3 = point_3[2] - point_0[2]
    z_delta_4 = point_4[2] - point_0[2]

    point_delta_1 = point_1 - point_0
    point_delta_2 = point_2 - point_0
    point_delta_3 = point_3 - point_0
    point_delta_4 = point_4 - point_0

    a_2 = 2 * x_delta_2 / r_delta_2 - 2 * x_delta_1 / r_delta_1
    a_3 = 2 * x_delta_3 / r_delta_3 - 2 * x_delta_1 / r_delta_1
    a_4 = 2 * x_delta_4 / r_delta_4 - 2 * x_delta_1 / r_delta_1

    b_2 = 2 * y_delta_2 / r_delta_2 - 2 * y_delta_1 / r_delta_1
    b_3 = 2 * y_delta_3 / r_delta_3 - 2 * y_delta_1 / r_delta_1
    b_4 = 2 * y_delta_4 / r_delta_4 - 2 * y_delta_1 / r_delta_1

    c_2 = 2 * z_delta_2 / r_delta_2 - 2 * z_delta_1 / r_delta_1
    c_3 = 2 * z_delta_3 / r_delta_3 - 2 * z_delta_1 / r_delta_1
    c_4 = 2 * z_delta_4 / r_delta_4 - 2 * z_delta_1 / r_delta_1

    d_2 = r_delta_2 - r_delta_1 - (math.pow(x_delta_2, 2) + math.pow(y_delta_2, 2) + math.pow(z_delta_2, 2)) / r_delta_2 + (math.pow(x_delta_1, 2) + math.pow(y_delta_1, 2) + math.pow(z_delta_1, 2)) / r_delta_1
    d_3 = r_delta_3 - r_delta_1 - (math.pow(x_delta_3, 2) + math.pow(y_delta_3, 2) + math.pow(z_delta_3, 2)) / r_delta_3 + (math.pow(x_delta_1, 2) + math.pow(y_delta_1, 2) + math.pow(z_delta_1, 2)) / r_delta_1
    d_4 = r_delta_4 - r_delta_1 - (math.pow(x_delta_4, 2) + math.pow(y_delta_4, 2) + math.pow(z_delta_4, 2)) / r_delta_4 + (math.pow(x_delta_1, 2) + math.pow(y_delta_1, 2) + math.pow(z_delta_1, 2)) / r_delta_1

    arr_a = np.array([[a_2, b_2, c_2], [a_3, b_3, c_3], [a_4, b_4, c_4]])
    arr_b = np.array([0 - d_2, 0 - d_2, 0 - d_2])
    solution = np.linalg.solve(arr_a, arr_b)

    '''
    a_3 = np.array([[a_3, b_3, c_3]])
    b_3 = np.array([-d_3])
    solution_3 = np.linalg.lstsq(a_3, b_3)

    a_4 = np.array([[a_4, b_4, c_4]])
    b_4 = np.array([-d_4])
    solution_4 = np.linalg.lstsq(a_4, b_4)
    '''
    print("DELTA VALUES:")
    print("Δr1: ", r_delta_1)
    print("Δr2: ", r_delta_2)
    print("Δr3: ", r_delta_3)
    print("Δr4: ", r_delta_4)
    print("point 0: ", point_0)
    print("point 1: ", point_1)
    print("Δpoint 1: ", point_delta_1)
    print("Δpoint 2: ", point_delta_2)
    print("Δpoint 3: ", point_delta_3)
    print("Δpoint 4: ", point_delta_4)

    print("\nLINEARNI SISTEM:")
    print("a_2: ", a_2)
    print("a_3: ", a_3)
    print("a_4: ", a_4, "\n")

    print("b_2: ", b_2)
    print("b_3: ", b_3)
    print("b_4: ", b_4, "\n")

    print("c_2: ", c_2)
    print("c_3: ", c_3)
    print("c_4: ", c_4, "\n")

    print("d_2: ", d_2)
    print("d_3: ", d_3)
    print("d_4: ", d_4, "\n")

    print("end point: ", solution[0] + point_0)
    return solution[0] + point_0


if __name__ == "__main__":

    # read_data("input0.txt")

    ''' 2) EXAMPLE for 5 points '''
    p0 = np.array([3, 2, 1])
    p1 = np.array([2, 0, -2])
    p2 = np.array([0, 2, 0])
    p3 = np.array([2, 5, 0])
    p4 = np.array([5, 5, 0])
    t0 = 94812.82170000
    t1 = 94812.83085468
    t2 = 94812.82809237
    t3 = 94812.82957627
    t4 = 94812.83199484

    p_avg = np.float64(np.array([0, 0, 0]))
    p_err = 0
    results = []
    sums = []
    points = [p0, p1, p2, p3, p4]
    distances = [t0, t1, t2, t3, t4]

    results.append(trilateration(points, distances))
    print(results)
