# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 12:13:47 2018

@author: Avi
"""
from DroneWorld import DroneSimulator
from Astar import AStartSearch
from Helpers import  HeuristicFunctions,EuclideanDistance
from RelaxedAStar import RAStarSearch
from Plots import PlotPath

class PathFinder:
    
    def __init__(self,droneSimulator,searchAlgorithm):
        
        self.DroneSimulator = droneSimulator
        self.SearchAlgo = searchAlgorithm
        self.__previousGoalStates = []        
    
    
    
    def GetActions(self,world,goalState,color):
        
        #identify if goal is complete or not
        isGoalComplete = False if goalState.count('?') > 0 else True
        
        #check if color is mentioned or not
        isColorMentioned = False if color == '?' else True
        
        #Update color if not mentioned.
        if isColorMentioned == False:
            if isGoalComplete == True and world.IsPositionAvailable(goalState):
                color = world.GetColor(goalState)
            else:
                color = world.GetRandomAvailableColor()
                
        # identify goal state if it is incomplete        
        if isGoalComplete == False:
            goalState = self.__identifyGoalState(world,goalState,color)
        
        #identify actions for the complete goal state
        actions = self.__getActionsForCompleteGoal(world,goalState,color)
        
        return actions
    
    def __identifyGoalState(self,world,goalState,color):
        #will update the code once Pahuni sends it
        pass
    
    def __getActionsForCompleteGoal(self, world,goalState,color):
                
        currentHeight = world.GetMaxHeight(goalState)        
        x, goalHeight, z  = goalState[0],goalState[1],goalState[2] 
        #dronePos = world.GetDronePosition()
        
        actions = []
        #if the target location is empty and there is a supporting block below
        if currentHeight == goalHeight-1:
            sourcePos = self.__identifySourcePosition(world,goalState,color)
            actions = self.__getActions(world, sourcePos, goalState)
        
        # if the target location does not have supporting block below
        if currentHeight < goalHeight-1:
            # get blocks near by that can be place to achieve the desired height
            neighbours = self.__getBlocks(goalHeight-currentHeight-1,world,goalState,color)
            
            #identify source position that can be moved to goal state
            sourcePos,sourcePosActions = self.__identifySourcePosition(world,goalState,color)
            
            height = currentHeight
            #create actions for neighbours and source block
            for neighbor in neighbours:
                actions += self.__getActions(world, neighbor, [x,height,z])
                height += 1
            
            actions += sourcePosActions
            
            actions += self.__getActions(world, sourcePos, goalState)
        
        #if the target location is occupied and there are blocks on top of it.
        if currentHeight > goalHeight-1:
            # get Empty locations near by so that that blocks can be moved to achieve the desired height
            neighbours = self.__getEmptyLocations(currentHeight-goalHeight+1,world,goalState,color)
                        
            height = currentHeight
            saved = []
            #create actions for neighbours and source block
            for neighbor in neighbours:
                actions += self.__getActions(world, neighbor, [x,height,z])
                #get block color
                blockColor = world.GetColor([x,height,z])
                
                #if block color matches with goal color then save it
                if blockColor == color:
                    saved.append(neighbor)
                height -= 1
                
            #identify source position that can be moved to goal state
            if saved != []:
                sourcePos = self.__getNearestPositions(saved,goalState)
            else:
                sourcePos,sourcePosActions = self.__identifySourcePosition(world,goalState,color)
            
            # perform actions to move any blocks required for source block to be available to move
            actions += sourcePosActions
            
            #perform actions required to move the source block
            actions += self.__getActions(world, sourcePos, goalState)
        
        return actions

    def __identifySourcePosition(self,world,goalState,color):
        
        sourceLoc = world.GetLocationsOfMovableBlock(color)

        # if there is a block already available in the upper level, we will pick the one that is is nearer
        if sourceLoc != []:
            dists = [(index,EuclideanDistance(goalState, index)) for index in sourceLoc]
            dists = sorted(dists, key = lambda i : i[1])            
                           
            return dists[0][0] ,[]   
        
        #if there are no blocks of the color readily available to move.
        heights = [(index, index[1]-world.GetMaxHeight(index)) for index in world.world.GetAvailableBlocks(color)]
        heights = sorted(heights, key = lambda i : i[1])
        
        pos, h = heights[0][0], world.GetMaxHeight(heights[0][0])
        
        # get Empty locations near by so that that blocks can be moved to achieve the desired height
        neighbours = self.__getEmptyLocations(pos[1]-h+1,world,goalState,color)
                    
        height = h
        actions = []
        x,z = pos[0],pos[2]
        
        #create actions for neighbours and source block
        for neighbor in neighbours:
            actions += self.__getActions(world, neighbor, [x,height,z])
            height -= 1
        
        return pos, actions
    
    def __getActions(self,world, source, goal):
        
        return [('Drone',source,goal),('Block',source,goal)]
    
    def __getBlocks(self,k,world,goalState,color):
        '''2) when blocks need to be placed
                a) pick  planes with height >= height(Xg,Zg) and height <= maxHeight(world) + 1                
                b) identify the K planes with minimum euclidian distance from goal (Xg,Zg) plane'''
               
        return world.GetPositions(goalState, k, color,  ('Blocks',self.__previousGoalStates))    
    
    def __getEmptyLocations(self,k,world,goalState,color):
        '''1) when blocks need to be removed
                a) pick  planes with height <= height(Xg,Zg) or height <= maxHeight(world) + 1                
                b) identify the K planes with minimum euclidian distance from goal (Xg,Zg) plane'''
        return world.GetPositions(goalState, k, color ,('Empty',self.__previousGoalStates))        
    
    def __getNearestPositions(self,saved,goalState):
        
        dists = [(index,EuclideanDistance(goalState, index)) for index in saved]
        dists = sorted(dists, key = lambda i : i[1])
        
        #first one is the min distance point
        return dists[0][0]
    
    def PerformActions(self,actions, world):
        for action in actions():            
            if action[0] == 'Drone':
                self.__action(world, world.GetDronePosition(), action[1], False)
            
            if action[0] == 'Block':
                self.__action(world, action[1], action[2], True)
    
    def __action(self, world, startPos, goalPos, hasBlock):
        
        path,_ = self.SearchAlgo.Search(startPos,goalPos,world, isDrone = (hasBlock == False))
        
        #Attach drone to the block
        if hasBlock == True:            
            success = world.Attach()
            if success == True:
                print('Block attached successfully')
            
        steps = len(path)
        i = 0
        oldPos = startPos                
        while(i < steps):
            newPos = path[i]
            
            #identify the change in the Positions
            dx,dy,dz = (newPos[0]-oldPos[0], newPos[1]-oldPos[1],newPos[2]-oldPos[2])
            
            #Perform the move in the world.
            world.Move(dx,dy,dz)
            
        if hasBlock == True:
            success = world.Release()
            if success == True:
                print('Block released successfully')
            
        
if __name__ == '__main__':
    
    goalState = '(6,0,-27,yellow)'
    
    world = DroneSimulator(100,50,100)
    world.Initialise('grid3.txt')   
    hueristics = HeuristicFunctions()
    astar = AStartSearch(lambda x,y : hueristics.hf(x,y))       
    
    pathFinder = PathFinder(world,astar)
    dronePath, blockPath,goalPos,success  = pathFinder.FindPath(goalState)
    
    
    
    blockPath = [[56, 6, 86],[56, 6, 85],[56, 6, 84],[56, 6, 83],[56, 6, 82],[56, 6, 81],[56, 6, 80],[56, 6, 79],[56, 6, 78],[56, 6, 77],[56, 6, 76],[56, 6, 75],[56, 6, 74],[56, 6, 73],[56, 6, 72],[56, 6, 71],[56, 6, 70],[56, 6, 69],[56, 6, 68],[56, 6, 67],[56, 6, 66],[56, 6, 65],[56, 6, 64],[56, 6, 63],[56, 6, 62],[56, 6, 61],[56, 6, 60],[56, 6, 59],[56, 6, 58],[56, 6, 57],[56, 6, 56],[56, 6, 55],[56, 6, 54],[56, 6, 53],[56, 6, 52],[56, 6, 51],[56, 6, 50],[56, 6, 49],[56, 6, 48],[56, 6, 47],[56, 6, 46],[56, 6, 45],[56, 6, 44],[56, 6, 43],[56, 6, 42],[56, 6, 41],[56, 6, 40],[56, 6, 39],[56, 6, 38],[56, 6, 37],[56, 6, 36],[56, 6, 35],[56, 6, 34],[56, 6, 33],[56, 6, 32],[56, 6, 31],[56, 6, 30],[56, 6, 29],[56, 6, 28],[56, 6, 27],[56, 6, 26],[56, 6, 25],[56, 6, 24]]    
    world = DroneSimulator(100,50,100)
    world.Initialise('grid3.txt')
    plot = PlotPath(world.Grid)
    plot.showPath(blockPath,dronePath)