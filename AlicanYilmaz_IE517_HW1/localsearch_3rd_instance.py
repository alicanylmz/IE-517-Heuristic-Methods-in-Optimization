#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:59:30 2021

@author: alicanyilmaz
"""

# third instance
with open('gap-data-3instances.txt') as f:
    all_lines=f.read().splitlines()
    lines_cost=list(range(59,69))
    lines_resource=list(range(70,80))
    line_capacity=81
    resource = []
    cost = []
    capacities=[]
    i, j = [int(x) for x in all_lines[57].split()]
    
    for loc,line in enumerate(all_lines): # read rest of lines
        if loc in lines_cost: 
            cost.append([int(x) for x in line.split()])                            
        if loc in lines_resource: 
            resource.append([int(x) for x in line.split()])    
        if loc==line_capacity:
            capacities=([int(x) for x in line.split()])    

# =============================================================================
#PARAMETERS ARE DEFINED
         
Nu_of_agents=i 
Nu_of_jobs=j
cost_matrix=cost         #rows are agent,columns are jobs
resource_matrix=resource #rows are agent,columns are jobs
capacity=capacities      #capacities of agents


#Resources and cost parameters are stored  as dictionaries for ease of implementation
resource_dict={}
for k in range(1,i+1):
    for l in range(1,j+1):
        resource_dict[(k,l)]=resource_matrix[k-1][l-1]
cost_dict={}
for k in range(1,i+1):
    for l in range(1,j+1):
        cost_dict[(k,l)]=cost_matrix[k-1][l-1]
        
import time       
start_time = time.time() #to keep track of CPU time of the heuristic        
#sort based on norm(cost_i_j)+norm(resource_i_j)

normalized_cost_dic={k:v/max(cost_dict.values()) for k,v in cost_dict.items()} #cost values are normalized
normalized_resource_dic={k:v/max(resource_dict.values()) for k,v in resource_dict.items()} #resource values are normalized

       
# (i,j) pairs are sorted based on f_ij values with best found alpha=0.5
sorted_dic={k: v for k, v in sorted(resource_dict.items(), key=lambda item: normalized_cost_dic[item[0]]+0.2*normalized_resource_dic[item[0]])}

#initialization of remaining capacity
remaining_capacity=capacities.copy()

#Initialization of assigned jobs for each agent. Initially empty.
S={agent:[] for agent in range(1,i+1)}

#deleting job from the dic. This function is used to check whether any job remained unassigned at the end of the heuristic.
def delete_job_from_dict(j):
  for k,v in sorted_dic.copy().items():
      if k[1]==j:
       del sorted_dic[k]
            
            

assigned_job=[]  #initialization  
total_cost=0     #initialization   

# =============================================================================
# CONSTRUCTION HEURISTIC(PHASE-1) 
#1) normalize costi_j and resourcei_j. And sum their values for each (i,j) pair to calculate f_i,j
#2) Assign starting from the smallest f_i,j pair considering the capacity constraint.


for k,v in sorted_dic.copy().items():
  if (remaining_capacity[k[0]-1]>=v) and k[1] not in assigned_job: #checks resource availability 
            total_cost+=cost_dict[k]
            S[k[0]].append(k[1])# adding job to the agent
            remaining_capacity[k[0]-1]-=v #remaining capacity is adjusted
            delete_job_from_dict(k[1]) # delete the assigned job from the dic
            assigned_job.append(k[1])
  else: continue
    
#if sorted_dic is empty then all jobs are assigned.







# =============================================================================
#LOCAL SEARCH(PHASE-2)
#First necessary functions are defined.

import copy

  
# This function swaps agents of job i and job j and returns the new swapped solution.
def swap_jobs(i,j,dic):
    copy_dic=copy.deepcopy(dic)
    m1=None
    m3=None  

    for m,k in copy.deepcopy(copy_dic).items():
        for a in range(0,len(k)):
            x=k[a] 
            if x==i:
                m1=m
                copy_dic[m].remove(i)
            if x==j:
                m3=m
    copy_dic[m3].remove(j)            
    copy_dic[m1].append(j) 
    copy_dic[m3].append(i)
    return(copy_dic)    

# This function calculates the cost of the solution given and returns it.
def calculate_cost(dic):
    cost_total=0
    for i,j in dic.items():
        for k in j:    
            cost_total+=cost_dict[(i,k)]
    return(cost_total)
# This functions returns False if capacity constraint is violated and returns True if capacity is not violated,i.e. solution is feasible.
def check_capacity(dic):
    for i,j in dic.items():
        total_capacity=0
        for k in j:
               total_capacity+=resource_dict[(i,k)] 
        if total_capacity>capacities[i-1]:
           return(False)
        else: continue
    return(True)     


#Initializations and Improvement
best_cost=total_cost #initialization(best cost is equal the cost of the solution obtained from construction heuristic)
current_agent_job_assignment=copy.deepcopy(S) #initialization
incumbent_soln=copy.deepcopy(current_agent_job_assignment) #refers to current best solution
flag=1 #used to start while loop. 
#As long as an improved solution is found in the neighbourhood space, flag equals=1,otherwise flag=0 and loop is ended at that solution,i.e. none of the neighbours are better.
while(flag==1):
    flag=0
    #searching in neighbourhood space
    for i in range(1,Nu_of_jobs+1):
        for j in range(i+1,Nu_of_jobs+1):
           neighbour_agent_job_assignment=swap_jobs(i,j,current_agent_job_assignment)#assign neighborhood solution
           cost=calculate_cost(neighbour_agent_job_assignment) #calculate the cost of neighborhood solution
           if cost<best_cost and bool(check_capacity(neighbour_agent_job_assignment)): #check if neighborhood solution is better and feasible.
               best_cost=cost  #update best cost   
               incumbent_soln=copy.deepcopy(neighbour_agent_job_assignment) #update incumbent solution
               flag=1 #stay in the loop
    current_agent_job_assignment=copy.deepcopy(incumbent_soln)  #update the current solution with incumbent solution
    print(incumbent_soln,best_cost) #helps to keep track of swapped jobs and improved costs at each iteration 

print("--- %s seconds ---" % (time.time() - start_time))