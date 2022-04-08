import pandas as pd
import numpy as np
import requests
import folium
import polyline
import urllib
import matplotlib.pyplot as plt
import seaborn as sns
import time
import math
import json
from branca.element import Figure
from sklearn.cluster import KMeans
from geopy import distance



def cluster(order_for_today, sample_daily_order, available_vehicles):
    # vehicle_list = []
    df_lat_lng = pd.read_csv('../../data/df_lat_lng.csv')
    daily_order_df = df_lat_lng[df_lat_lng['Name'].isin(sample_daily_order)]

    X = daily_order_df[['Lat', 'Lng']]

    kmeans = KMeans(n_clusters = available_vehicles, random_state = 42)
    kmeans.fit(X)
    daily_order_df['cluster'] = kmeans.labels_

    daily_order_df.to_csv('../../data/daily_order_df_clustered.csv', index = False)
    
def route(order_for_today, sample_daily_order, available_vehicles):    

    daily_order_df = pd.read_csv('../../data/daily_order_df_clustered.csv')
    df_lat_lng = pd.read_csv('../../data/df_lat_lng.csv')
    sample_daily_order_list = []
    vehicle_list = []
    color_to_csv_list = []
    
    for i in range(available_vehicles):
        sample_daily_order_list.append(daily_order_df[daily_order_df['cluster'] == i]['Name'].tolist())

    depot_url = 'http://localhost:5000/trip/v1/driving/'
    depot_lng = df_lat_lng[df_lat_lng['Name'] == '10 woodlands terrace, singapore']['Lng'].item()
    depot_lat = df_lat_lng[df_lat_lng['Name'] == '10 woodlands terrace, singapore']['Lat'].item()
    depot_loc = f'{depot_lng},{depot_lat};{depot_lng},{depot_lat}'
    r = requests.get(depot_url + depot_loc) 
    # print(f'Status code: {r.status_code}')
    res = r.json()
    depot_hint = res['waypoints'][0]['hint']


    # for x in sample_daily_order_list:
        # setting up folium figure
    fig=Figure(width = 900, height = 500)
    m1 = folium.Map(location = ['1.369528', '103.802410'], zoom_start=11)
    folium.Marker(location=['1.4504311', '103.8059588'],icon=folium.Icon(color='black',icon='none'), tooltip = 'Depot').add_to(m1)

    cluster_number = 0
    color_num = 0
    color_list = ['lightblue', 'darkblue', 'purple', 'green', 'cadetblue', 'orange', 'lightgreen', 'lightred', 'red', 'darkgreen', 'blue', 'gray', 'beige', 'darkpurple', 'pink', 'lightgray', 'darkred']

    # retrieving list from nested list
    for clustered_route in sample_daily_order_list:
        clustered_route.append('10 woodlands terrace, singapore')

    # creating nested list of coordinates for each delivery location
        locations = []
        for location in clustered_route:
            point = []
            point.append(df_lat_lng['Lng'][df_lat_lng['Name'] == location].item())
            point.append(df_lat_lng['Lat'][df_lat_lng['Name'] == location].item())
            locations.append(point)

    # create string to input all locations for api request
        loc = ''
        for i in range(len(locations)):
            if i != (len(locations) - 1):
                loc += f'{locations[i][0]},{locations[i][1]};'
            else:
                loc += f'{locations[i][0]},{locations[i][1]}'

        url = "http://localhost:5000/trip/v1/driving/"

    # api request
        r = requests.get(url + loc) 
        if r.status_code!= 200:
            return {}
        res = r.json()
        res

    # drawing markers for each delivery location
        for i in range(len(res['waypoints'])):

            if res['waypoints'][i]['hint'] != depot_hint:
                lat = res['waypoints'][i]['location'][1]
                lng = res['waypoints'][i]['location'][0]
                folium.Marker(location=[lat, lng],icon=folium.Icon(color=color_list[color_num],icon='none'), tooltip = clustered_route[i]).add_to(m1)        

    # add to folium map
        folium.PolyLine(
            polyline.decode(res['trips'][0]['geometry']),
            weight=8,
            color=color_list[color_num],
            opacity=1
        ).add_to(m1)

        # duration = round((res['trips'][0]['duration']/60),0)
        # duration2 = round((res['trips'][0]['duration']/60),0) * 2
        # duration_min = round(res['trips'][0]['duration'])
        # distance = round((res['trips'][0]['distance'] / 1000),2)
        # duration_distance = round(((res['trips'][0]['distance']/40)*0.06),0)
        
        # all durations in mins, unless specified
        
        duration = round((res['trips'][0]['duration']/60),0)
        distance = round((res['trips'][0]['distance'] / 1000),2)
        duration_distance = round(((res['trips'][0]['distance']/40)*0.06),0)

    # printing of additional details
        route_dict = {}
        
        # display vehicle number
        route_dict['Vehicle'] = cluster_number
        
        # display traveling distance according to OSRM
        printable_distance = str(round(distance)) + 'km'
        route_dict['Distance'] = printable_distance
        
        # display number of locations
        printable_number_of_locations = len(clustered_route)
        route_dict['Number of Locations'] =  len(clustered_route)
        
        # # display traveling duration according to OSRM
        # traveling_duration = (str(int(duration/60)) + 'hrs ' + str(int(duration%60)) + 'mins')
        # route_dict['Traveling Duration'] = traveling_duration
        
        
        # display traveling duration according to distance
        route_dict['Duration by Distance'] = str(int(duration_distance/60)) + 'hrs ' + str(int(duration_distance%60)) + 'mins'
        
        # display traveling duration according to distance plus buffer
        duration_distance = duration_distance + (len(clustered_route)*10)
        route_dict['Duration by Distance + buffer (10 mins per location)'] = str(int(duration_distance/60)) + 'hrs ' + str(int(duration_distance%60)) + 'mins'
    
        # display route color
        route_dict['Color'] = color_list[color_num]
        color_to_csv_list.append(color_list[color_num])
        
        vehicle_list.append(route_dict)

        cluster_number += 1
        color_num += 1

    # saving folium html file
    m1.save(outfile= "../../routes/overall_route.html")
    
    # saving color to csv list for future use
    color_to_csv_df = pd.DataFrame(color_to_csv_list)
    color_to_csv_df.to_csv('../../data/color_to_csv_list.csv')
    
    return sample_daily_order_list, vehicle_list

def vehicle_cluster(vehicle_cluster, sample_daily_order_list):
    df_lat_lng = pd.read_csv('../../data/df_lat_lng.csv')
    depot_url = 'http://localhost:5000/trip/v1/driving/'
    depot_lng = df_lat_lng[df_lat_lng['Name'] == '10 woodlands terrace, singapore']['Lng'].item()
    depot_lat = df_lat_lng[df_lat_lng['Name'] == '10 woodlands terrace, singapore']['Lat'].item()
    depot_loc = f'{depot_lng},{depot_lat};{depot_lng},{depot_lat}'
    r = requests.get(depot_url + depot_loc) 
    # print(f'Status code: {r.status_code}')
    res = r.json()
    depot_hint = res['waypoints'][0]['hint']
    
###################################################
    
    x = vehicle_cluster
    # return sample_daily_order_list
    # local variables
    color_num = x
    color_list = ['lightblue', 'darkblue', 'purple', 'green', 'cadetblue', 'orange', 'lightgreen', 'lightred', 'red', 'darkgreen', 'blue', 'gray', 'beige', 'darkpurple', 'pink', 'lightgray', 'darkred']
    

    z = sample_daily_order_list[x]
    # z.append('10 woodlands terrace, singapore')
    
    locations = []
    for item in z:
        point = []
        point.append(df_lat_lng['Lng'][df_lat_lng['Name'] == item].item())
        point.append(df_lat_lng['Lat'][df_lat_lng['Name'] == item].item())
        locations.append(point)

    loc = ''
    for i in range(len(locations)):
        if i != (len(locations) - 1):
            loc += f'{locations[i][0]},{locations[i][1]};'
        else:
            loc += f'{locations[i][0]},{locations[i][1]}'


    url = "http://localhost:5000/trip/v1/driving/"
    r = requests.get(url + loc) 
    if r.status_code!= 200:
        return {}
    res = r.json()
    res

    fig=Figure(width = 900, height = 700)
    m2 = folium.Map(location = ['1.4504311', '103.8059588'], zoom_start=12)
    folium.Marker(location=['1.4504311', '103.8059588'],icon=folium.Icon(color='black',icon='none'), tooltip = 'Depot').add_to(m2)

    for i in range(len(res['waypoints'])):
        color_list = ['lightblue', 'darkblue', 'purple', 'green', 'cadetblue', 
                                   'white', 'orange', 'lightgreen', 'lightred', 'red', 'darkgreen', 
                                   'blue', 'gray', 'beige', 'darkpurple', 'pink', 'lightgray', 'darkred']

        if res['waypoints'][i]['hint'] != depot_hint:
            lng = res['waypoints'][i]['location'][1]
            lat = res['waypoints'][i]['location'][0]
            folium.Marker(location=[lng, lat],icon=folium.Icon(color=color_list[color_num],icon='none'), tooltip = z[i]).add_to(m2)


    folium.PolyLine(
        polyline.decode(res['trips'][0]['geometry']),
        weight=8,
        color=color_list[color_num],
        opacity=1
    ).add_to(m2)
    
    duration = round((res['trips'][0]['duration']/60),0)
    duration2 = round((res['trips'][0]['duration']/60),0) * 2
    

    print('Vehicle ', x)
    print('Traveling Duration: ', int(duration/60), 'hrs', int(duration%60), 'mins')
    print('Estimated Delivery Duration: ', int(duration2/60), 'hrs', int(duration2%60), 'mins')
    print('Distance: ',(res['trips'][0]['distance'] / 1000), 'km')
    print(color_list[color_num])
    print('---')
    
    m2.save(outfile= "../../routes/single_route.html")

    return sample_daily_order_list[vehicle_cluster]

###################################################

def change_cluster(to_cluster, location_to_change):
    daily_order_df = pd.read_csv('../../data/daily_order_df_clustered.csv')
    st.write(daily_order_df)
    