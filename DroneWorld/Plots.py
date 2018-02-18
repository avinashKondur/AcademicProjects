from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


class PlotPath:
    def __init__(self, grid,path):
        self._pathFound = path
        self._grid = grid

    def showPath(self):
        fig = plt.figure(figsize=(10, 10), facecolor='w')

        ax = fig.add_subplot(111, projection='3d')
        xcoord,ycoord,zcoord,colour=self.__calcCoor()

        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        ax.set_zlim(0, 50)
        ax.set_xlabel("X Coordinates")
        ax.set_ylabel("Z Coordinates")
        ax.set_zlabel("Y Coordinates")

        for i in self._pathFound:
            i[0]-=50
            i[2]-=50
        xs, ys, zs = zip(*self._pathFound)
        ax.plot(xs, zs, ys, 'o-', lw=2, color='black', ms=1)
        ax.scatter(xcoord, zcoord, ycoord, c=colour, marker='s')
        ax.set_title("Path followed by Drone")
        black_patch = mpatches.Rectangle((0,0),0.1,0.1,color='black', label='Drone Position')
        plt.legend(handles=[black_patch])
        ax.grid(True)
        plt.show()

    def __calcCoor(self):

        colour = np.array([])

        nGrid = np.asarray(self._grid)
        xcoord, ycoord, zcoord = np.where(nGrid != '')

        indices = [[x, y, z] for x, y, z in zip(*(xcoord, ycoord, zcoord))]
        for p in indices:
            if nGrid[p[0]][p[1]][p[2]][0]=='D':
                colour=np.append(colour,'black')
            else:
                colour=np.append(colour,nGrid[p[0]][p[1]][p[2]])
        xcoord -= 50
        zcoord -= 50
        return (xcoord,ycoord,zcoord,colour)

