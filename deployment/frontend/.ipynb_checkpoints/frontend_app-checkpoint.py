import pandas as pd
import requests
# import urllib
import json
# from branca.element import Figure
from sklearn.cluster import KMeans
# from geopy import distance
import streamlit as st
import streamlit.components.v1 as components
# import utils
import routing




########## Title for the Web App ##########
st.title("Logistic Routing")

########## available vehicles##########

available_vehicles = st.number_input("Available Vehicles", min_value=1, max_value=7, value=2, step=1)
sample_daily_order_list = []
vehicle_list = []
sample_daily_order_list_unnested = []

########## upload daily order list ##########

daily_order = st.file_uploader('Upload order_for_today CSV')
if daily_order is not None:
    order_for_today = pd.read_csv(daily_order).drop(['Unnamed: 0'],axis=1)
    sample_daily_order = order_for_today['0'].tolist()
else:
    st.warning('Upload order_for_today CSV')
    
######### cluster button ###########

if st.button('Cluster!'):
    routing.cluster(order_for_today, sample_daily_order, available_vehicles)
    st.write('Clustered!')
    
    
    
# st.write(order_for_today)

########## Route button ##########
if st.button('Generate Overall Routes'):
    sample_daily_order_list, vehicle_list = routing.route(order_for_today, sample_daily_order, available_vehicles)
    HtmlFile = open("../../routes/overall_route.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code,width=900, height=800)
    st.write(vehicle_list)
    ########## location to change cluster ########
    for list in sample_daily_order_list:
        for location in list:
            sample_daily_order_list_unnested.append(location)
            
# with st.form("my_form"):
#     st.write("Re Cluster Location")
#     location_to_change = st.selectbox('Select location to Re Cluster', sorted(set(sample_daily_order_list_unnested)))
#     change_to_cluster = st.number_input("Change to which vehicle cluster?", min_value=0, max_value=available_vehicles-1, value=0, step=1)

    
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write(location_to_change, 're clustered to ', change_to_cluster)




    # to_cluster = st.number_input("Change to which vehicle cluster?", min_value=0, max_value=available_vehicles, value=0, step=1)
    # st.write(to_cluster)
    # location_to_change = st.selectbox('Select location to change', sorted(set(sample_daily_order_list_unnested)))
    # if st.button('Change Cluster'):
    #     routing.change_cluster(to_cluster, location_to_change)

########## route number input field ##########
vehicle_cluster = st.number_input('Vehicle Number', min_value = 0, max_value = int(available_vehicles), value = 1, step = 1)

########## single route button ##########
if st.button('Generate Route for Vehicle number'):
    sample_daily_order_list, vehicle_list = routing.route(order_for_today, sample_daily_order, available_vehicles)
    customer_list = routing.vehicle_cluster(vehicle_cluster, sample_daily_order_list)
    HtmlFile = open("../../routes/single_route.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code,width=900, height=800)
    st.write(customer_list)
    # HtmlFile = open("../../routes/single_route.html", 'r', encoding='utf-8')
    # source_code = HtmlFile.read() 
    # print(source_code)
