import numpy as np
def get_max_WEIGHTS_DISTANCES(vehicle_type):
    # Define maximum volumes for different vehicle types
    '''
         - scooter: Pour les articles de taille moyenne et pour une courte distance(-10 Kg)
         - van : Pour les articles lourds et pour une courte distance(-30 Kg)
         - mini van: Pour les articles lourds et pour une longue/courte distance(-30 Kg)
         - camion: Pour les articles lourds et NOMBREUX et pour une longue distance(-50 Kg)
    '''
    max_weights = {#Kg
        'scooter': 10,
        'mini van': 30,
        'van': 30,
        # VAN AND MINI VAN SERVE THE SAME PURPOSE, WE'LL USE THE SAME WEIGHTS AND LET THE CLIENT DECIDE BASED ON THE AVAILABILITY
        'camion':50
    }
    max_distance ={
        'scooter': 20,
        'van': 50,
        'mini van': 100,
        'camion': np.abs(float('inf'))
    }

    # Convert vehicle type to lowercase for case-insensitive matching
    vehicle_type_lower = vehicle_type.lower()

    # Use get method to retrieve the max volume for the given vehicle type
    max_volume = max_weights.get(vehicle_type_lower)
    max_distance = max_distance.get(vehicle_type_lower)

    if max_volume is not None:
        print( f"The maximum volume for '{vehicle_type}' is: {max_volume} L.")
    else:
        print( f"Volume information not available for '{vehicle_type}'.")
    return max_volume,max_distance

def can_vehicle_carry_item(vehicule, distance, volume):

    vehicule_MAXW,vehicule_MAXD = get_max_WEIGHTS_DISTANCES(vehicule)

    if volume > vehicule_MAXW:
        print(f"Item with volume {volume} L cannot be carried by a {vehicule_MAXW} L vehicle.")
        return False
    if distance > vehicule_MAXD:
        print(f"Item with distance {distance} L cannot be carried by a {vehicule_MAXD} L vehicle.")
        return False
    return True


# Example usage
vehicle_type = 'scooter'
result = get_max_WEIGHTS_DISTANCES(vehicle_type)
print(result)
