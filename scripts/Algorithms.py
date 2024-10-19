import time
import random
from scripts.AStar import *
from scripts.Greedy import *


def show(matrix):
    print(matrix)


def timePause(indexTime):
    start_time = time.time()
    while True:
        cur_time = time.time()
        elapsed_time = cur_time - start_time

        if elapsed_time >= indexTime:
            break


def convertSecondsToTime(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return int(hours), int(minutes), int(seconds)

# viết thuật toán ở đây ---------------------------------------------------------------------------------
# thuật toán gì đấy kết quả trả về là vị trí hàng nào cột số bao nhiêu


def greedy(matrix, machineRule):
    print("miniMax")
    while True:
        row, col = get_computer_move_greedy(matrix, machineRule)
        if matrix[row][col] == 0:
            return col, row
    # print(result)
    return 0, 0


def AStar(matrix, machineRule):
    print("A*")
    while True:
        row, col = CptFindChessAStar(matrix, machineRule)
        if matrix[row][col] == 0:
            return col, row
    # print(result)
    return 0, 0


# viết hàm khiểm tra thử ai chiến thắng nếu X thắng thì trả False nếu O thắng thì trả True nếu chưa kết thúc thỉ trả None
def checkWinner(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if j <= len(matrix[i]) - 5:
                if sum(matrix[i][j+k] for k in range(5)) == 5:
                    print("O wins")
                    return 1
                elif sum(matrix[i][j+k] for k in range(5)) == -5:
                    print("X wins")
                    return -1

            if i <= len(matrix) - 5:
                if sum(matrix[i+k][j] for k in range(5)) == 5:
                    print("O wins")
                    return 1
                elif sum(matrix[i+k][j] for k in range(5)) == -5:
                    print("X wins")
                    return -1

    # Kiểm tra đường chéo chính
    for i in range(len(matrix) - 4):
        for j in range(len(matrix[i]) - 4):
            if sum(matrix[i+k][j+k] for k in range(5)) == 5:
                print("O wins")
                return 1
            elif sum(matrix[i+k][j+k] for k in range(5)) == -5:
                print("X wins")
                return -1

    # Kiểm tra đường chéo phụ
    for i in range(len(matrix) - 4):
        for j in range(4, len(matrix[i])):
            if sum(matrix[i+k][j-k] for k in range(5)) == 5:
                print("O wins")
                return 1
            elif sum(matrix[i+k][j-k] for k in range(5)) == -5:
                print("X wins")
                return -1
    
    # if np.any(matrix):
    #     return 0

