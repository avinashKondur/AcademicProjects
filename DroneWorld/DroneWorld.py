# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:08:37 2018

@author: Avi
"""
import numpy as np
import random
from math import sqrt


class DroneSimulator:
    
    def __init__(self,nx,ny,nz):
        
        self._nx = nx
        self._ny = ny
        self._nz = nz
        
        self.CurrentDronePos = None
        self.colors = dict()
        self.OccupiedPos = []
        self.IsBlockAttached = False
        
        self.Grid = [[['' for k in range(self._nx+1)] for j in range(self._ny+1)] for i in range(self._nz+1)]
    
    def Initialise(self,fileName):
        
        try:
            fo = open(fileName,'r')
            data = fo.read()            
            lines = data.split('\n')
            
            #print(lines)
            #fetch the drones information from the list
            drones = list(filter(lambda x : 'DRONE' in str.upper(str.strip(x)),lines))
            
            #fetch blocks information from the list
            blocks = list(filter(lambda x : 'DRONE' not in str.upper(str.strip(x)),lines))
            
            #print(blocks)
            #check if there is only one drone mentioned in the file
            if len(drones) != 1 :
                print('Drone world should have one Drone. Please correct the input file and restart the process')
                return False                
            
            self.CurrentDronePos,obj,isValid = self.__getDataFromLine(drones[0])
            
            #print(obj)
            self.Grid[self.CurrentDronePos[0]][self.CurrentDronePos[1]][self.CurrentDronePos[2]] = obj
            
            self.OccupiedPos.append(self.CurrentDronePos)
            
            if isValid == False:
                return False
            
            blocksDict = dict()
            
            for block in blocks:

                if block.strip() == '':
                    continue
                
                #blockPos,color,isValid = self.__getDataFromLine(block)
                pos, color = self.ExtractPosColorFromInput(block)
                blockPos = self.GetPosFromString(pos)
                
                blocksDict[tuple(blockPos)] = color
                                
                #update the colors dictionary 
                self.colors[color] = self.colors.get(color,0) + 1
            
            blocksList = list(blocksDict.keys())
            blocksList = sorted(blocksList, key = lambda p : p[1])
            
            print(blocksList)
            for block in blocksList:
                
                isValid = self.ValidatePos(list(block))
                                
                if isValid == False:
                    continue
                
                #update the block pos dictionary
                self.OccupiedPos.append(blockPos)
                                                
                #set the grid with respective Color
                self.Grid[block[0]][block[1]][block[2]] = color                
                                                    
        except IOError:
            print('Exception while reading the file - ', fileName)
        except:
            print('Exception raised in initialising block world.....')
    
    def Attach(self):
        dronePos = self.CurrentDronePos
        if (dronePos[0], dronePos[1]-1, dronePos[2]) in self.BlockPos:
            self.IsBlockAttached = True
            return True
        else:
            print("Block cannot be attached as there is not block below.")
            return False
    
    def Move(self, dx,dy,dz):
        
        if dx not in [-1,0,1] or dy not in [-1,0,1] or dz not in [-1,0,1]:
            print("displacement length should not exceed more than 1 in length")
            return False
        
        newDonePos = (self.CurrentDronePos[0] + dx, self.CurrentDronePos[1]+dy, self.CurrentDronePos[2]+dz)
        
        if newDonePos in self.OccupiedPos:
            print("Destination square for drone is occupied")
            return False
        
        if self.IsBlockAttached:
            newBlockPos = (newDonePos[0],newDonePos[1]-1,newDonePos[2])
            
            if newBlockPos in self.BlockPos:
                print("Drone has block attached and the new position has a block obstructing the dron movement")
                return False
            
            currentBlockPos = (self.CurrentDronePos[0] , self.CurrentDronePos[1]-1, self.CurrentDronePos[2])
            
            #move the block to new Position
            self.Grid[newBlockPos[0]][newBlockPos[1]][newBlockPos[2]] = self.Grid[currentBlockPos[0]][currentBlockPos[1]][currentBlockPos[2]]
            self.OccupiedPos.append(newBlockPos)
            
            self.Grid[currentBlockPos[0]][currentBlockPos[1]][currentBlockPos[2]] = ''
            self.OccupiedPos.remove(currentBlockPos)
            
        # move the Grid to new Position
        self.Grid[newDonePos[0]][newDonePos[1]][newDonePos[2]] = self.Grid[self.CurrentDronePos[0]][self.CurrentDronePos[1]][self.CurrentDronePos[2]]
        self.OccupiedPos.append(newDonePos)
        
        self.Grid[self.CurrentDronePos[0]][self.CurrentDronePos[1]][self.CurrentDronePos[2]] = ''
        self.OccupiedPos.remove(self.CurrentDronePos)
        
        self.CurrentDronePos = newDonePos
                
        return True
            
    def Release(self):
        if not self.IsBlockAttached:
            print("There is not block atttached and Release cannot be performed")
            return False
                
        currentBlockPos = (self.CurrentDronePos[0] , self.CurrentDronePos[1]-1, self.CurrentDronePos[2])
        while (currentBlockPos[0] , currentBlockPos[1]-1, currentBlockPos[2]) not in self.BlockPos:
            currentBlockPos = (currentBlockPos[0] , currentBlockPos[1]-1, currentBlockPos[2])
            
            
        self.IsBlockAttached = False    
        return True
            
    def __getDataFromLine(self, line):
        
        pos,obj = self.ExtractPosColorFromInput(line)
    
        #validate the position
        transfromedPos,isValid = self.ValidatePos(self.GetPosFromString(pos),str.upper(obj) == 'DRONE')
        
        if isValid == False:
            print('Input has invalid Position : {0} for object : {1} '.format(pos,obj))
            if str.upper(obj) == 'DRONE':
                print('System will terminate now as the position for Drone is invalid')
            
        return (transfromedPos, str.upper(obj),isValid)
    
    def ExtractPosColorFromInput(self,line):
        pos = line[str.index(line,"(")+1:str.rindex(line,",")]
        obj = line[str.rindex(line,",")+1:str.rindex(line,")")]
        
        return pos,obj
    
    
    def GetPosFromString(self, string):
        x = string[:str.index(string,",")]
        rest = string[str.index(string,",")+1:]
        y = rest[:str.index(rest,",")]
        z = rest[str.index(rest,",")+1:]
        
        return self.GetTransformedGridPosition((int(x), int(y), int(z)))
    
    def GetTransformedGridPosition(self, pos):
        return [pos[0] + 50,pos[1],pos[2] + 50]
    
    def GetTransformedUserFormat(self,pos):
        return [pos[0] - 50,pos[1],pos[2] - 50]
    
    def ValidatePos(self,pos, isDrone = False, pathSearch = False):        
        
        (x,y,z) = (pos[0],pos[1],pos[2])
        
        #print(x,y,z)
        #check if coordinates are in valid range
        if x not in range(0,self._nx + 1) or y not in range(0,self._ny+1) or z not in range(0,self._nz + 1):
            print('Given coordinates {0} are out of range '.format(pos))
            return None, False
        
        #check if the block position is not in air
        if isDrone == False and pathSearch == False and y != 0 and [x,y-1,z] not in self.OccupiedPos and [x,y-1,z] != self.CurrentDronePos:
            print('There is no supporting block below for pos = {0}'.format(pos))
            return None, False
        
        #if this is called in path search then, we would need to check position above the block is also un occcupied for the 
        #Drone to move, after finding the path
        if isDrone == False and pathSearch == True and [x,y+1,z] in self.OccupiedPos:
            return None, False
        
        #check if the position is already occupied by another block
        if pos in self.OccupiedPos:
            print('There is already a block in the given position = {0}'.format(pos))
            return None, False
        
        return (pos,True)
    
    def GetLocationsOfMovableBlock(self, color, forDrone = False):
        
        
        if color != '?' and str.upper(color) not in list(self.colors.keys()):
            print("There is no block with color : ", color)                
            return None,False
        
        if color == '?':            
            color = random.choice(list(self.colors.keys()))
            print("Color is not mentioned in the input, so randmonly choosen color is : ",color)
            
        nGrid = np.asarray(self.Grid)        
        xi, yi, zi = np.where(nGrid == str.upper(color))
        
        if forDrone == True:
            indices = [[x,y+1,z] for x,y,z in zip(*(xi,yi,zi))]            
            return list(filter(lambda p : nGrid[p[0]][p[1]][p[2]] == '', indices)), True
        else:
            indices = [[x,y,z] for x,y,z in zip(*(xi,yi,zi))]
            return list(filter(lambda p : nGrid[p[0]][p[1]+1][p[2]] == '', indices)), True
        
    
    def GetDronePosition(self):
        return self.CurrentDronePos
    
    def GetRandomEmpty(self):
        nGrid = np.asarray(self.Grid)
        xi,yi,zi = np.where(nGrid == '')
        
        indices = [[x,y,z] for x,y,z in zip(*(xi,yi,zi))]
        return random.choice(list(filter(lambda p : nGrid[p[0]][p[1]-1][p[2]] != '', indices)))
        
    
    def GetPossibleGoalPos(self, gPos,color,sourcePos):
        
        (xmissing,ymissing,zmissing) = (gPos[0]=='?',gPos[1]=='?',gPos[2]=='?')        
        
        print('gPos = ', gPos)
        
        nGrid = np.asarray(self.Grid)
        xi,yi,zi = np.where(nGrid == '')
        indices = [[x,y,z] for x,y,z in zip(*(xi,yi,zi))]
        
        print('len(indices)=',len(indices))
        if ymissing == False:            
            yLevelIndices = list(filter(lambda p : (p[1] == 0 and p[1] == int(gPos[1])) or (nGrid[p[0]][int(gPos[1])-1][p[2]] != '' and p[1] == int(gPos[1])), indices))            
        else:
            
            yLevelIndices = list(filter(lambda p : nGrid[p[0]][p[1]-1][p[2]] != '', indices))
        #print('len(yLevelIndices)=',yLevelIndices)
            
        if xmissing == False:
            yLevelIndices = list(filter(lambda p : p[0] == int(gPos[0])+50, yLevelIndices))
            #print('len(yLevelIndices)=',yLevelIndices)
            
        if zmissing == False:
            yLevelIndices = list(filter(lambda p : p[2] == int(gPos[2])+50, yLevelIndices))
            #print('len(yLevelIndices)=',yLevelIndices)
        
        #print('yLevelIndices = ',yLevelIndices)
        return yLevelIndices            
            
        
        
if __name__ == '__main__':
    world = DroneSimulator(100,50,100)
    world.Initialise('world1.txt')       