#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 12:23:39 2021

@author: alicanyilmaz
"""


import pandas as pd
from numpy.random import choice
import numpy as np
import time
    

path_of_dataset=r'/Users/alicanyilmaz/Desktop/IE517/ie517hw2dataset.xlsx'
first_instance = pd.read_excel(path_of_dataset, sheet_name='first_instance')
second_instance = pd.read_excel(path_of_dataset, sheet_name='second_instance')
third_instance = pd.read_excel(path_of_dataset, sheet_name='third_instance')

instance=third_instance #choose the problem instance



p_list=[4,6,8]#number of facilities to be opened for each instance


######### HELPER FUNCTIONS ################

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

# removes randomly  existing k facility and adds  new k facility.      


def k_swap(facility_locs,k):
    fac_locs=facility_locs.copy()
    if k==1:
        location_pool=[i for i in list(instance["no"]) if i not in fac_locs]
        added_loc=int(choice(list(location_pool), 1))
        removed_loc=int(choice(list(fac_locs), 1))
        fac_locs.remove(removed_loc)
        fac_locs.append(added_loc)
        return fac_locs

    elif k==2:
        location_pool=[i for i in list(instance["no"]) if i not in fac_locs]
        added_locs=list(choice(list(location_pool), 2,replace=False))
        removed_locs=list(choice(list(fac_locs), 2,replace=False))
        for r in removed_locs:
            fac_locs.remove(r)
        for a in added_locs:
            fac_locs.append(a)
        return fac_locs
    
    elif k==3:
        location_pool=[i for i in list(instance["no"]) if i not in fac_locs]
        added_locs=list(choice(list(location_pool), 3,replace=False))
        removed_locs=list(choice(list(fac_locs), 3,replace=False))
        for r in removed_locs:
            fac_locs.remove(r)
        for a in added_locs:
            fac_locs.append(a)
        return fac_locs
        
def swap_local_search(facility_locs,old_loc,new_loc): #takes the current facility locs, location of the facility and new loc. of the facility as argument        
      fac_locs=facility_locs.copy()
      fac_locs.remove(old_loc) 
      fac_locs.append(new_loc)
      return fac_locs
#########################


###### Initial locations are the same with SA initial locations. ######
i=0
#init_locs=[[14,16,32,24],[51,40,34,9],[10,21,51,40],[48,7,15,10],[35,36,6,2],[11,48,34,50],[6,18,14,31],[28,37,12,47],[13,22,41,42],[16,5,8,25],[3,26,46,50,11,43],[49,11,27,33,25,47],[7,18,3,12,4,11],[21,28,6,47,5,2],[3,9,7,20,35,12],[30,8,39,10,50,42],[43,45,11,17,16,44],[17,4,47,9,6,21],[7,33,51,32,38,44],[41,6,35,15,48,37],[28,26,50,25,23,2,47,39],[10,40,25,30,43,32,7,1],[7,39,42,24,48,18,38,23],[30,29,47,21,20,45,2,13],[46,15,20,31,39,42,2,22],[21,20,32,24,44,5,35,47],[32,13,9,27,21,33,23,47],[40,45,1,38,28,41,31,35],[40,19,50,43,32,23,15,20],[17,19,30,37,48,23,8,21]]
#init_locs=[[54,24,32,3],[49,5,66,73],[20,67,55,66],[1,44,66,41],[29,59,63,46],[64,24,74,41],[56,59,76,72],[14,34,67,39],[24,76,6,37],[43,31,38,74],[66,54,21,9,12,56],[5,65,23,48,30,42],[24,28,31,30,61,36],[19,49,9,39,2,62],[33,50,3,6,72,23],[29,17,48,30,10,8],[21,55,69,38,67,33],[47,75,9,55,32,65],[46,31,9,47,67,40],[2,9,76,39,10,65],[40,48,14,74,6,41,38,17],[7,22,18,58,40,24,35,46],[47,54,6,13,45,18,59,41],[56,76,21,60,14,49,38,6],[73,43,54,5,62,4,59,29],[60,21,54,7,20,64,22,33],[47,9,54,39,11,59,56,3],[10,33,7,17,72,52,5,40],[18,8,33,55,37,61,69,23],[40,75,72,52,31,43,56,36]]
init_locs=[[95,28,16,83],[37,55,96,95],[67,29,45,42],[49,6,15,14],[15,66,6,73],[95,92,16,71],[42,65,41,21],[19,63,97,100],[26,7,78,47],[75,92,6,100],[67,78,62,44,31,72],[7,99,49,98,95,27],[95,9,36,52,14,23],[25,8,34,45,48,84],[65,58,73,3,96,64],[81,23,67,1,4,45],[43,17,3,46,89,29],[32,25,34,100,67,10],[86,82,20,23,28,4],[46,58,7,79,18,89],[50,58,23,96,61,7,51,5],[84,28,55,101,39,65,91,70],[34,54,41,101,70,99,45,72],[80,73,71,52,81,54,100,49],[58,1,36,16,95,53,9,5],[53,68,72,97,86,81,48,18],[92,27,84,47,77,97,76,22],[48,51,65,8,38,79,7,24],[12,43,19,2,18,37,26,98],[82,8,3,58,92,32,50,67]]
for no_of_facility in p_list: # this is used to excel writing
    for output_no in range(10): #this is used to excel writing
        
        #VNS Heuristic
        start_time = time.time() #to keep track of CPU time of the heuristic 
        
        #step 1:INITIALIZATION
        p=no_of_facility#number of new facilities to be opened(4-6-8)
        S=init_locs[i] #current locations
        initial_locations=S #initial locations
        cost_S=calculate_cost(S)#initial cost
        best_cost=cost_S #initially best cost equals initial cost
        k_max=3 # at most 3 neighbor structure
        nu_of_iterations=0 #keep track of number of iterations.
        i+=1 
        
######### START OF THE VNS ################        
        while (time.time() - start_time)<=60*5: #end the heuristic when the time limit is passed
            k=1 # initially first neighborhood is used    
            while k <= k_max:
                print("k=",k,"best_cost=",best_cost,"incumbent_s=",S)
                nu_of_iterations+=1 #needed for output table
                #SHAKING
                S_n=k_swap(S,k)
                
                #LOCAL SEARCH(1-swap is used for local search)
                potential_locs=[i for i in list(instance["no"]) if i not in S_n]
                cost_S_n_n=[] #keep track of all neigbor costs
                S_n_n_locs=[] #keep track of all neighbors
                for floc in S_n:#scan all the 1-swap neighbors of S_n
                    for new_loc in potential_locs:
                       S_n_n=swap_local_search(S_n,floc,new_loc) 
                       S_n_n_locs.append(S_n_n) 
                       cost_S_n_n.append(calculate_cost(S_n_n))
                if min(cost_S_n_n)< best_cost: #local optimum condition
                    S=S_n_n_locs[cost_S_n_n.index(min(cost_S_n_n))]#update the current/optimal solution
                    best_cost=min(cost_S_n_n) #update the best cost
                    k=1  #initialize the neighborhood structure
                else:
                    k+=1 #update  the neighborhood structure
########### END OF THE VNS
                 
        #export output as csv
        output={"Solution":S,"obj. value":best_cost,"number of iterations":nu_of_iterations,"CPU time":(time.time() - start_time),"initial locations":initial_locations}          
        df=pd.DataFrame(output)
        df.to_excel("/Users/alicanyilmaz/Desktop/VNS_101/output_{}{}.xlsx".format(output_no,p), index = False, header=True,sheet_name="1p{}".format(p))        
        
          



