# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from copy import copy, deepcopy

class gameState:
    def __init__(self, map):
        """Game State consists of a grid, domain for each variable (assigned and unassigned)"""
        self.map = map
        self.assigned = self.formAssigned()
        self.domains = self.formDomain()
        self.unassigned = list(self.domains.keys())
        self.failure = False
        self.changeDomain()

    def formDomain(self):
        """Returns the initial domains in form of a dictionary"""
        domains = {}
        for x in range(0, 9):
            for y in range(0, 9):
                if (x, y) not in self.assigned:
                    domains[(x, y)] = []
                    for value in range(1, 10):
                        domains[(x, y)].append(value)
        return domains

    def formAssigned(self):
        """Returns the initial assigned variables as a list"""
        assigned = []
        for x in range(0, 9):
            for y in range(0, 9):
                if self.getValue((x, y)) != 0: assigned.append((x, y))
        return assigned

    def getValue(self, variable):
        """Returns the value of a variable"""
        x, y = variable
        return self.map[x][y]

    def changeValue(self, variable, value):
        """Changes the value of a variable, change the assigned list and domain dict"""
        x, y = variable
        self.assigned.append(variable)
        self.unassigned.remove(variable)
        del self.domains[variable]
        self.map[x][y] = value

    def getDomain(self, variable):
        """Returns the domain of a variable"""
        return self.domains[variable]

    def changeDomain(self):
        """Forward Check"""
        for variable in self.unassigned:
            values = self.getDomain(variable)
            newDomain = values.copy()
            for value in values:
                consistent = self.isConsistent(variable, value)
                if not consistent:
                    newDomain.remove(value)
            self.domains[variable] = newDomain

    def isFailure(self):
        for variable in self.unassigned:
            if len(self.getDomain(variable)) == 0: self.failure = True
            return False

    def nextVariable(self):
        minDomainSize = 10
        minVariable = None
        for variable in self.unassigned:
            domainSize = len(self.domains[variable])
            if domainSize < minDomainSize:
                minDomainSize = domainSize
                minVariable = variable
        return minVariable

    def isCompleted(self):
        for x in range(0, 9):
            for y in range(0, 9):
                if self.getValue((x, y)) == 0: return False
        return True

    def checkRow(self, location, value):
        x, y = location
        for columnNum in range(0, 9):
            if columnNum != x:
                if self.getValue((columnNum, y)) == value: return False
        return True

    def checkBox(self, location, value):
        groups = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        x, y = location
        for idx, group in enumerate(groups):
            if x in group: xIdx = idx
            if y in group: yIdx = idx

        for columnNum in groups[xIdx]:
            for rowNum in groups[yIdx]:
                if (x, y) != (columnNum, rowNum):
                    if self.getValue((columnNum, rowNum)) == value: return False
        return True

    def checkColumn(self, location, value):
        x, y = location
        for rowNum in range(0, 9):
            if rowNum != y:
                if self.getValue((x, rowNum)) == value: return False
        return True

    def isConsistent(self, location, value):
        const1 = self.checkRow(location, value)
        const2 = self.checkBox(location, value)
        const3 = self.checkColumn(location, value)
        return (const1 and const2 and const3)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

def backtrack(gameState):
    """Backtracking Algorithm"""
    if gameState.isCompleted(): return gameState
    variable = gameState.nextVariable()
    values = gameState.getDomain(variable)

    for value in values:
        if gameState.isConsistent(variable, value):
            new_gameState = deepcopy(gameState)
            new_gameState.changeValue(variable, value)
            new_gameState.changeDomain()

            if not new_gameState.isFailure():
                result = backtrack(new_gameState)
                if result != 0: return result
    return 0

def printGrid(result):
    print("End of the game, the result is \n")
    for i in range(0, 9):
        if (i % 3 == 0): print("-------------------------------------")
        for j in range(0, 9):
            if (j % 3 == 0):
                if j == 0:
                    print("|", end="  ")
                    print(result.map[i][j], end="  ")
                else:
                    print("|", end="  ")
                    print(result.map[i][j], end="  ")
            else:
                if j == 8:
                    print(result.map[i][j], end="  ")
                    print("|", end="")
                else:
                    print(result.map[i][j], end="  ")
        print()
        if i == 8: print("-------------------------------------")

if __name__ == '__main__':
    map = [[0, 8, 0, 0, 0, 0, 3, 0, 9],
           [0, 0, 0, 0, 6, 2, 0, 0, 5],
           [0, 1, 0, 0, 0, 7, 0, 0, 0],
           [0, 0, 0, 0, 7, 1, 0, 0, 0],
           [9, 2, 3, 0, 0, 0, 6, 0, 0],
           [0, 6, 0, 0, 0, 0, 5, 4, 0],
           [2, 5, 0, 8, 0, 9, 0, 0, 0],
           [0, 0, 0, 1, 5, 0, 9, 3, 2],
           [4, 0, 9, 0, 0, 0, 0, 0, 0]]

    game = gameState(map)

    result = backtrack(game)

    if result != 0:
        printGrid(result)
    else:
        print("Sudoku is unsolvable!")
