#!/usr/bin/env python
# coding: utf-8

# In[73]:


"""
Created on Sun May 27 2021

@author: alicanyilmaz, cemrecadir
"""

import random as rand
import numpy as np
import pandas as pd
import copy
from copy import deepcopy as dp
import time
import xlsxwriter
from numpy.random import choice

class ProfitableTourProblem:
    
    def __init__(self, name, low=True):
        
        file_name = 'dataset-TSPP.xls'
        df = pd.read_excel(file_name, sheet_name = name)
        
        self.x = np.transpose(np.asarray([df['x']])) # x coordinates of customers
        self.y = np.transpose(np.asarray([df['y']])) # y coordinates of customers
        
        if low == True:
            self.profit = np.transpose(np.asarray([df['Low']])) # low profit of the customers
        else:
            self.profit = np.transpose(np.asarray([df['High']])) # high profit of the customers
        
        self.N = len(self.profit) # number of customers
        
        self.curr_sol = [] # current customer list / permutation
        self.curr_obj = None # current obj value
        self.curr_N = None; # number of customers visited in the current solution
        
        self.inc_obj = None # the incumbent objective value
        self.inc_sol = [] # the incumbent customer list / permutation
        self.inc_N = None; # number of customers visited in the incumbent solution
        
        self.distance = np.zeros((self.N, self.N)) # distance matrix between the customers
        self.CreateDistanceMatrix()
    
    def CreateDistanceMatrix(self): # create a distance matrix to store and easily access the distances between two customres (or depot)
        
        for i in range (0, self.N):
            for j in range(i, self.N):
                d = ((self.x[i]-self.x[j])**2 + (self.y[i]-self.y[j])**2)**0.5 # calculate euclidean distance
                self.distance[i,j] = d
                self.distance[j,i] = d
        self.distance = np.round(self.distance, 2) #rounding the distances to 2 digits after decimal point
        return self.distance
  
    def greedy_initial_construction(self):
        k=rand.randrange(2, self.N) #number of cities to be visited 
        route_1=[]#initially route is empty
        cities_to_be_inserted=list(choice(range(1,self.N), k,replace=False))#choose k cities to be inserted randomly
        for i in cities_to_be_inserted:
            if i == cities_to_be_inserted[0]:
                route_1=[i]
            elif i == cities_to_be_inserted[1]:
                route_1.append(i)
            else:
                route_1,_=dp(self.insert_the_best_loc(city = i,route = route_1)) #insert cities to te best location possible
        
        self.curr_sol = dp(route_1)
        self.CalculateObj()
        self.curr_N = len(self.curr_sol)
        return route_1

    def insert_the_best_loc(self,city,route): # insert the city the best possible location in the route
        cand_routes=[]
        cost_of_the_routes=[]
        for loc in range(len(route)+1):
            new_route=dp(route)
            new_route.insert(loc,city)
            cost_of_the_routes.append(self.CalculateObj(new_route))
            cand_routes.append(new_route)
        best_route=cand_routes[np.argmax(cost_of_the_routes)]
        return best_route,np.max(cost_of_the_routes)
    
    def CalculateObj(self, route = None): # calculate the objective value vector for the current solution
        
        if route == None: # if another solution is not specified, use self.curr_sol
            flag = 0
            route = dp(self.curr_sol)
        
        else:
            flag = 1        
        obj=0
        for loci,i in enumerate(route):
            if loci==0:
                obj+=self.profit[i]-self.distance[0,route[loci]]
            else:
                obj+=self.profit[i]-self.distance[route[loci-1],route[loci]] 
        if len(route)>=1:
            obj+=-self.distance[route[len(route)-1],0]
        obj = np.round(obj, 2)
        
        if flag == 0: # change self.curr_obj
            self.curr_obj = dp(float(obj))
        
        return float(obj)
    
    def Addition(self, solution=None, obj=None):
        
        if solution == None: # if another solution is not specified, use self.curr_sol
            flag = 0
            solution = dp(self.curr_sol)
            obj = dp(self.curr_obj)
            n = dp(self.curr_N)
        
        else:
            flag = 1
            n = len(solution)
        
        untravelled=[i for i in range(1,self.N) if i not in solution] # list of untravelled cities
        delta=[]
        maxdelta=[]
        maxdelta_ind=[]
        for i in range(0,len(untravelled)):
            delta.append([])
            for j in range(0,n):
                # calcuate the change in the obj
                if j == 0:
                    delta[i].append(self.profit[untravelled[i]]-self.distance[0,untravelled[i]]-self.distance[untravelled[i],solution[0]]+self.distance[0,solution[0]])
                else:
                    delta[i].append(self.profit[untravelled[i]]-self.distance[solution[j-1],untravelled[i]]-self.distance[untravelled[i],solution[j]]+self.distance[solution[j-1],solution[j]])
            maxdelta.append(max(delta[i])) #find the best obj change for an untravalled city
            maxdelta_ind.append(delta[i].index(max(delta[i])))
        
        bestdelta = max(maxdelta) # find the best obj change
        if bestdelta > 0: # apply the move only if the onjective improves
            cust_ind = maxdelta.index(bestdelta) # the index of the customer having the best obj change
            pos = maxdelta_ind[cust_ind] # the position to insert
            cust = untravelled[cust_ind] # the customer to insert
            solution.insert(pos, cust)
            obj = obj + bestdelta
            n = n + 1
        
        if flag == 0: # change self.curr_obj
            self.curr_sol = dp(solution)
            self.curr_obj = dp(obj)
            self.curr_N = dp(n)
            
        return solution, obj, n
    
    def Removal(self, solution=None, obj=None):
        
        flag = 1
        
        if solution == None: # if another solution is not specified, use self.curr_sol
            flag = 0
            solution = dp(self.curr_sol)
            obj = dp(self.curr_obj)
            n = dp(self.curr_N)
        
        else:
            n = len(solution)
        
        delta=[]
        for i in range(0,n):
            # find the customers that affect the obj change
            if i == 0:
                prev_cust = 0
                curr_cust = solution[i]
                next_cust = solution[i+1]
            elif i== n-1:
                prev_cust = solution[i-1]
                curr_cust = solution[i]
                next_cust = 0
            else:
                prev_cust = solution[i-1]
                curr_cust = solution[i]
                next_cust = solution[i+1]
            # calculate obj change
            delta.append(-self.profit[curr_cust]+self.distance[prev_cust,curr_cust]+self.distance[curr_cust,next_cust]-self.distance[prev_cust,next_cust])
        
        bestdelta = max(delta) # find best possible change
        if bestdelta > 0: # apply the move only if the onjective improves
            cust_ind = delta.index(bestdelta) # index of the customer to be deteted
            cust = solution[cust_ind] # the customer to be removed
            solution.remove(cust)
            obj = obj + bestdelta
            n = n - 1
        
        if flag == 0: # change self.curr_obj
            self.curr_sol = dp(solution)
            self.curr_obj = dp(obj)
            self.curr_N = dp(n)
            
        return solution, obj, n
    
    def Two_Opt(self,route = None, obj=None):
        
        flag = 1
        
        if route == None: # if another solution is not specified, use self.curr_sol
            flag = 0
            route = dp(self.curr_sol)
            obj = dp(self.curr_obj)
                
        route.insert(0, 0) #add depots
        route.append(0)
        possible_routes=[]
        delta_cost=[]           
        for i in range(1, len(route)-2):
               for j in range(i+2, len(route)-1):
                    #print("i,j=",i,j)
                    # create the new route by reversing the cities between i and j
                    new_route = []
                    new_route = dp(route[:])
                    new_route[i:j] = dp(route[j-1:i-1:-1])
                    new_route = dp(new_route[1:-1]) #removes 0's(depots)
                    possible_routes.append(new_route)
                    before_c=self.distance[route[i-1],route[i]]+self.distance[route[j-1],route[j]] #cost before 2-opt
                    after_c=self.distance[route[i-1],route[j-1]]+self.distance[route[i],route[j]] #cost after 2-opt
                    delta_cost.append(before_c-after_c) # the change in the obj value
        #print("delta_cost=",delta_cost,"possible_routes=",possible_routes)
        if delta_cost[np.argmax(delta_cost)]>0: #if maximum delta_cost is positive, choose its' route,else make no change
            obj = obj + delta_cost[np.argmax(delta_cost)]
            route = dp(possible_routes[np.argmax(delta_cost)])
        else: # remove 0's (depot)
            route.remove(0)
            route.remove(0)
        
        if flag == 0: # change self.curr_obj
            self.curr_sol = dp(possible_routes[np.argmax(delta_cost)])
            self.curr_obj = dp(obj)
        return route, obj, len(route)
    
    def MultiRemoval_Reinsertation(self,solution = None, obj=None):
        flag = 1
        
        if solution == None: # if another solution is not specified, use self.curr_sol
            flag = 0
            solution = dp(self.curr_sol)
            obj = dp(self.curr_obj)
            n = dp(self.curr_N)
        
        else:
            n = len(solution)
            
        sol=dp(solution)
        removed_locs=[] # store the removed customers
        for i in range(n):
            if rand.random()>0.5: # remove probabilistically
                sol.remove(solution[i])
                removed_locs.append(solution[i])
        rand.shuffle(removed_locs) # reorder
        for city in removed_locs:
            sol,_=self.insert_the_best_loc(city,sol) # insert to the best location
         
        obj=self.CalculateObj(sol)
        if flag == 0: # change self.curr_obj
            self.curr_sol = dp(sol)
            self.curr_obj = dp(obj)
            self.curr_N   = len(sol)
        return sol, obj , len(sol) 
    
    
    def MultiRemoval_Addition(self,solution = None, obj=None):
        flag = 1
        
        if solution == None: # if another solution is not specified, use self.curr_sol
            flag = 0
            solution = dp(self.curr_sol)
            obj = dp(self.curr_obj)
            n = dp(self.curr_N)
        
        else:
            n = len(solution)
            
        sol=dp(solution)
        removed_locs=[i for i in range(1,self.N) if i not in solution] # list of unvisited cities (removed cities are appended too)
        for i in range(n):
            if rand.random()<0.4: # remove probabilistically
                sol.remove(solution[i]) 
                removed_locs.append(solution[i])
        rand.shuffle(removed_locs) #reorder
        sol_obj=self.CalculateObj(sol)
        for city in removed_locs:
            new_sol,best_cost=self.insert_the_best_loc(city,sol) # insert to the best location
            if best_cost>sol_obj: # insert if it improves the obj
                sol=dp(new_sol)
                sol_obj=dp(best_cost)
         
        obj=dp(sol_obj)
        if flag == 0: # change self.curr_obj
            self.curr_sol = dp(sol)
            self.curr_obj = dp(obj)
            self.curr_N   = len(sol)
            
        return sol, obj , len(sol)    
    
    def VND(self, k_max=3, max_iter = None):
        
        best_s = dp(self.curr_sol)
        best_obj = dp(self.curr_obj)
        best_n = dp(self.curr_N)
        
        if max_iter == None:
            max_iter = 1
        
        nu_of_iterations=0 #keep track of number of iterations.
        for i in range(0, max_iter):
            k=1 # initially first neighborhood is used    
            while k <= k_max:
                
                #print("d-k=",k,"d-best_obj=",best_obj,"d-incumbent_s=",best_s,"d-incumbent_n=",best_n)
                nu_of_iterations+=1 #needed for output table
                
                #LOCAL SEARCH with VND
                if k == 1:
                    self.curr_sol, self.curr_obj, self.curr_N=dp(self.Addition(best_s,best_obj))
                elif k == 2:
                    self.curr_sol, self.curr_obj, self.curr_N=dp(self.Removal(best_s,best_obj))
                
                elif k == 3:
                    self.curr_sol, self.curr_obj, self.curr_N=dp(self.Two_Opt(best_s,best_obj))
                
                if self.curr_obj > best_obj: #local optimum condition
                    best_s = dp(self.curr_sol) #update the best solution
                    best_obj = dp(self.curr_obj) # update the best cost
                    best_n = dp(self.curr_N) # update number of customers
                    k=1  #initialize the neighborhood structure
                else:
                    k+=1 #update the neighborhood structure
        
        # update the current solution, objective and N as the best solution found by the VND
        self.curr_sol = dp(best_s)
        self.curr_obj = dp(best_obj)
        self.curr_N = dp(best_n)
        
        return best_s, best_obj, best_n, nu_of_iterations, i
    
    def VNSwithVND(self, k_max=2, max_time=180, patience=40):
        
        self.inc_sol = dp(self.curr_sol) #update the best solution
        self.inc_obj = dp(self.curr_obj) # update the best cost
        self.inc_N = dp(self.curr_N) # update number of customers
        
        start_time = time.time()
        nu_of_iterations=0 #keep track of number of iterations.
        while (time.time() - start_time)<=max_time: # end the heuristic when the time limit is passednd the heuristic when the time limit is passed
            k=1 # initially first neighborhood is used    
            while k <= k_max:
                print("k=",k,"best_obj=",self.inc_obj,"incumbent_s=",self.inc_sol,"incumbent_n=",self.inc_N)
                nu_of_iterations+=1 #needed for output table
                #SHAKING
                if k == 1:
                    self.curr_sol, self.curr_obj, self.curr_N=dp(self.MultiRemoval_Reinsertation(self.inc_sol,self.inc_obj))
                elif k == 2:
                    self.curr_sol, self.curr_obj, self.curr_N=dp(self.MultiRemoval_Addition(self.inc_sol,self.inc_obj))
                
                #LOCAL SEARCH(VND is used for local search)
                self.VND()
                
                print(self.inc_obj)
                    
                if self.curr_obj > self.inc_obj: #local optimum condition
                    self.inc_sol = dp(self.curr_sol) #update the best solution
                    self.inc_obj = dp(self.curr_obj) # update the best cost
                    self.inc_N = dp(self.curr_N) # update number of customers
                    real_time = np.round(time.time()-start_time, 2)
                    k=1 # initialize the neighborhood structure
                else:
                    k+=1 #update the neighborhood structure
            if np.round(time.time()-start_time,2) - real_time > patience:
                break
        total_time = np.round(time.time()-start_time, 2)
        return self.inc_sol, float(self.inc_obj), self.inc_N, nu_of_iterations, total_time, real_time


# In[74]:


workbook = xlsxwriter.Workbook('CemreÇadır_AlicanYılmaz_hw3results2.xlsx')


# In[63]:


rand.seed(51)
eil51_LP = ProfitableTourProblem('eil51', low=True)
worksheet = workbook.add_worksheet("eil51-LP")
for i in range(5):
    eil51_LP.greedy_initial_construction()
    inc_sol, inc_obj, inc_N, nu_of_iterations, totaltime, realtime = eil51_LP.VNSwithVND()
    inc_sol.insert(0,0)
    inc_N = len(inc_sol)
    s = ','.join([str(elem) for elem in inc_sol])
    writelist = ['eil51-LP', inc_obj, inc_N, s, totaltime]
    for j in range (0, len(writelist)):
        worksheet.write(i+1,j, writelist[j])


# In[64]:


rand.seed(51)
eil51_HP = ProfitableTourProblem('eil51', low=False)
worksheet = workbook.add_worksheet("eil51-HP")
for i in range(5):
    eil51_HP.greedy_initial_construction()
    inc_sol, inc_obj, inc_N, nu_of_iterations, totaltime, realtime = eil51_HP.VNSwithVND()
    inc_sol.insert(0,0)
    inc_N = len(inc_sol)
    s = ','.join([str(elem) for elem in inc_sol])
    writelist = ['eil51-HP', inc_obj, inc_N, s, totaltime]
    for j in range (0, len(writelist)):
        worksheet.write(i+1,j, writelist[j])


# In[65]:


rand.seed(76)
eil76_LP = ProfitableTourProblem('eil76', low=True)
worksheet = workbook.add_worksheet("eil76-LP")
for i in range(5):
    eil76_LP.greedy_initial_construction()
    inc_sol, inc_obj, inc_N, nu_of_iterations, totaltime, realtime = eil76_LP.VNSwithVND()
    inc_sol.insert(0,0)
    inc_N = len(inc_sol)
    s = ','.join([str(elem) for elem in inc_sol])
    writelist = ['eil76-LP', inc_obj, inc_N, s, totaltime]
    for j in range (0, len(writelist)):
        worksheet.write(i+1,j, writelist[j])


# In[66]:


rand.seed(76)
eil76_HP = ProfitableTourProblem('eil76', low=False)
worksheet = workbook.add_worksheet("eil76-HP")
for i in range(5):
    eil76_HP.greedy_initial_construction()
    inc_sol, inc_obj, inc_N, nu_of_iterations, totaltime, realtime = eil76_HP.VNSwithVND()
    inc_sol.insert(0,0)
    inc_N = len(inc_sol)
    s = ','.join([str(elem) for elem in inc_sol])
    writelist = ['eil76-HP', inc_obj, inc_N, s, totaltime]
    for j in range (0, len(writelist)):
        worksheet.write(i+1,j, writelist[j])


# In[67]:


rand.seed(101)
eil101_LP = ProfitableTourProblem('eil101', low=True)
worksheet = workbook.add_worksheet("eil101-LP")
for i in range(5):
    eil101_LP.greedy_initial_construction()
    inc_sol, inc_obj, inc_N, nu_of_iterations, totaltime, realtime = eil101_LP.VNSwithVND()
    inc_sol.insert(0,0)
    inc_N = len(inc_sol)
    s = ','.join([str(elem) for elem in inc_sol])
    writelist = ['eil101-LP', inc_obj, inc_N, s, totaltime]
    for j in range (0, len(writelist)):
        worksheet.write(i+1,j, writelist[j])


# In[75]:


rand.seed(101)
eil101_HP = ProfitableTourProblem('eil101', low=True)
worksheet = workbook.add_worksheet("eil101-HP")
for i in range(3):
    eil101_HP.greedy_initial_construction()
    inc_sol, inc_obj, inc_N, nu_of_iterations, totaltime, realtime = eil101_HP.VNSwithVND(max_time=180*3, patience=120)
    inc_sol.insert(0,0)
    inc_N = len(inc_sol)
    s = ','.join([str(elem) for elem in inc_sol])
    writelist = ['eil101-HP', inc_obj, inc_N, s, totaltime]
    for j in range (0, len(writelist)):
        worksheet.write(i+1,j, writelist[j])


# In[72]:


workbook.close()

