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
st.title("Re Cluster Locations")

# importing dataframes from previous notebooks
color_to_csv_df = pd.read_csv('../../data/color_to_csv_list.csv')
daily_order_df_clustered = pd.read_csv('../../data/daily_order_df_clustered.csv')

# settings lists
color_to_csv_list = color_to_csv_df['0'].tolist()
daily_order_df_clustered_list = daily_order_df_clustered['Name'].tolist()

with st.form("my_form"):
    # drop down box to select options
    location_to_change = st.selectbox('Location to re route?', daily_order_df_clustered_list)
    new_cluster_color = st.selectbox('Color of new route?', color_to_csv_list)
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        
        # getting new cluster number from color dropdown box
        new_cluster_number = color_to_csv_df[color_to_csv_df['0'] == new_cluster_color].index.tolist()

        # getting index number from location dropdown box
        location_to_change_index_number = daily_order_df_clustered[daily_order_df_clustered['Name'] == location_to_change].index.tolist()
        
        # overwrite old cluster number
        old_cluster = daily_order_df_clustered.iloc[[location_to_change_index_number[0]], [7]].values.tolist()[0][0]
        
        # print out confirmation
        st.write('Location to re route: ', location_to_change)
        st.write('Old Route: ', color_to_csv_list[old_cluster], str(old_cluster))
        st.write('New Route: ', color_to_csv_list[new_cluster_number[0]], str(new_cluster_number[0]))

        daily_order_df_clustered.iloc[[location_to_change_index_number[0]], [7]] = new_cluster_number

        # saving to new csv
        daily_order_df_clustered.to_csv('../../data/daily_order_df_clustered.csv', index = False)
        
        # print new cluster and color
        # st.write(location_to_change_index_number[0])
        # st.write(daily_order_df_clustered.iloc[[65], [7]])
        
        
        
        # st.write(daily_order_df_clustered[daily_order_df_clustered['Name'] == location_to_change])
        # daily_order_df_clustered[daily_order_df_clustered['Name'] == location_to_change]['cluster'] = new_cluster_number
        # st.write(daily_order_df_clustered[daily_order_df_clustered['Name'] == location_to_change])
        
        
        
        
        
        

