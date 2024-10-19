import numpy as np
import time

class TicTacToe:
    def __init__(self, matrix, isMachine, playerRule):
        if matrix == 0:
            self.matrix = np.zeros((19, 19))
        else:
            self.matrix = matrix
        
        self.isMachine = isMachine
        self.curRule = -1
        self.playerRule = playerRule
        self.score = [0, 0]
        self.history = []
        self.suggest = False
        self.algorithms = 1
  
    def setMatrix(self, pos_row, pos_col, value):
        self.matrix[pos_row][pos_col] = value

    def getMatrix(self):
        return self.matrix
    
    def resetMatrix(self):
        self.matrix = np.zeros((19, 19))

    def changeMatrix(self, matrix):
        self.matrix = np.asarray(matrix)

    def setIsMachine(self, isMachine):
        self.isMachine = isMachine
    
    def getIsMachine(self):
        return self.isMachine

    def setRule(self, curRule):
        self.curRule = curRule
    
    def getRule(self):
        return self.curRule
    
    def changeRule(self, curRule):
        self.curRule *= -1
    
    def setPlayerRule(self, playerRule):
        self.playerRule = playerRule
    
    def getPlayerRule(self):
        return self.playerRule
    
    def setMiniTime(self, timeValue):
        if timeValue != None:
            self.start_mini_time = timeValue
        else:
            self.start_mini_time = time.time()

    def getMiniTime(self):
        return self.start_mini_time
    
    def setTime(self, timeValue):
        if timeValue != None:
            self.start_time = timeValue
        else:
            self.start_time = time.time()

    def getTime(self):
        return self.start_time
    
    def setScore(self, score):
        self.score = score

        if self.score[0] > 9:
            self.score[0] = 0 
        if self.score[1] > 9:
            self.score[1] = 0 

    def getScore(self):
        return self.score
    
    def addHistory(self, posMatrix):
        self.history.append(posMatrix)
    
    def getHistory(self):
        if self.history == []:
            return None, None
        
        if self.isMachine:
            if len(self.history) < 2:
                return None, None
            tempx = self.history[-1]
            del self.history[-1]
            tempo = self.history[-1]
            del self.history[-1]
            
            return tempx, tempo
        
        if self.curRule == 1:
            temp = self.history[-1]
            del self.history[-1]
            
            return temp, None
        else:
            tempo = self.history[-1]
            del self.history[-1]
            return None, tempo

    def getSuggest(self):  
        return self.suggest
    
    def setSuggest(self, status):
        self.suggest = status
    
    def getAlgorithms(self):
        return self.algorithms
    
    def setAlgorithms(self, algorithms):
        self.algorithms = algorithms