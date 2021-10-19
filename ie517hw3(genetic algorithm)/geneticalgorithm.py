#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 13:31:09 2021

@author: alicanyilmaz
"""

#Genetic algorithm 



import openpyxl
import numpy as np
import pandas as pd
import random as rand
from numpy.random import choice 
import time

# =============================================================================
#READING DATA

#Change "1_st instance" to "2nd_istance or to "3rd_instance", and usecols=("B:F") to obtain
#second and third dataset.


wb = openpyxl.load_workbook("ie517hw3.xlsx")


Job_Number = wb['1st_instance']['B1'].value #get job no
machine_number = wb['1st_instance']['D1'].value #get machine no

p_j_i=pd.read_excel("ie517hw3.xlsx",sheet_name="1st_instance",usecols=("B:E"),skiprows=(1)) #read process time as df


# =============================================================================






## HELPER FUNCTIONS

sorted_population=[]
#This function calculates makespan given job order in a recursive manner. 
def F_j_i(j_index,i,job_order):
    #initial conditions. We have discontuinity at first machine and first job
    
    j=job_order[j_index] #corresponding job
    
    #job before the last job, job_before_j=job_order[j_index-1]
    if i==1 and j_index>=1: #first machine's makespan 
        job_before_j=j_index-1   

        return F_j_i(job_before_j,1,job_order)+p_j_i.loc[j][1]
    
   

    if j_index==0: #first job's makespan at machine i
        sum_=0
        for k in range(1,i+1):
          sum_+=  p_j_i.loc[j][k]
        return sum_
    
    job_before_j=j_index-1   

    return max(F_j_i(j_index,i-1,job_order),F_j_i(job_before_j,i,job_order))+p_j_i.loc[j,i]#makespan equals starting time of the last job of the last machine + its processing time
  


#applies 1-point crossover to parents to obtain  new child.
def cross_over(parent1,parent2): 
    cross_over_point=rand.choice(range(1,Job_Number))
    child=[parent1[i] for i in range(cross_over_point)]
    for i in parent2:
        if i not in child:
            child.append(i)
    return child

#shift mutation
def mutate(child):
    child_copy=child.copy()
    element=rand.choice(range(Job_Number))
    child_copy.remove(element)
    new_loc=rand.choice(range(Job_Number))
    child_copy.insert(new_loc,element)
    return child_copy

#population generation
def generate_pop(N_pop):
    population=[]
    for i in range(N_pop):
        population.append(list(np.random.permutation(Job_Number)))
    return population

#Selection
def select_parent_fitness_rank_dist(population):
    probability=[2*i/(N_pop*(N_pop+1)) for i in range(1,N_pop+1)]
    population_objectives=[]
    for solution in population:
        population_objectives.append(F_j_i(Job_Number-1,machine_number,solution))
        
    global sorted_population
    sorted_population=[x for _, x in sorted(zip(population_objectives,population),reverse=True)]
    parents=[]
    for i in range(len(population)):
        parent_indexes=list(choice(len(sorted_population), 2, p=probability,replace=False))
        couple=[]
        for j in parent_indexes:            
            couple.append(sorted_population[j])
        parents.append(couple)
    return parents

#population update
def Elitist_strategy(old_pop,new_pop):
    new_pop.remove(new_pop[rand.randint(0,len(new_pop)-1)]) #randomly remove one and add the best of previous
    global sorted_population
    new_pop.append(sorted_population[N_pop-1])
    return new_pop

def calculate_statistics(population):

    population_objectives=[]
    for solution in population:
        population_objectives.append(F_j_i(Job_Number-1,machine_number,solution))
    best_obj=min(population_objectives)
    best_solution=population[population_objectives.index(best_obj)]
    average_of_objectives=np.mean(population_objectives)
    
    
    return(best_obj,best_solution,average_of_objectives)

#GENETIC ALGORITHM
start_time = time.time() #to keep track of CPU time of the heuristic
#set parameters
N_pop=4
P_c=1
P_m=1

stopping_time=60*5 #stopping time is 5 minutes

#initialization
population=generate_pop(N_pop)
best_obj,best_solution,average_of_objectives=calculate_statistics(population)

generation=0
while(time.time() - start_time)<=stopping_time:
    generation+=1
    print("generation=",generation)
    #Selection
    parents=select_parent_fitness_rank_dist(population)
    childs=[]
    #crossover
    for couple in parents:
        if rand.random()<P_c:
            childs.append(cross_over(couple[0],couple[1])) #%100 crossover probability
        else: childs.append(couple[0])
    #mutation
    for i in range(len(childs)):
        if rand.random()<P_m:     #%100 mutation probability
            childs[i]=mutate(childs[i])
    #update population
    population=Elitist_strategy(population,childs)
    

# Calculate statistics

results= calculate_statistics(population)



