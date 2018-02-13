# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 12:13:47 2018

@author: Avi
"""
from DroneWorld import DroneSimulator
from Astar import AStartSearch
from Helpers import  HeuristicFunctions,EuclideanDistance
from RelaxedAStar import RAStarSearch

class PathFinder:
    
    def __init__(self,droneSimulator,searchAlgorithm):
        
        self.DroneSimulator = droneSimulator
        self.SearchAlgo = searchAlgorithm        
    
    def FindPath(self, targetLoc):
                
        #extract color of block to move
        pos, color = self.DroneSimulator.ExtractPosColorFromInput(targetLoc)
        
        unknownsCount = pos.count('?')
        if unknownsCount == 0:
            goalPos  = self.DroneSimulator.GetPosFromString(pos)
            
            #check if target is empty or not
            
            #identify which block neeed to be moved
            dronePath, blockPath, success = self.__findPaths(list(goalPos),color)
        else:
            #identify the block nearer to drone of same color
            dronePaths,success = self.__findSource(color)
            
            if success == True:
                
                sourceLoc = list(dronePaths.keys())                                
                pathLens = sorted([(loc,len(dronePaths[loc])) for loc in sourceLoc], key = lambda p: p[1]) 
                #print(pathLens[0][])
                sourcePos = list(pathLens[0][0])
                dronePath = dronePaths[pathLens[0][0]]
        
                goalPos,blockPath = self.__identifyGoalPosition(pos,color,sourcePos)
                                
            else:
                return None, None, False
        
        return dronePath, blockPath,goalPos,success        
    
    def __identifyGoalPosition(self,goal, color,sourcePos):
        
        unknownsCount = goal.count('?')        
        if unknownsCount  == 3:
            goalPos = self.DroneSimulator.GetRandomEmpty()
            path,cost = self.SearchAlgo.Search(sourcePos,goalPos,self.DroneSimulator, isDrone=False)
            return goalPos,path
        
        x = goal[:str.index(goal,",")]
        rest = goal[str.index(goal,",")+1:]
        y = rest[:str.index(rest,",")]
        z = rest[str.index(rest,",")+1:]
                
        indices = self.DroneSimulator.GetPossibleGoalPos([x,y,z],color,sourcePos)
        
        print(sourcePos)            
        if len(indices) > 0:
            dists = [(index,EuclideanDistance(sourcePos, index)) for index in indices]
            dists = sorted(dists, key = lambda i : i[1])                        
            goalPos, path = self.__getMinDistIndex( dists[:10], sourcePos)

        else:
            goalPos =  self.DroneSimulator.GetRandomEmpty()                 
            path,cost = self.SearchAlgo.Search(sourcePos,goalPos,self.DroneSimulator, isDrone=False)

        
        return goalPos, path
    
    def __getMinDistIndex(self, top10,sourcePos):
        
        paths = dict()        
        
        #call search algorithm to identify the cost for Drone to move to each of the source loc
        for loc in top10: 
            #loc contains (identifiedGoalPos, euclideandistance)
            #pick the identifiedGoalPos to gaol
            goal = loc[0]
            dronePath,cost = self.SearchAlgo.Search(sourcePos,goal,self.DroneSimulator, isDrone=False)
            paths[tuple(goal)] = dronePath
                
        pathLens = sorted([(loc[0],len(paths[tuple(loc[0])])) for loc in top10], key = lambda p: p[1])
        
        goalPos = pathLens[0][0]
        path = paths[tuple(goalPos)]
        
        return goalPos, path
        
    def __findSource(self,color):
        
        sourceLoc, validColor = self.DroneSimulator.GetLocationsOfMovableBlock(color,forDrone = True)
        
        if validColor == False:
            return None,None, False
        
        dronePaths = dict()        
        
        #call search algorithm to identify the cost for Drone to move to each of the source loc
        for loc in sourceLoc:            
            dronePath,cost = self.SearchAlgo.Search(self.DroneSimulator.GetDronePosition(),loc,self.DroneSimulator, isDrone=True)
            dronePaths[tuple(loc)] = dronePath
            
        return dronePaths, True
    
    def __findPaths(self,goal,color):
        
        
        sourceLoc, validColor = self.DroneSimulator.GetLocationsOfMovableBlock(color,forDrone = True)
        
        if validColor == False:
            return None,None,False
        
        dronePaths = dict()
        blockPaths = dict()
        
        #call search algorithm to identify the cost for Drone to move to each of the source loc
        for loc in sourceLoc:            
            dronePath,cost = self.SearchAlgo.Search(self.DroneSimulator.GetDronePosition(),loc,self.DroneSimulator, isDrone=True)
            dronePaths[tuple(loc)] = dronePath
                        
            blockPath,cost = self.SearchAlgo.Search([loc[0],loc[1]-1,loc[2]], goal,self.DroneSimulator, isDrone=False)
            blockPaths[tuple(loc)] = blockPath
            
        pathLens = [len(dronePaths[tuple(loc)]) + len(blockPaths[tuple(loc)]) for loc in sourceLoc]
        
        minIndexSource = pathLens.index(min(pathLens))
        
        loc = sourceLoc[minIndexSource]
        
        return dronePaths[tuple(loc)], blockPaths[tuple(loc)],True
        
if __name__ == '__main__':
    
    goalState = '(4,1,3,red)'
    
    world = DroneSimulator(100,50,100)
    world.Initialise('data.txt')   
    hueristics = HeuristicFunctions()
    astar = AStartSearch(lambda x,y : hueristics.hf(x,y))       
    
    pathFinder = PathFinder(world,astar)
    dronePath, blockPath,goalPos,success  = pathFinder.FindPath(goalState)
    
    goalState1 = '(-4,?,3,red)'
    dronePath1, blockPath1,goalPos1,success  = pathFinder.FindPath(goalState1)
        
    goalState2 = '(-2,?,?,?)'
    dronePath2, blockPath2,goalPos2,success  = pathFinder.FindPath(goalState2)
    
    goalState3 = '(?,?,?,?)'
    dronePath3, blockPath3,goalPos3,success  = pathFinder.FindPath(goalState3)
    
    raStar = RAStarSearch(lambda x,y : hueristics.hf(x,y))
    pathFinder = PathFinder(world,raStar)
    
    goalState4 = '(0,0,?,?)'
    dronePath4, blockPath4,goalPos4,success  = pathFinder.FindPath(goalState4)
        
    
    
        