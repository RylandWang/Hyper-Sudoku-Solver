# Given a hypersudoku grid, either outputs a filled grid solution or None if no valid solutions found.
# Note: Input sudoku grid must be defined as a 9x9 matrix (2d array)

import time
from subprocess import *
import sys, io

class HyperSudoku:
    
    @staticmethod
    def checkPossibilities(grid, i, j):
        """
        Given a 2d-list grid and index of a single entry, return a list of 
        all possible values for the entry.
        """
        possibilities = {}
        
        # assume all possiblities valid by default
        for num in range(1,10):
            possibilities[num] = True
        
        # ____check row to determine possible values____
        for x in range (9):
            # eliminate option if vlaue exists in row
            if grid[x][j] != 0:
                possibilities[grid[x][j]] = False
        
        # ____check column to determine possible values____
        for y in range (9):
            # eliminate option if value exists in column
            if grid[i][y] != 0:
                possibilities[grid[i][y]] = False
        
        # ___check 3x3 normal block for possible values____
        
        # define range of corresponding 3x3 normal block
        starti = i - (i % 3)
        endi = i + (2 - (i % 3)) +1
        
        startj = j - (j % 3)
        endj = j + (2 - (j % 3)) +1
        
        #check possibitlies within normal block
        for x in range(starti, endi):
            for y in range(startj, endj):
                # eliminate possiblity if value exists in regular block
                if grid[x][y] != 0:
                    possibilities[grid[x][y]] = False
        
        # ____check 3x3 hyper block for possible values____
        
        # if entry exists inside a hyper block
        if str(i) in "123567" and str(j) in "123567":
            
            # define range of corresponding 3x3 hyper block
            if i <= 3:
                starti = 1
                endi = 4
            elif i <= 7:
                starti = 5
                endi = 8
            
            if j <= 3:
                startj = 1
                endj = 4
            elif j <= 7:
                startj = 5
                endj = 8
                
            # check possibitlies within hyper block
            for x in range(starti, endi):
                for y in range(startj, endj):
                    if grid[x][y] != 0:
                        possibilities[grid[x][y]] = False
                        
        return possibilities
        
    def isSolved(grid):
        '''
        Returns true if a Sudoku grid is fully solved
        '''
        result = True
        # check for 0 within grid
        # if at least one 0 exists, return false
        for i in range(len(grid[0])):
            exit = False
            for j in range(len(grid)):
                if grid[i][j] == 0:
                    result = False
                    exit = True
                    break
            if exit:
                break
            
        return result
                
    
    def solver_function(grid):
        """
        Provides solutions for a given Sudoku grid, returns as matrix of values
        in string form.
        
        Called by solve() to convert to 2-d list form.
        """
        solved = False
        if not HyperSudoku.isSolved(grid):
           
            i = 0
            j = 0
            
            # find indexes of next "0" entry
            for i in range(9):
                exit = False
                for j in range(9):
                    if grid[i][j] == 0:
                        exit = True
                        break
                if exit:
                    break
            
            # check all possibilities at entry
            possibilities = HyperSudoku.checkPossibilities(grid, i, j)
            
            # recursively explore all possibitlies
            for num in range(1,10):
                if possibilities[num]:
                    grid[i][j] = num
                    grid = HyperSudoku.solver_function(grid)
            
            # a violation occurs at this point
            # backtrack to explore other possiblities
            grid[i][j] = 0
        
        # fully solved
        else:
            print(grid)
        
        return grid        
        
    @staticmethod
    def solve(grid):
        """
        Input: An 9x9 hyper-sudoku grid with numbers [0-9].
                0 means the spot has no number assigned.
                grid is a 2-Dimensional array. Look at
                Test.py to see how it's initialized.

        Output: A solution to the game (if one exists),
                in the same format. None of the initial
                numbers in the grid can be changed.
                'None' otherwise.
        """
        # defined new grid to store values of solved grid
        solved_grid = []
        for i in range(9):
            solved_grid.append([])
        
        stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        # call solver function
        HyperSudoku.solver_function(grid)
        # capture stdout as string
        output = sys.stdout.getvalue()
        sys.stdout = stdout
       
        nums_visited = 0
        row= 0
         # manually store each integer value from grid string to list
        for char in output:
            if char in "0123456789":
                solved_grid[row].append(int(char))
                nums_visited += 1
                if nums_visited % 9 == 0:
                    row += 1
        
        # if list is empty, ie unsolvable grid
        if len(solved_grid[0]) == 0:
            solved_grid = None
                      
        return solved_grid
      
    @staticmethod
    def printGrid(grid):
        """
        Prints out the grid in a nice format. Feel free
        to change this if you need to, it will NOT be 
        used in marking. It is just to help you debug.

        Use as:     HyperSudoku.printGrid(grid)
        """
        print("-"*25)
        for i in range(9):
            print("|", end=" ")
            for j in range(9):
                print(grid[i][j], end =" ")
                if (j % 3 == 2): 
                    print("|", end=" ")
            print()
            if (i % 3 == 2):
                print("-"*25)
