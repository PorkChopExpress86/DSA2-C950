from helper import *
from Genetic import *
from Truck import Truck
from Package import Package


def load_truck_easy():
    """Manual loading of the truck packages"""
    truck1.packages = [7, 29, 19, 1, 13, 39, 20, 21, 4, 40, 14, 15, 16, 34]
    truck2.packages = [18, 36, 3, 8, 30, 6, 31, 32, 5, 37, 38, 25, 26]
    truck3.packages = [27, 35, 2, 33, 11, 28, 17, 12, 24, 23, 10, 22, 9]


# Fill hash table
hash_map = fill_hash_table("CSVFiles/packages.csv")

# Create distance matrix
distance_array = create_distance_matrix("CSVFiles/distance_table.csv")

# Create address index
address_index = create_address_dict("CSVFiles/addresses.csv")

# Set up parameters and create truck objects
truck_packages = {}
speed = 18
truck1 = Truck(
    1, speed=speed, location="4001 S700 E", departure_time="08:00:00"
)  # early departure, more time sensitive packages
truck2 = Truck(
    2, speed=speed, location="4001 S700 E", departure_time="09:05:00"
)  # late arrival packages

truck3 = Truck(3, speed=speed, location="4001 S700 E")  # EOD deliveries and left overs

# Load packages in trucks
load_truck_easy()

# print(truck1.packages)
# print(truck2.packages)
# print(truck3.packages)


# Truck 1
truck1_package_indexes = convert_package_id_to_address_index(
    truck1.packages, address_index, hash_map
)

best1, score1 = genetic_algorithm(
    truck1_package_indexes,
    np.asarray(distance_array),
    address_index,
    hash_map,
    truck1,
    return_history=True,
    verbose=False,
)
# Time to complete the route in hours
truck1_total_time = score1 / truck1.speed

truck1.finish_time = truck_finish_time(truck1, score1)

# print(
#     f"The best route for truck 1 is {best1}. \t\nThat will be {score1:.1f} miles. \t\nDeparture: {truck1.departure_time}, finish time: {truck1.finish_time}"
# )

# Truck 2
truck2_package_indexes = convert_package_id_to_address_index(
    truck2.packages, address_index, hash_map
)

best2, score2 = genetic_algorithm(
    truck2_package_indexes,
    np.asarray(distance_array),
    address_index,
    hash_map,
    truck2,
    return_history=True,
    verbose=False,
)
truck2_total_time = score2 / truck2.speed
truck2.finish_time = truck_finish_time(truck2, score2)
# print(
#     f"The best route for truck 2 is {best2}. \t\nThat will be {score2:.1f} miles. \t\nDeparture: {truck2.departure_time}, finish time: {truck2.finish_time}"
# )

# Truck 3
if truck1.finish_time < truck2.finish_time:
    t3_depart = truck1.finish_time
else:
    t3_depart = truck2.finish_time
truck3.departure_time = t3_depart
truck3_package_indexes = convert_package_id_to_address_index(
    truck3.packages, address_index, hash_map
)

best3, score3 = genetic_algorithm(
    truck3_package_indexes,
    np.asarray(distance_array),
    address_index,
    hash_map,
    truck3,
    return_history=True,
    verbose=False,
)

truck3_total_time = score3 / truck3.speed
truck3.finish_time = truck_finish_time(truck3, score3)
# print(
#     f"The best route for truck 3 is {best3}. \t\nThat will be {score3:.1f} miles. \t\nDeparture: {truck3.departure_time}, finish time: {truck3.finish_time}"
# )
total_distance = score1 + score2 + score2
print(f"Total trip disance was {total_distance:.2f}")

# truck1_route_address = convert_address_id_to_address(hash_map, best1, address_index)
# truck2_route_address = convert_address_id_to_address(hash_map, best2, address_index)
# truck3_route_address = convert_address_id_to_address(hash_map, best3, address_index)

# print(
#     f"The best route for truck 1 is {truck1_route_address}. \t\nThat will be {score1} miles."
# )
# print(
#     f"The best route for truck 2 is {truck2_route_address}. \t\nThat will be {score2} miles."
# )
# print(
#     f"The best route for truck 3 is {truck3_route_address}. \t\nThat will be {score3} miles."
# )

distance_mat = np.asarray(distance_array)

truck1_route = delivery_times(truck1, best1, distance_mat, address_index, hash_map)
truck2_route = delivery_times(truck2, best2, distance_mat, address_index, hash_map)
truck3_route = delivery_times(truck3, best3, distance_mat, address_index, hash_map)

print(f"Truck 1: \n{truck1_route}\n")
print(f"Truck 2: \n{truck2_route}\n")
print(f"Truck 3: \n{truck3_route}\n")