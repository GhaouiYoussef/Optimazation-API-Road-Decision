from Main_functions  import seconds_to_hms  ,split_route,get_route_distances    ,generate_google_maps_link  ,calculate_total_distance   ,choose_starting_point,         combine_consecutive_occurrences
from Tsp_modified import tsp 


def optimize_delivery_multiple_missions(locations_list,mission_tasks, entropot_data,GOOGLE_MAPS_API_KEY='AIzaSyAgaRnl5RlSg1bX79_CH3E3xchf_bgA6Gw',):#AIzaSyAgaRnl5RlSg1bX79_CH3E3xchf_bgA6Gw
    # return None
    print('Execuating optimize_delivery_multiple_missions')
    results = []
    locations_fit_to_create_DM=[]
    locations_mappping={}#{location_index:parcelId}
    pickups_mappping={}#{parcelId:location_index}
    locked_entropot={}#{parcelId:location_index}
    locked_delivery={}#{parcelId:location_index}
    wights_mapping={}#{parcelId:weight}
    UI=[]
    vehicleType=[]
    Data_list=[]
    google_maps_link_list_all=[]
    '''
            The concept:
            - when the location i is set as the next location to visit, we will check the corresponding parcelId to that location
            - if the parcelId in the dicinnary 'locked_entropot' , exist, the we unloack the corresponding location_index and added it to U,if not(DOESNT EXIST), we ignore it and strat corrresponding to locked_delivery dict , if it exist we unlock the corresponding location_index and added it to U
            - if added or not we will rerun the solution to our TSP problem
    
    '''
    print('locations_list: ',locations_list)
    for i,element in enumerate (locations_list):
        #[(action1, address1, parcelId1),...,(actionn, addressn, parcelIdn)]
        #action in ['PICKUP','DELIVERY','ENTREPOT']

        locations_fit_to_create_DM.append(element[1])#we add adresses only to the list of locations_fit_to_create_DM
        locations_mappping.update({i:element[2]})# we map index of location to parcelId
        wights_mapping.update({element[2]: element[3]})# we map index of location to parcelId

        ##print(f'parcelID: {element[0]} \n')
        if element[0]=='PICKUP':
            '''
            UI: Unlocked locations Index
            the UI will play a huge role in setting the unlocked matrix
            '''

            UI.append(i)#the pickups are always unlocked in the begining
            pickups_mappping.update({element[2]:i})# we map index of location to parcelId
        elif element[0]=='DELIVERY&PICKUP (ENTROPOT)':
            ##print(f'ENTROPOT: {element[2]} \n')
            ##print(f'ENTROPOT: {i} \n')  
            locked_entropot.update({element[2]:i})# we map parcelId to index of location
            ##print('locked_entropot pre: ',locked_entropot)


        else:#element[0]=='DELIVERY'
            locked_delivery.update({element[2]:i})# we map parcelId to index of location
 
 #-------------------------------------------------------------------------------------------------------------
    '''#FIXING THE PROBLEM OF THE SINGLE PICKUP FROM HUB TO DISTINATION
    locked_delivery_keys = set(locked_delivery.keys())
    pickups_mapping_values = set(pickups_mappping.keys())

    # Check if all values in locked_delivery exist in pickups_mapping keys
    if not(locked_delivery_keys.issubset(pickups_mapping_values)):
        ##print('we have a single pickup from hub to distination')
        # If not, then we have a single pickup from hub to distination
        # Find values in locked_delivery that do not exist in pickups_mapping keys
        values_not_in_pickups_mapping = locked_delivery_keys - pickups_mapping_values
        # Convert the set of values to a list if needed
        values_not_in_pickups_mapping_list = list(values_not_in_pickups_mapping)
        ##print(f'values_not_in_pickups_mapping_list: {values_not_in_pickups_mapping_list} \n')
        for parcelid in values_not_in_pickups_mapping_list:
        # Check if the value has a corresponding key in locked_entropot
            if parcelid in locked_entropot.keys():
                # Update pickups_mapping with the key-value pair
                index=locked_entropot[parcelid]
                UI.append(index)
                #for a better view of the solution
                ##print(f'locations_list[index][0]: {locations_list[index][0]} \n')
                locations_list[index]=list(locations_list[index])
                locations_list[index][0]='PICKUP'
                locations_list[index]=tuple(locations_list[index])

                # Remove the key from locked_entropot
                locked_entropot.pop(parcelid)
                
'''





    ##print(f'UI: {UI} \n')
    ##print(f'locations_mappping: {locations_mappping} \n')
    ##print(f'pickups_mappping: {pickups_mappping} \n')
    ##print(f'locked_entropot: {locked_entropot} \n')
    ##print(f'locked_delivery: {locked_delivery} \n')
    ##print(f'locations_fit_to_create_DM: {locations_fit_to_create_DM} \n')

    # Créer une contrainte d'ordre pour les emplacements de ramassage et de livraison
    # order_constraint,locations = create_order_constraint(Pickup_locations,Delivery_locations)

    # index_to_location = {i: loc for i, loc in enumerate(locations)}
    # ##print(f'index_to_location {index_to_location} \n')
    # Obtenir la matrice des distances entre les emplacements
    distance_matrix  = get_route_distances(locations_fit_to_create_DM, GOOGLE_MAPS_API_KEY)
    
    # Test for API-GMPAS
    try:
        
        print( f'distance_matrix {distance_matrix }\n ' )
    except:
        print("distance_matrix not found! \n")
    e_copy=locked_entropot.copy()
 
    # Résoudre le problème du voyageur de commerce (TSP) avec des véhicules
    submatrix = [[distance_matrix[row][col] for col in UI] for row in UI]
    print(f'submatrix: {submatrix} \n') 

    start_location= choose_starting_point(submatrix)
    start_location=UI[start_location]

    ##print(f'start_location: {start_location} \n')
    # print(f'UI: {UI} \n')
    # print(f'locations_mappping: {locations_mappping} \n')
    # print(f'locked_entropot: {locked_entropot} \n')
    # print(f'locked_delivery: {locked_delivery} \n')
    tsp_routes = tsp(distance_matrix,start_location,UI,locations_mappping,
                 locked_entropot,locked_delivery,wights_mapping ,
                 locations_fit_to_create_DM)#default value  
    ##print(f'route: {routes} \n')


    '''
    # no optimzation solution
    routes=[0,10,1,11,2,12,3,13,4,14,5,15,6,16,7,17,8,18,9,19]
    ##print(f'NON OPTIMIZED   route: {routes} \n')
    '''
    for routes_key in tsp_routes:
        Data=[]
        vehicleType.append(routes_key.upper())
        print('We are back to Final_algorithm.py')
        result = ""
        print('routes: ',tsp_routes[routes_key])
        print('locations_fit_to_create_DM: ',locations_fit_to_create_DM)
        if tsp_routes[routes_key]:
            total_distance= calculate_total_distance(distance_matrix, tsp_routes[routes_key])



            #-------------------------------------------------------------------------------------------------------------
            #set the corresponding locations to the routes
            route_names = [locations_fit_to_create_DM[loc_idx] for loc_idx in tsp_routes[routes_key]]

            ##print(f'route_names: {route_names} \n')

            #ADDING DOUBLE HUB MISSION TO THE CORRESPONDANCE WITH mission_tasks
            print(f'e_copy: {e_copy} \n')
            for loc_idx in tsp_routes[routes_key]:
                # print(e_copy   )
                # print(Data)

                if loc_idx in e_copy.values():
                    # print('loc_idx: ',loc_idx   )
                    # print(mission_tasks[loc_idx])
                    Data.append(mission_tasks[loc_idx])
                    # print(entropot_data[loc_idx])
                    Data.append(entropot_data[loc_idx])
                else:
                    Data.append(mission_tasks[loc_idx])
            # Data = [mission_tasks[loc_idx] for loc_idx in routes]
            # ##print(f'route_names: {route_names} \n')



            #gey the google maps link for the route
            final_route_name=combine_consecutive_occurrences(route_names)
            if len(final_route_name)>25:#on the assumtion that we will never need more than 50 locations, but that case we just use %len(final_route_name)
                    google_maps_link_list = {}
                    google_maps_link_list['Etape 1'] = generate_google_maps_link(final_route_name[:len(final_route_name)])
                    google_maps_link_list['Etape 2'] = generate_google_maps_link(final_route_name[len(final_route_name):])

                    # google_maps_link_list.append(google_maps_link)
            else:
                google_maps_link_list = []
                google_maps_link = generate_google_maps_link(final_route_name)
                google_maps_link_list.append(google_maps_link)
            result += f"Optimal route for {routes_key}: {' --> '.join(final_route_name)} <br>"
            result += f"Total distance : {total_distance:.2f} kilometers <br> <br>"

        else:
            result = "No solution found."

        results.append(result)
        Data_list.append(Data)
        google_maps_link_list_all.append(google_maps_link_list)
        print(f'fin boucle {routes_key}')
            
    return vehicleType,results,Data_list,google_maps_link_list_all
