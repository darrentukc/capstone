

<img src="http://imgur.com/1ZcRyrc.png" style="float: left; margin: 20px; height: 55px">

# Capstone Project: Logistics Routing

## Background

Eng Bee Foodstuff Manufacturing Pte Ltd is a company with a history of more than 100 years, handing over the torch from generation to generation. It is, as it's name implies, a food manufacturing company. It mainly produces dried and fresh rice vermicelli, and processed peanuts for traditional chinese snacks.

As Eng Bee Foodstuff is an old company, the workflow has largely remain unchanged.

It employs drivers who are also responsible for sales, as they drive around Singapore looking for new customers and making sure existing customers are taken care off. It is a system that works well for the previous generation. However, as more and more obstacles appear, like staff retention, staff retiring, new generation customers, the old way is unlikely to be the more optimum way.

## Problem Statement

Delivery drivers are not only tasked to ensure deliveries are made, they are also responsible to build rapport with customers. This presents a number of problems.

Customers only come into contact with drivers.

1. As the turnover rate for drivers is high, a new driver every 2 years, customer retention rate may not be as high.
2. Customers may be poached by other companies who may choose to hire driver at a higher salary, resulting in a large loss of customers and revenue.

Similar to driver turn over rate, admin staff turn over rate is high as well.
3. It will take the admin staff around 3 to 6 months to have a grasp of driver routes.
4. A driver may be delivering to a certain customer for a number of years. But, due to unforeseen circumstances, customer may have shifted to another location. This may cause the existing driver to drive in circles, resulting in low efficiency.
5. A driver may fall sick. Without replacement drivers, the workload has to be split among the other drivers.

These issues will need to be resolved by the admin staff, to redistribute the orders to other drivers. From past experience, drivers tend to bully the admin staff, by pushing the responsibilty to other drivers. This results in a toxic working environment for the admin staff.

##### What we plan to do

We plan to make a routing system, which takes in a whole list of daily orders, clusters them and routes them. We will be using KMeans to cluster them according to the number of drivers available that day. This will solve problem 5, 3 and 4.

After clustering with KMeans, a route will be generated for the driver to follow for a more optimum route.

By getting customers to place their orders directly to the company, we will have records of existing customers and their habits. If an attempt is made to poach customers, we try to reverse that. A dedicated salesperson can then handle all their issues. This solves problem 1 and 2.

##### How will success be evaluated?

The success of the model will be assessed based on duration of each delivery. It is calculated by using the distance between each location starting and ending at the factory, with a buffer of 10mins per location for unloading.

Each route should take around the same duration, for an even split of workload.

##### Is the scope of the project appropriate? Who are our important stakeholders and why is this important to investigate?

This model will facilitate Eng Bee Foodstuff in planning the delivery routes and understand customers better. By clustering routes and showing the routes clearly on a map, it will be clearer drivers and admins and lessen any friction between them. New customers can also be added to this list and included in the routes. With this lessened workload for the admin, they will be able to complete other tasks.

## Contents:

1. [Datasets Used](#1.-Datasets-Used)
2. [Data Dictionary](#2.-Data-Dictionary)
3. [APIs Used](#3.-APIs-Used)
4. [NoteBooks](#4.-Notebooks)
5. [Scoring](#5.-Feature-Engineering)
6. [Conclusion](#6.-EDA)

### 1. Datasets Used

The following datasets were used for this projects:

- contacts_compiled_sample.csv
Sample of all customers.

- df_lat_lng
CSV database of customer addresses and coordinates

- distance_array
CSV of distance array between one location and every other location

- daily_order_df_clustered.csv
Clustered CSV, for backend use

- order_for_today
CSV of today's orders


### 2. Data Dictionary

The below is a data dictionary containing all the data features, type and its description:


|Feature|Type|Description|
|---|---|---|
|---|---|---|
|***contacts_compiled_sample.csv***|
|**Name**|*object*|Customer Address.| <br>
|**Given Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Additional Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Family Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Driver**|*object*|Driver allocated to customer, or represents Depot.| <br>
|---|---|---|
|***df_lat_lng.csv***|
|**Name**|*object*|Customer Address.| <br>
|**Given Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Additional Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Family Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Driver**|*object*|Driver allocated to customer, or represents Depot.| <br>
|**Lat**|*float64*|Coordinates Latitude.| <br>
|**Lng**|*float64*|Coordinates Longitude.| <br>
|---|---|---|
|***daily_order_df_clustered.csv***|
|**Name**|*object*|Customer Address.| <br>
|**Given Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Additional Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Family Name**|*object*|Additional info extracted from Google Contacts.| <br>
|**Driver**|*object*|Driver allocated to customer, or represents Depot.| <br>
|**Lat**|*float64*|Coordinates Latitude.| <br>
|**Lng**|*float64*|Coordinates Longitude.| <br>
|**Cluster**|*float64*|Cluster of customer after clustering.| <br>

### 3. APIs Used

#### - Google maps API
Google maps API is used to generate the coordinates for each address. The coordinates will be used later downstream to cluster and route each location.

#### - Open Source Routing Machine (OSRM)
An OSRM is hosted on the local pc to parse all coordinates for the day's locations. The OSRM will return a shortest route, along with distance and duration of route. As this is a NP hard problem, the returned route is only an estimation. However, it is good enough for our use case.

### 4. Notebooks

>#### 1. Cust db get lat lng
>>Here, we get the longitude and latitude of each address from Google Maps API for all existing customers. This database of coordinates will be used further down, instead of sending a request to Google each time a route is generated.
>#### 2. Cust db distance duration
>>After getting the coordinates for each address, a distance matrix is generated with OSRM for each location against every other location.

>#### 3. Cluster Order Input
>>In this notebook, the daily orders are uploaded in a csv file. Then, a new data frame containing the coordinates is created by selecting the locations from df_lat_lng. KMeans clustering will be used, as it is one of the better models to cluster to orders for this particular case. Consideration has been made for other methods like networkx and community detection, but these methods work well with not densely connected nodes. The number of available vehicles is also declared here.

>#### 3b. Route before cluster
>>This notebook takes a list of locations and arranges them in order, starting from the depot.

>#### 4. Routing
>>Orders are retrieved from daily_order_df_clustered and each cluster of locations is used to generate it's own route. These routes are then saved in a folium map.

>#### 4b. Reroute
>>In the event that some vehicles are unable to deliver to certain locations, the address can be reclustered to the next nearest cluster in this notebook.

### 5. Scoring
Scoring of the model is not as straight forward.
For example, driver A has 20 locations and driver B also has 20 locations. If driver A takes 20mins in order to unload the goods for each location, while driver B only takes 2 mins, driver A will always finish later than driver B. In another scenario, if driver A is very hardworking and efficient, and takes 2 mins instead of 20 mins to unload at each location, he will return at the same time as driver B. However, he had to work harder than driver B to finish work at the same time. This will cause some issues that will surface out sooner or later.
With this in mind, we will score our model according to how well it distributes the locations among drivers and the time taken for the route. The time taken will be calculated by taking the distance travelled divided by an average speed of 40km/hr, plus 10 mins buffer for each location. the 10 mins will include time taken ( distance duration + buffer in notebook ) to unload plus any unforeseen traffic conditions.
If there is an unbalance in locations or time taken, the re route function can take any point in a certain cluster and change the cluster number to the nearest other cluster.

### 6. Conclusion

- Recalling our problem statement, there are many issues that Eng Bee Foodstuff is facing, or is foreseen to face in the near future.
- This model not only will help the admin staff in the clustering and routing of the locations, it also ensures that anyone, whether the person has any knowledge of the roads in Singapore, to be able to cluster with relative fairness.  

#### Limitations

- Kmeans is not the best clustering method, as it clusters the locations using eucledian distance, instead of the physical distance. Therefore, human intervention from time to time is still needed.

However, with experienced employees and the re route function, balance can be brought onto the routes. Newer staff can visually see the difference between the routes, and try to balance it out themselves, instead of relying totally on the possibly biased feedback of drivers.

#### Future Improvements
-	Other clustering methods can be applied, such as Minimum Spanning Tree, to better cluster the locations.
- Another method of putting all locations into a single route, and splitting the route into the number of vehicles available may be a good way to solve the problem.
- A future improvement could be to use multiple ways of clustering, such as the 2 methods above, and to manually choose the best route.
- Physical weight of goods and location limitations like time frame, car park height restrictions could be added into the equation for a better route.
