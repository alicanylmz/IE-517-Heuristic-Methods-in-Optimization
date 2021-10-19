# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:08:38 2021

@author: Alican
"""

#Construction Heuristic for G.A.P

# =============================================================================
# Read the data(First instance)

with open('gap-data-3instances.txt') as f:
    all_lines=f.read().splitlines()
    lines_cost=list(range(15,20))
    lines_resource=list(range(21,26))
    line_capacity=27
    resource = []
    cost = []
    capacities=[]
    i, j = [int(x) for x in all_lines[13].split()]
    
    for loc,line in enumerate(all_lines): # read rest of lines
        if loc in lines_cost: 
            cost.append([int(x) for x in line.split()])                            
        if loc in lines_resource: 
            resource.append([int(x) for x in line.split()])    
        if loc==line_capacity:
            capacities=([int(x) for x in line.split()])



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
sorted_dic={k: v for k, v in sorted(resource_dict.items(), key=lambda item: normalized_cost_dic[item[0]]+0.5*normalized_resource_dic[item[0]])}

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
# CONSTRUCTION HEURISTIC 
#1) normalize costi_j and resourcei_j. And sum their values for each (i,j) pair to calculate f_i,j
#2) Assign starting from the smallest f_i,j pair considering the capacity constraint.


for k,v in sorted_dic.copy().items():
  if (remaining_capacity[k[0]-1]>=v) and k[1] not in assigned_job: #checks resource availability and whether selected job is assigned or not
            total_cost+=cost_dict[k] 
            S[k[0]].append(k[1])# adding job to the agent
            remaining_capacity[k[0]-1]-=v #remaining capacity is adjusted
            delete_job_from_dict(k[1]) # delete the assigned job from the dic
            assigned_job.append(k[1])
  else: continue
    
#if sorted_dic is empty then all jobs are assigned.

print("--- %s seconds ---" % (time.time() - start_time))







#THIS PART IS THE SAME. ONLY INSTANCE IS CHANGED.
#Reading
#second instance 
with open('gap-data-3instances.txt') as f:
    all_lines=f.read().splitlines()
    lines_cost=list(range(34,42))
    lines_resource=list(range(43,51))
    line_capacity=52
    resource = []
    cost = []
    capacities=[]
    i, j = [int(x) for x in all_lines[32].split()]
    
    for loc,line in enumerate(all_lines): # read rest of lines
        if loc in lines_cost: 
            cost.append([int(x) for x in line.split()])                            
        if loc in lines_resource: 
            resource.append([int(x) for x in line.split()])    
        if loc==line_capacity:
            capacities=([int(x) for x in line.split()])  
            
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

start_time = time.time()
        
#sort based on norm(cost_i_j)+norm(resource_i_j)

normalized_cost_dic={k:v/max(cost_dict.values()) for k,v in cost_dict.items()} #cost values are normalized
normalized_resource_dic={k:v/max(resource_dict.values()) for k,v in resource_dict.items()} #resource values are normalized

       
# (i,j) pairs are sorted based on f_ij values with best found alpha=0.5
sorted_dic={k: v for k, v in sorted(resource_dict.items(), key=lambda item: normalized_cost_dic[item[0]]+0.3*normalized_resource_dic[item[0]])}

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
# CONSTRUCTION HEURISTIC 
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
print("--- %s seconds ---" % (time.time() - start_time))







#THIS PART IS THE SAME. ONLY INSTANCE IS CHANGED.
#Reading
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
   
        
   
start_time = time.time()    
   
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
# CONSTRUCTION HEURISTIC 
#1) normalize costi_j and resourcei_j. And sum their values for each (i,j) pair to calculate f_i,j
#2) Assign starting from the smallest f_i,j pair considering the capacity constraint.


for k,v in sorted_dic.copy().items(): #here k is job-agent list and v is corresponding resource
  if (remaining_capacity[k[0]-1]>=v) and k[1] not in assigned_job: #checks resource availability 
            total_cost+=cost_dict[k]
            S[k[0]].append(k[1])# adding job to the agent
            remaining_capacity[k[0]-1]-=v #remaining capacity is adjusted
            delete_job_from_dict(k[1]) # delete the assigned job from the dic
            assigned_job.append(k[1])
  else: continue
    
#if sorted_dic is empty then all jobs are assigned.
print("--- %s seconds ---" % (time.time() - start_time))

