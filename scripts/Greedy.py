import numpy as np
import random

# Hàm đánh giá tiềm năng của một ô trống
def evaluate_position(row, col, board, player):
    directions = [
        [0, 1],  # Ngang
        [1, 0],  # Dọc
        [1, 1],  # Chéo trái sang phải
        [1, -1], # Chéo phải sang trái
    ]
    max_score = 0
    for dx, dy in directions:
        count = 1
        blocks = 0
        
        # Đếm về phía trước
        for i in range(1, 5):
            x, y = row + dx * i, col + dy * i
            if 0 <= x < 19 and 0 <= y < 19:
                if board[x, y] == player:
                    count += 1
                elif board[x, y] == -player:
                    blocks += 1
                    break
                else:
                    break
            else:
                blocks += 1
                break
        
        # Đếm về phía sau
        for i in range(1, 5):
            x, y = row - dx * i, col - dy * i
            if 0 <= x < 19 and 0 <= y < 19:
                if board[x, y] == player:
                    count += 1
                elif board[x, y] == -player:
                    blocks += 1
                    break
                else:
                    break
            else:
                blocks += 1
                break
        
        # Tính điểm
        if blocks == 2:
            score = 0  # Bị chặn hai đầu
        else:
            score = count
        
        max_score = max(max_score, score)
    
    return max_score

# Hàm tìm các nước đi tốt nhất
def get_best_points(board, player):
    max_attack_score = float('-inf')
    max_defense_score = float('-inf')
    best_attack_points = []
    best_defense_points = []
    
    for i in range(19):
        for j in range(19):
            if board[i, j] == 0:
                attack_score = evaluate_position(i, j, board, player)
                defense_score = evaluate_position(i, j, board, -player)
                
                if attack_score > max_attack_score:
                    max_attack_score = attack_score
                    best_attack_points = [(i, j)]
                elif attack_score == max_attack_score:
                    best_attack_points.append((i, j))
                
                if defense_score > max_defense_score:
                    max_defense_score = defense_score
                    best_defense_points = [(i, j)]
                elif defense_score == max_defense_score:
                    best_defense_points.append((i, j))
    
    if max_attack_score >= max_defense_score:
        return best_attack_points
    else:
        return best_defense_points

# Hàm lấy nước đi cho AI
def get_computer_move_greedy(board, player):
    best_points = get_best_points(board, player)
    return random.choice(best_points)


