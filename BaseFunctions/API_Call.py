from flask import Flask, request, jsonify
from Final_algorithm import optimize_delivery_multiple_missions
from flask_cors import CORS
import numpy as np

app = Flask(__name__)

CORS(app, resources={r"/api/v1/runsheet-proposal": {"origins": "*"}})  # Allow all origins for the /api/v1/runsheet-proposal route
CORS(app)  # Enable CORS for all routes
'''        for mission_route,data,google_maps_link_list in zip(mission_route,data,google_maps_link_list):
            i+=1
            runsheet_response.update({
                'status': 'success',
                'code': 200,
                'message': 'Successful operation',
                'data': [
                    {
                        'description': mission_route,
                        'google_maps_link_list': google_maps_link_list,
                        f'Runsheet{i}': data
                    }
                ]
            })'''
@app.route('/api/v1/runsheet-proposal', methods=['POST'])
def make_runsheet():
    try:
        # Get the JSON data from the frontend request
        data_missions = request.get_json()
        # #print(f'data_missions: {data_missions[1]} \n')
        mission_tasks = []
        mission_id=[]
        locations_list = []# list of tuples (action, address, parcelId, parcelVolume)
        entropot_PICKUP_data=[]
        ENTROPOT=False
        entropot_notseen_parcels=[]
        dictionarry_map_PID_RANK={}
        dictionarry_map_PID_action={}
        rank=-1
        runsheet_response={}

        for data in data_missions:
            

            for task in data['tasks']:
                mission_id=data['uid']
                mission_type = data['type']
                # vehicleType=data['vehicleType']
                productType=data['productType']
                # task_action = task['action']
                number_of_stops = len(task['stops'])
                for i in range(number_of_stops):
                    if task['stops'][i]['hub']!=None:
                        action='DELIVERY&PICKUP (ENTROPOT)'
                        ENTROPOT=True
         
    #This isnt an accurate approache since we can have in a mission a single taskp of pickup from hub to distination, WE WILL FIX IT LATER IN FINAL ALGORITHM

                    else:
                        action=task['stops'][i]['action']
                        ENTROPOT=False
    
                    action_address=task['stops'][i]['address']['address']
                    for item in task['stops'][i]['items']:
                        rank+=1
                        try :
                            if parcelId!=item['product']['parcelId']:
                                #We are goinng to intialise some random weights for every diffrenet parcel
                                parcelId=item['product']['parcelId']
                                parcelVolume=np.random.randint(1, 10)
                        except:
                                parcelId=item['product']['parcelId']
                                parcelVolume=np.random.randint(1, 10)


                        # locations_list.append((action, action_address, parcelId, parcelVolume))
                                                # ,task['stops'][i]['items']['parcelVolume']))#can be added once the volume data would be added


                        print((action, action_address, parcelId, parcelVolume))
                        if ENTROPOT==True:
                            

                            
                            if parcelId not in entropot_notseen_parcels:
                                # print(locations_list[-1],rank)
                                entropot_notseen_parcels.append(parcelId)
                                # locations_list.append((action, action_address, parcelId, parcelVolume))
                                #print('we are in entropot')
                                # entropot_PICKUP_data.append(parcelId)
                                print(f'{parcelId } _ {rank }')
                                
                                dictionarry_map_PID_RANK.update({parcelId : rank})

                                task_dict = {
                                    'mission_id': mission_id,
                                    'mission_type': mission_type,
                                    # 'vehicleType': vehicleType,
                                    'productType': productType,
                                    '_id': task['_id'],
                                    'action': task['action'],
                                    'status': task['status'],
                                    'stops_action': task['stops'][i]['action'],
                                    'stops_place_id': task['stops'][i]['address']['place_id'],
                                    'stops_region': task['stops'][i]['address']['region'],
                                    'stops_address': action_address,
                                    'item_product_parcelUid': item['product']['parcelUid'],
                                    'item_product_parcelVolume': parcelVolume,
                                }


                                dictionarry_map_PID_action.update({parcelId : task_dict})


                                print('dictionarry_map_PID_RANK: ',dictionarry_map_PID_RANK)
                            else:
                                entropot_notseen_parcels.remove(parcelId)
                                RANK=dictionarry_map_PID_RANK[parcelId]
                                action='DELIVERY&PICKUP (ENTROPOT)'
                                locations_list.insert(RANK,(action, action_address, parcelId, parcelVolume))


                                print(locations_list[-1],RANK)
                                action='DELIVERY'
                                #print('before insert')
                                mission_tasks.insert(RANK,{
                        'uid': mission_id,
                        'type': mission_type,
                        # 'vehicleType': vehicleType,
                        'productType' : productType,
                        'tasks' : [{

                            '_id': task['_id'],
                            'action': task['action'],
                            'status': task['status'],
                            'stops': [{
                                'action': action,
                                'address':{
                                    'place_id':task['stops'][i]['address']['place_id'],
                                    'region' : task['stops'][i]['address']['region'],
                                    'address':action_address, 
                                        },
                            'items': [
                                {
                                'product':{
                                    'parcelUid':item['product']['parcelUid'],
                                    'parcelVolume':parcelVolume#,
                                }
                                    }
                                    ]
                            }]

                    }]
                    }
                    )
                                #print('post insert')
                                action='PICKUP'
                                entropot_PICKUP_data.insert(RANK,{

                            'uid': mission_id,
                            'type': mission_type,
                            # 'vehicleType': vehicleType,
                            'productType' : productType,
                            'tasks' : [{

                                '_id': task['_id'],
                                'action': task['action'],
                                'status': task['status'],
                                'stops': [{
                                    'action': action,
                                    'address':{
                                        'place_id':task['stops'][i]['address']['place_id'],
                                        'region' : task['stops'][i]['address']['region'],
                                        'address':action_address, 
                                            },
                                'items': [
                                    {
                                    'product':{
                                        'parcelUid':item['product']['parcelUid'],
                                        'parcelVolume':parcelVolume#,
                                    }
                                        }
                                        ]
                                }]

                        }]
                        })
                                break
                        else:
                            
                            locations_list.append((action, action_address, parcelId, parcelVolume))

                            mission_tasks.append({
                        'uid': mission_id,
                        'type': mission_type,
                        # 'vehicleType': vehicleType,
                        'productType' : productType,
                        'tasks' : [{

                            '_id': task['_id'],
                            'action': task['action'],
                            'status': task['status'],
                            'stops': [{
                                'action': action,
                                'address':{
                                    'place_id':task['stops'][i]['address']['place_id'],
                                    'region' : task['stops'][i]['address']['region'],
                                    'address':action_address, 
                                        },
                            'items': [
                                {
                                'product':{
                                    'parcelUid':item['product']['parcelUid'],
                                    'parcelVolume':parcelVolume#,
                                }
                                    }
                                    ]
                            }]

                    }]
                    }
                    

                            )
                            entropot_PICKUP_data.append({'marhbe': 0})
                        print(f'locations_list: {locations_list}  \n\n')

        print('entropot_notseen_parcels: ',entropot_notseen_parcels)
        i=-1
        for pid in entropot_notseen_parcels:
            #print('hello')
            task_dict = dictionarry_map_PID_action.get(pid, {})

            RANK=dictionarry_map_PID_RANK[pid]
            i+=1
            # RANK+=i
            # action_address= '152 Rue DD 49, Dakar, Senegal'
            action_address=locations_list.insert(RANK,(task_dict.get('stops_action'), task_dict.get('stops_address'), pid, task_dict.get('item_product_parcelVolume')))
            print('rank',RANK)


            # Use task_dict to populate mission_tasks
            mission_tasks.insert(RANK, {
                'uid': task_dict.get('mission_id'),
                'type': task_dict.get('mission_type'),
                # 'vehicleType': task_dict.get('vehicleType'),
                'productType': task_dict.get('productType'),
                'tasks': [{
                    '_id': task_dict.get('_id'),
                    'action': task_dict.get('action'),
                    'status': task_dict.get('status'),
                    'stops': [{
                        'action': task_dict.get('stops_action'),
                        'address': {
                            'place_id': task_dict.get('stops_place_id'),
                            'region': task_dict.get('stops_region'),
                            'address': task_dict.get('stops_address'),
                        },
                        'items': [
                            {
                                'product': {
                                    'parcelUid': task_dict.get('item_product_parcelUid'),
                                    'parcelVolume': task_dict.get('item_product_parcelVolume'),
                                }
                            }
                        ]
                    }]
                }]
            })
            entropot_PICKUP_data.insert(RANK,{'marhbe': 0})
            # #print('post insert mission_tasks',mission_tasks)
        #print('entropot_PICKUP_data: ',entropot_PICKUP_data)
        #print('kamalna')
        for element in mission_tasks:
            try:
                if element is not None:
                    address = element.get('tasks', [{}])[0].get('stops', [{}])[0].get('address', {}).get('address')
                    ac= element.get('tasks', [{}])[0].get('stops', [{}])[0].get('action')
                    if address is not None:
                        print( ac , address)
            except :
                print('z')
                continue
        print('kamalna')
        for element in entropot_PICKUP_data:
            try:
                if element !={'marhbe': 0}:
                    address = element.get('tasks', [{}])[0].get('stops', [{}])[0].get('address', {}).get('address')
                    ac= element.get('tasks', [{}])[0].get('stops', [{}])[0].get('action')
                    if address is not None:
                        print( ac , address)
                else:
                    print('vide',element.get('marhbe'))
            except :
                print('vide',element.get('None'))
                continue

        def find_duplicates(lst):
            seen = set()
            duplicates = set()

            for item in lst:
                if item in seen:
                    duplicates.add(item)
                else:
                    seen.add(item)

            return list(duplicates)


        redundant_elements = find_duplicates(locations_list)

        #print("Redundant elements in the list:", redundant_elements)

        # locations_list= list(set(locations_list))
        print(f'length locations_list: {len(locations_list)} \n')
        print(f'length mission_tasks: {len(mission_tasks)} \n')
        print(f'length entropot_PICKUP_data: {len(entropot_PICKUP_data)} \n')
        try:
            vehicleType,mission_route, data_list, google_maps_link_list = optimize_delivery_multiple_missions(locations_list,mission_tasks,entropot_PICKUP_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Pass the list  of stops for this mission
        
        # )

        # optimized_routes.append(mission_route)

        # # Return the optimization results for all missions as a JSON response
        # Combine the data into a single dictionary

        # we are going to add a loop separating different rusheets AKA diffrenet vehicules_roadmaps
        i=0

        runsheet_response = {
            "code": 200,
            "data": []
        }

        for i, (vehicule,mroute, data, google_maps_link) in enumerate(zip(vehicleType,mission_route, data_list, google_maps_link_list), start=1):
            runsheet_response["data"].append({
                'description': mroute,
                'google_maps_link_list': google_maps_link,
                'vehiculeType': vehicule,
                f'Runsheet{i}': data
            })

        runsheet_response.update({
            'status': 'success',
            'message': 'Successful operation'
        })

        # Return a single JSON response
        return jsonify(runsheet_response), 200

    except Exception as e:
        # Handle errors and return an OpenAPI-compliant error response
        error_response = {
            'status': 'error',
            'code': 500,
            'message': str(e)
        }
        return jsonify(error_response), 500

if __name__ == '__main__':
    app.run(debug=True)
