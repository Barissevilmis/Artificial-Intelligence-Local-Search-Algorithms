import random
import sys
import time
import math
import numpy as np
import itertools
import scipy.stats as st
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
#Since each Queen conflict amount has been calculated=> return value must be divided by 2
def TotalCost(board,size):

    totalC = 0
    for i in range(size):
        totalC += CostQueen(board,i,size)
    
    return totalC/2
    

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
        
        #Random Row selection
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

#Black Box Test => Try all permuations for 4 queen => 256 different configuration 
def BlackBoxTest():

    size = 4
    row0 = [0, 1, 2, 3]
    row1 = [0, 1, 2, 3]
    row2 = [0, 1, 2, 3]
    row3 = [0, 1, 2, 3]

    permList = list(itertools.product(row0, row1, row2, row3))
    board = {}
    success = 0

    for p in range(len(permList)):
        board[0] = permList[p][0]
        board[1] = permList[p][1]
        board[2] = permList[p][2]
        board[3] = permList[p][3]

        totalCost = TotalCost(board, size)

        newCost = SimulatedAnnealing(board, size, totalCost)

        if newCost == 0:
            success += 1

    if success == len(permList):
        print("Black Box test succeeded, all permutations have been solved!")
        
        
def main(argv):

    startTime = time.time()
    board = {}
    #Size is being arranged for testing=> Don't change, not finished!
    runSize = 100
    size = [512]
    timeArr = np.zeros((runSize,1))
    
    success = 0
    print("Size     Time     StandartDeviation     StandartError     %90-CL     %95CL")
    
    for item in range(len(size)):
      
        #Trial number = 100: Easier to find avg. and percentage
        for k in range(runSize):
            specificTime = time.time()
            #Foreach columnn assign random row number => Hashmap for faster initial states search
            for i in range(size[item]):
                rand = random.randint(0,size[item]-1)
                board[i] = rand  #Keys are column numbers, rows are values

            totalCost = TotalCost(board,size[item])
            #print("----------------------------------")

            newCost = SimulatedAnnealing(board,size[item],totalCost)

            #Amount of succesful trials 
            #print('Old Cost: ', totalCost,'New Cost: ', newCost)
            if newCost == 0:
                success += 1
            timeArr[k] = time.time()-specificTime
            
        #Mean, Standart Deviation and Standart Error 
        mean = np.mean(timeArr)
        sigma = np.std(timeArr)
        stdError = sigma / (math.sqrt(runSize))
        
        #Confidence Interval Evaluation for 90% and 95%
        ninetyPercent = st.norm.interval(0.90, loc=mean, scale=sigma)
        ninetyPercent = (round(ninetyPercent[0],2),round(ninetyPercent[1],2))
        
        ninetyFivePercent = st.norm.interval(0.95, loc=mean, scale=sigma)
        ninetyFivePercent = (round(ninetyFivePercent[0],2),round(ninetyFivePercent[1],2))
        
        print(size[item],"     ","%.2f" % mean,"     ","%.2f" % sigma,"     ","%.2f" % stdError,"     ",ninetyPercent,"     ",ninetyFivePercent)
       
        
        startTime = time.time()
    #T_0 = 18000 :Success Rate: 100% => cooling 0,999 Runtime = 750s; Success Rate:44% => cooling = 0,99 Runtime = 436s ; SucessRate: 13% => cooling = 0,98, Runtime = 246s
    #How many of 100 are succesful and run time
    #print("Success Rate:",success,"%, Runtime:" ,time.time()-startTime)

if __name__ == "__main__":
    
    main(sys.argv)
