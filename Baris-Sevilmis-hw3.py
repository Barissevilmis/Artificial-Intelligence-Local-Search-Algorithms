import random
import sys
import time
import copy
from math import exp
            
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

#Calculate Energy Probability for Simulated Annealing
def EnergyCalculator(energy,temperatur):

    valE = exp(-(energy)/temperatur)
    rand = random.random()
   

    if rand < valE :
        return True
    
    return False
    

#Choose a random Successor=> If it is better then continue; else only continue with probability of EnergyCalculator
#Starting Temperatur can be assigned differently, also Mapping function of time(iteration) to temperature can be assigned differently
#Possible Optimization: Don't choose random succesor but better succesor, only when it blocks use temperature technique
def SimulatedAnnealing(board,size):

    currentState = copy.deepcopy(board)
    nextState = {}
    
    #bs => Better Succesor, ws => Worst Succesor

    #bs = 0
    #ws = 0
    t = 0
    T = 1
    while True:
        #Decrease coolFactor for better result, but higher runtime 
        coolFactor = 0.0000001 
        T -= (t*coolFactor) 
        
        if TotalCost(currentState,size) == 0:
            return currentState
        
        if T <= 0:
            #print(bs," ", ws)
            return currentState

        nextState = copy.deepcopy(currentState)

        i = random.randint(0,size-1)   
        j = random.randint(0,size-1)
        
        nextState[i] = j
        energy = TotalCost(nextState,size) - TotalCost(currentState,size)

        if energy < 0:
            #bs += 1
            currentState = copy.deepcopy(nextState)
        
        else:
            #ws += 1
            if EnergyCalculator(energy,T):
                currentState = copy.deepcopy(nextState)

        t += 1
        
                


def main(argv):

    startTime = time.time()
    board = {}
    size = 10
    
    success = 0
    k = 0
    
    while k < 100:
        #Foreach columnn assign random row number => Hashmap for faster initial states search
        for i in range(size):
            rand = random.randint(0,size-1)
            board[i] = rand  #Keys are column numbers, rows are values

        totalCost = TotalCost(board,size)

        
        board = HillClimbing(board,size)
        #board = FirstChoiceHillClimbing(board,size)
        #board = SimulatedAnnealing(board,size)

        newCost = TotalCost(board,size)

        print('Old Cost: ', totalCost,'New Cost: ', newCost)
        if newCost == 0:
            success += 1
        
        k += 1
    
    #How many of 100 are succesful and run time
    print(success," " ,time.time()-startTime)

if __name__ == "__main__":
    main(sys.argv)
