import numpy as np
from vehicules_info import can_vehicle_carry_item
from Main_functions import choose_starting_point
# SCOOTER_MAXW, SCOOTER_MAXD = get_max_volume('scooter')
# MINI_VAN_MAXW, MINI_VAN_MAXD = get_max_volume('mini van')
# VAN_MAXW, VAN_MAXD = get_max_volume('van')
ENTROPOT = '152 Rue DD 49, Dakar, Senegal'
route_scooter=[]



def find_closest_unvisited_location(distance_matrix, current_location, visited, UI, locations_mappping, locked_entropot, locked_delivery):
    closest_location = None
    min_distance = float('inf')

    unlocked_unvisted = [item for item in UI if item not in visited]

    for i in unlocked_unvisted:
        distance = distance_matrix[current_location][i]
        if distance < min_distance:
            min_distance = distance
            closest_location = i

    parcelId = locations_mappping[closest_location]
    if parcelId in locked_entropot.keys():

        UI.append(locked_entropot[parcelId])
        locked_entropot.pop(parcelId)
    elif parcelId in locked_delivery.keys():
        UI.append(locked_delivery[parcelId])
        locked_delivery.pop(parcelId)

    return closest_location



def tsp(matrix, start_location, UI, locations_mappping, locked_entropot, locked_delivery, weights_mapping, locations_fit_to_create_DM):
    n = len(matrix)
    total_weight = 0
    for i in UI:
        address = locations_fit_to_create_DM[i]
        pid = locations_mappping[i]
        delivery_idx = locked_delivery[pid]
        distance = matrix[i][delivery_idx]
        if address == ENTROPOT:
            idx=i
            if can_vehicle_carry_item('scooter', distance, weights_mapping[pid]):
            # print(f'distance: {distance} for {pid} ')
            # print(f'wight :{wights_mapping[pid]}')
            # print(f'i the location index: {i} for the adress: {adresse} and the parcelId: {pid}')
                if total_weight <= 10:
                    print(f'a scooter is gonna make the carry {pid} ({weights_mapping[pid]}) for {distance} km')
                    route_scooter.append(delivery_idx)
                    print('level 1')
                    #removing set locations---------------------------------------------
                    locked_delivery.pop(pid)

                    UI.remove(i)
                    n-=1
                    total_weight += weights_mapping[pid]
                else:
                    break
                    #For now we will just break and see how other vihicules will handle the rest of the deliveries
    n-=1
    print('level 2')
    if len(route_scooter) > 0:
        visited_scooter = [idx]
    counter=len(route_scooter)+1
    print('level 3')
    while len(visited_scooter) < counter :
        
        current_location=visited_scooter[-1]
        MD=float('inf')
        for i in route_scooter:
            print('level 4')
            print('current_location: ',current_location)
            print('i: ',i)
            distance = matrix[current_location][i]
            if distance < MD:
                MD = distance
                closest_location = i
        visited_scooter.append(closest_location)
        route_scooter.remove(closest_location)



    print('mochkla houni')

    submatrix = [[matrix[row][col] for col in UI] for row in UI]
    print(f'submatrix: {submatrix} \n') 

    start_location= choose_starting_point(submatrix)
    start_location=UI[start_location]


    visited = [start_location]

        # Add #print statements for debugging
    #print('Before UI update: ', UI)


    # adding the unlock location from the starting point
    #print('locations_mappping',locations_mappping)
    parcelId=locations_mappping[start_location]

    #print('parcelId: ',parcelId)
    if parcelId in locked_entropot.keys():
        UI.append(locked_entropot[parcelId])
        #print('UI: ',UI)
        #print('locked_entropot: ',locked_entropot)
        locked_entropot.pop(parcelId)

    elif parcelId in locked_delivery.keys():
        UI.append(locked_delivery[parcelId])
        locked_delivery.pop(parcelId)
    #print('UI: ',UI)
    print('n: ',n)
    while len(visited) < n:
        current_location = visited[-1]        
        print('visited in TSP : ',visited)
        closest_location = find_closest_unvisited_location(matrix, current_location,
                                                            visited,UI,locations_mappping,
                 locked_entropot,locked_delivery)

        if closest_location is not None:
            visited.append(closest_location)
            current_location = closest_location
        else:
            break
    print('visited aka result: ',visited)
    tsp_routes ={}
    tsp_routes.update({'scooter':visited_scooter})
    tsp_routes.update({'van':visited})
    return tsp_routes












