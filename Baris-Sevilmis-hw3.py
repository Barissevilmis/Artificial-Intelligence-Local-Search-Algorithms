import random
import sys
import time
import math
import copy
import numpy as np
import scipy.stats
import pandas as pd
            
#Conflict amount of a single queen with other queens in terms of rows and queens diagonal locations
def CostQueen(board, key, size):

    costQ = 0
    
    for i in range(size):

        if i != key:
            
            #Check row collision
            if board[i] == board[key] :
                costQ += 1

            #Check diagonal collisions
            index = key - i
            
            if board[i] == (board[key]-index) or board[i] == (board[key]+index):
                costQ += 1
    
    
   
    return costQ

#Total Cost Function=> Sum of each conflicts cost
def TotalCost(board,size):

    totalC = 0
    for i in range(size):
        totalC += CostQueen(board,i,size)
    
    return totalC/2

#Hill climbing algorithm is used => Every step choose highest succesor of current state is chosen
#Ends when local maxima or global maxima is reached
def HillClimbing(board,size):    

    currentState = copy.deepcopy(board)
    nextState = {}
    tempState = copy.deepcopy(board)
    

    while True:

        tempState.clear()

        for i in range(size):

            costCurr = CostQueen(currentState,i,size)
            
            for j in range(size):
                
                nextState = copy.deepcopy(currentState)
                nextState[i] = j

                if CostQueen(nextState,i,size) < costCurr:
                    costCurr = CostQueen(nextState,i,size)
                    tempState = copy.deepcopy(nextState)
              
        if len(tempState) != 0 and (TotalCost(tempState,size) < TotalCost(currentState,size)):
            currentState = copy.deepcopy(tempState)
        
        else:
            return currentState

#Variation of Hill Climbing: Choose first better successor of the current state and continue until you reach a certain maximum point   
def FirstChoiceHillClimbing(board,size):

    currentState = copy.deepcopy(board)
    tempState = {}
    nextState = {}
    

    while True:

        nextState.clear()

        for i in range(size):

            costCurr = CostQueen(currentState,i,size)
            tempState = copy.deepcopy(currentState)

            for j in range(size):
                    
                nextState = copy.deepcopy(currentState)
                nextState[i] = j

                if CostQueen(nextState,i,size) < costCurr:
                    currentState = copy.deepcopy(nextState)
                    break
              
        if TotalCost(tempState,size) == TotalCost(currentState,size):
            return currentState

    

#Choose a random Successor=> If it is better then continue; else only continue with probability of EnergyCalculator
#Starting Temperatur can be assigned differently, also Mapping function of time(iteration) to temperature can be assigned differently
#Possible Optimization: Don't choose random succesor but better succesor, only when it blocks use temperature technique
def SimulatedAnnealing(currentState,size,totalCost):

    nextState = {}
    
    #Scheduling Function: works fast for both small and large sizes(Success amount relatively small also in small size compared to first function) 
    #T_0 = 25000000 
    #T_0 = 3000000
    #T_0 = 110000
    #T_0 = 18000
    #Cooling Factor must be greater than 0,95 for success in 100 states
    #T = T_0*pow(0.99,t)
    #T = T_0*pow(0.98,t)
    
    #Current Parameters: Nearly 100% success for 10-100 size
    t = 1
    T_0 = 18000 
    while True:
        
        coolingFactor = 0.999
        T = T_0*pow(coolingFactor,t)
        
        #If totalcost becomes 0, goal is reached
        #Can directly return 0
        if totalCost == 0:
            return 0
        
        #Temperatur becomes 0, meaning simulated annealing must be finished
        if T == 0: 
            return totalCost
        
        
        #Random Column selection
        i = random.randint(0,size-1)  
        
        currentRow = currentState[i]
        
        #Calculate selected queens collision amount before changing its row
        currentQueenCost = CostQueen(currentState,i,size)
        
        #Random Column Statement
        j = random.randint(0,size-1)
            
        currentState[i] = j
        
        #Calculate selected queens collision amount after changing its row
        nextQueenCost = CostQueen(currentState,i,size)
        
        #energy = nextstate(energy) - currentstate(energy)
        delta = nextQueenCost - currentQueenCost

        if delta <= 0:
          
            totalCost += delta
        
        else:
            #Calculate energy in terms of deciding whether to accept worst state or not
            energy = totalCost + delta
            valE = 2**(-(energy)/T)
            rand = random.uniform(0,1)
            #print(valE)
            if rand < valE :
                totalCost += delta
            
            else:
                currentState[i] = currentRow

        
        t+=1       


def main(argv):

    startTime = time.time()
    board = {}
    #Size is being arranged for testing=> Don't change, not finished!
    size = 100 #[64,128,256,512,1024]
    
    success = 0
    
    #Trial number = 100: Easier to find avg. and percentage
    for k in range(size):
        #Foreach columnn assign random row number => Hashmap for faster initial states search
        for i in range(size):
            rand = random.randint(0,size-1)
            board[i] = rand  #Keys are column numbers, rows are values

        totalCost = TotalCost(board,size)
        print("----------------------------------")

        newCost = SimulatedAnnealing(board,size,totalCost)

        #Amount of succesful trials 
        print('Old Cost: ', totalCost,'New Cost: ', newCost)
        if newCost == 0:
            success += 1
    
    # T_0 = 18000 :Success Rate: 100% => cooling 0,999 Runtime = 750s; Success Rate:44% => cooling = 0,99 Runtime = 436s ; SucessRate: 13% => cooling = 0,98, Runtime = 246s
    #How many of 100 are succesful and run time
    print(success," " ,time.time()-startTime)

if __name__ == "__main__":
    main(sys.argv)

        
                


