#İlker Kara, 24.12.2019

import math     #For angle calculation, I use the arctan2 function from math module


class Maze:
    # Member functions and variables
    # All member variables are created with constructor
    def __init__(self, info):   # Constructor of Maze class
        self.walls = []
        self.other_information = {}

        for key in info.keys():  # For parsing the information(info variable-dictionary) that sent to the constructor
            if type(key) == tuple:
                self.walls.append(key)
            elif type(key) == str:
                self.other_information = info[key]

        self.num_rows = self.other_information['rows']
        self.num_cols = self.other_information['columns']
        self.start = self.other_information["start"]
        self.end = self.other_information["end"]

        self.maze_map = [[' ' for _ in range(self.num_cols)] for _ in range(self.num_rows)] # For creating blank maze map & map contains ' ' character

        for wall in self.walls:     # For placing the walls into the maze map
            i = wall[0]
            j = wall[1]
            self.maze_map[i][j] = 'w'

        self.maze_map[self.start[0]][self.start[1]] = "s"       # For placing the start point into the maze map
        self.maze_map[self.end[0]][self.end[1]] = "e"           # For placing the end point into the maze map

    # Member print function for printing the maze map at any time
    def print(self):
        for j in range(self.num_cols):      # To number columns & more readable output
            print("   ", j, end="")
        print()
        i = 0   # To number rows & more readable output
        for row in self.maze_map:
            print(i,row)
            i += 1

    # Member moveup function for moving up in the maze if possible
    def moveup(self,pos,pathMatrix):
        # All If statement's of move functions controls that 'Is the next position is in the map, not a wall' and 'Did I use this cell before'
        if 0 < pos[0] and pos[0]-1 < self.num_rows and self.maze_map[pos[0] - 1][pos[1]] != "w" and (pos[0] - 1, pos[1]) not in pathMatrix:
            print("UP")
            pos[0] -= 1
            pathMatrix.append((pos[0], pos[1]))     # If I can go to the next position without any problem, I should record this cell in pathMatrix variable
            # self.maze_map[pos[0] + 1][pos[1]] = "˄"
            return True
        else:
            return False

    # Member movedown function for moving down in the maze if possible
    def movedown(self,pos,pathMatrix):
        if pos[0] + 1 < self.num_rows and self.maze_map[pos[0] + 1][pos[1]] != "w" and (pos[0] + 1, pos[1]) not in pathMatrix:
            print("DOWN")
            pos[0] += 1
            pathMatrix.append((pos[0], pos[1]))
            # self.maze_map[pos[0]-1][pos[1]] = "˅"
            return True
        else:
            return False

    # Member moveleft function for moving left in the maze if possible
    def moveleft(self,pos,pathMatrix):
        if pos[1] > 0 and pos[1] - 1 < self.num_cols and self.maze_map[pos[0]][pos[1] - 1] != "w" and (pos[0], pos[1] - 1) not in pathMatrix:
            print("LEFT")
            pos[1] = pos[1] - 1
            pathMatrix.append((pos[0], pos[1]))
            # self.maze_map[pos[0]][pos[1]+1] = "<"
            return True
        else:
            return False

    # Member moveright function for moving right in the maze if possible
    def moveright(self,pos,pathMatrix):
        if pos[1] + 1 < self.num_cols and self.maze_map[pos[0]][pos[1] + 1] != "w" and (pos[0], pos[1] + 1) not in pathMatrix:
            print("RIGHT")
            pos[1] += 1
            pathMatrix.append((pos[0], pos[1]))
            # self.maze_map[pos[0]][pos[1]-1] = ">"
            return True
        else:
            return False

    # Member calculatedirection for  direction prediction with weights
    def calculatedirection(self,pos,direction):
        # Calculation of distance between the current position and the end point for each axis
        # Maze map is located in the 4th region not in the 1st region of cartesian coordinate system. Therefore, it is needed to convert x,y coordinates for calculation of angle
        X = pos[1] - self.end[1]
        Y = (-pos[0]) - (-self.end[0])

        # Calculation of the angle of the line passing through the current position and the end point
        r = math.atan2(Y, X)
        d = r * 180 / math.pi
        d += 180
        d %= 360

        print(d)

        # Direction prediction with angle
        arr = [[0 for j in range(3)] for i in range(3)]

        x = 135
        for i in range(3):
            for j in range(3):
                if i % 2 == 0:
                    arr[i][j] = x
                    x += 45 * (i - 1)
                else:
                    arr[i][j] = x
                    x -= 90
                arr[i][j] = abs(arr[i][j] - d) / 360
            if i % 2 == 0:
                x += 180
            else:
                x += 315
        arr[1][1] = -1

        print(arr)

        movements = (self.moveup, self.moveleft, self.moveright, self.movedown)
        iter = 0

        for i in range(3):
            for j in range(3):
                if not (i % 2 == 0 and j % 2 == 0) and (i, j) != (1, 1):
                    # print(arr[i][j])
                    if arr[i][j] in direction.keys():
                        arr[i][j] += 0.001              # For unique key and prevent overwriting
                    direction[arr[i][j]] = movements[iter]
                    iter += 1

        print(direction.keys())

        weights = sorted(list(direction.keys()), key = float)
        print(weights)
        return weights

    # Member findPath function for finding path from start to end and it tries to find the shortest path if possible
    def findPath(self):
        pos = list(self.start)    # First position is start point

        pathMatrix = []           # pathMatrix variable contains the cells that we travel
        pathMatrix.append(self.start)       # It starts with the start point to travelling

        # Direction prediction with angle
        direction = {}
        weights = self.calculatedirection(pos, direction)

        found = self.maze_map[pos[0]][pos[1]] == "e"

        # while self.maze_map[pos[0]][pos[1]] != "e":
        while not found:

            # Trying to move in order to calculated weights and their directions
            for weight in weights:
                print(direction[weight])
                if direction[weight](pos, pathMatrix):
                    break
            #   Direction prediction with angle
            direction = {}
            weights = self.calculatedirection(pos, direction)

            found = self.maze_map[pos[0]][pos[1]] == "e"

        # self.maze_map[self.start[0]][self.start[1]]="s"
        self.print()
        return pathMatrix

    def shortest(self,pos):
        if self.maze_map[pos[0]][pos[1]] == "e":
            return True
        else:
            return False


def main():

    map_information ={
        (0, 1): "W", (3, 1): "W", (3, 3): "W", (3, 4): "W",
        "information": {"rows": 5, "columns": 5, "start": (0, 4), "end": (4, 2)}
    }

    map_information ={
        (1, 1): "W", (2, 3): "W", (1, 3): "W", (0, 3): "W", (0, 1): "W", (0, 5): "W", (4, 3): "W", (2, 7): "W", (5, 7): "W", (5, 6): "W",
        "information": {"rows": 6, "columns": 8, "start": (2, 1), "end": (0, 7)}
    }

    maze = Maze(map_information)    # maze object created from Maze class with map_information

    maze.print()                    # maze map printed
    path = maze.findPath()

    print("Path: ", path)
    print("Length of path: ", len(path))


if __name__ == "__main__":
    main()