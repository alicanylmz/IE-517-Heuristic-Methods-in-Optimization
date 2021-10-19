#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 13:54:16 2021

@author: alicanyilmaz
"""

import pandas as pd
from numpy.random import choice
import numpy as np
import math 
import time
   
 
path_of_dataset=r'/Users/alicanyilmaz/Desktop/IE517/ie517hw2dataset.xlsx'
first_instance = pd.read_excel(path_of_dataset, sheet_name='first_instance')
second_instance = pd.read_excel(path_of_dataset, sheet_name='second_instance')
third_instance = pd.read_excel(path_of_dataset, sheet_name='third_instance')

instance=third_instance #choose the problem instance. First instance refers to 51 customer, second 76, third 101


p_list=[4,6,8]#number of facilities to be opened for each instance


#Choosing initial locations of facilities randomly

def choose_initial_locs(number_of_facilities):

    init_loc=list(choice(instance["no"], number_of_facilities,replace=False))
    return init_loc

#Calculates distance between two locations
def calculate_euclidean_dist(no1,no2):
    x_1=int(instance.loc[(instance.no==no1),"x_coord"])
    y_1=int(instance.loc[(instance.no==no1),"y_coord"])
    x_2=int(instance.loc[(instance.no==no2),"x_coord"])
    y_2=int(instance.loc[(instance.no==no2),"y_coord"])
    dist=np.sqrt((x_2-x_1)**2+(y_2-y_1)**2)
    dist=np.round(dist,2)
    return dist

def create_distance_matrix():
    distance=np.zeros((len(instance),len(instance)))
    for i in range(len(instance)):
        for j in range(len(instance)):
           d= calculate_euclidean_dist(i+1,j+1)
           distance[i,j]=d
           distance[j,i]=d
    return distance       

distance_matrix=create_distance_matrix()           



#find the total cost given facility locations.
def calculate_cost(facility_locs):
    locs=[i-1 for i in facility_locs]
    cost=0
    for customer in range(1,len(instance)+1):
      cost+=int(instance.loc[(instance.no==customer),"demand"])*min(distance_matrix[customer-1,locs])
    cost=np.round(cost,2)
    return cost  



# removes randomly an existing facility and adds a new facility.      
def one_swap(facility_locs):
    fac_locs=facility_locs.copy()
    location_pool=[i for i in list(instance["no"]) if i not in fac_locs]
    added_loc=int(choice(list(location_pool), 1))
    removed_loc=int(choice(list(fac_locs), 1))
    fac_locs.remove(removed_loc)
    fac_locs.append(added_loc)
    return fac_locs


for output_no in range(10): #Loop for printing the results on excel.(10 run for each each instance)
    for no_of_facility in p_list: # facility number to be opened-
        #Simulated Annealing Heuristic
        start_time = time.time() #to keep track of CPU time of the heuristic 
        
        #STEP 1:Initialization
        
        ip=0.5 #0.1,0.3,0.5,0.7
        r=0.9 #0.85, 0.9,0.95
        sf=0.5 #0.5,1,5
        fp=0.01 #0.01,0.02,0.05
        T=100000 # select initially large temperature
        p=no_of_facility#number of new facilitiyies to be opened
        S=choose_initial_locs(p) #(p=4)
        initial_locations=S
        cost_S=calculate_cost(S)#initial cost
        best_cost=cost_S #initially best cost equals initial cost
        incumbent_S=S #initially incumbent sol. equals best sol.
        terct=0 # counter for stopping condition. If that reaches 5, it stops.
        L=sf*p*(len(instance)-p) # number of iterations equals sf times neighbor size
        epoch_no=0 #used to find total number of iteration in a run
        #STEP 2:         
        while terct<5:
            j=0 # used as counter, solution is updated.
            for i in range(int(L)): #iterate over L times 
                S_n=one_swap(S) #get neighbor solution with 1-swap operation
                cost_S=calculate_cost(S)
                cost_S_n=calculate_cost(S_n) #calculates the cost of neighbor
                delta=cost_S_n-cost_S #Computes the difference of objectives
                if delta <=0:
                    S=S_n #update current solution            
                    if cost_S_n<best_cost:
                        best_cost=cost_S_n #update best cost
                        incumbent_S=S_n #update incumbent sol
                    j=j+1
                elif delta >0:
                    X=float(np.random.uniform(0,1,1))
                    if math.exp((-delta)/T)>X: #update current solution with probability
                      S=S_n 
                      j=j+1  
        #STEP 2-1 decrease the temperature
            if j/L<=fp:
                terct+=1
            if j/L>fp:
                terct=0
            if j/L>ip:
                T=T/2
                epoch_no+=1
            if j/L<=ip:
                T=r*T
                epoch_no+=1
            
            #end the while loop if time limit exceeds 10 minutes
            if (time.time() - start_time)>=60*10:
                break
            print("j=",j,"j/L=",j/L,"Temperature=",T,"terct=",terct,"best cost so far=",best_cost)
        print("optimal cost=",best_cost,"optimal solution=",incumbent_S)    #get the best objective and best solution
        print("number of iterations=",L*epoch_no)  
        print("initial locations=",initial_locations)              
        print("--- %s seconds ---" % (time.time() - start_time))  
        
        #export output as csv
        output={"Solution":incumbent_S,"obj. value":best_cost,"number of iterations":L*epoch_no,"CPU time":(time.time() - start_time),"initial locations":initial_locations}          
        df=pd.DataFrame(output)
        df.to_excel("/Users/alicanyilmaz/Desktop/SA_101/output_{}{}.xlsx".format(output_no,p), index = False, header=True,sheet_name="2p{}".format(p))#1p4 means first instance 4 facilities




