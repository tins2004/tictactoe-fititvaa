import socket
import json
import numpy as np

IP = 'localhost'
PORT = 5555

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.opponent = None

    def connect(self):
        try:
            self.client.connect((IP, PORT))
        except:
            return None
    
    def close(self):
        self.client.close()
    
    def inputUsername(self, username):
        self.username = username
        self.client.sendall(self.username.encode())
        response = self.client.recv(1024).decode()
        if response == "Tên người chơi đã tồn tại vui lòng nhập lại.":
            print("Tên người chơi đã tồn tại vui lòng nhập lại.")
            return False
        elif response == "Tạo thành công người chơi.":
            print("Tạo thành công người chơi.")
            return True

    def inputOpponent(self, opponent):
        if opponent == self.username:
            print("Không thể nhập tên chính người chơi.")
            return False
        message = json.dumps({'opponent': opponent})
        self.client.sendall(message.encode())

        while True:
            response = self.client.recv(1024).decode()
            if response == "Không tìm thấy đối thủ.":
                print("Không tìm thấy đối thủ.")
                return False
            elif response == "Đối thủ đang trong trận đấu.":
                print("Đối thủ đang trong trận đấu.")
                return False
            else:
                print(f"Đối thủ {opponent} đang chờ kết nối. Hãy đợi cho đến khi họ tham gia.")
                if response == f"Đã kết nối với đối thủ {opponent}. Trò chơi bắt đầu.":
                    print(f"Đã kết nối với đối thủ {opponent}. Trò chơi bắt đầu.")
                    self.opponent = opponent
                    return True

    def makeMove(self, row, col):
        try:
            message = {
                'opponent': self.opponent,
                'move': [row, col]
            }
            self.client.sendall(json.dumps(message).encode())
        except ValueError:
            print("Vui lòng nhập tọa độ hợp lệ (row col).")

    def updateMove(self):
        data = self.client.recv(4096).decode()
        if not data:
            print("Kết nối đã ngắt.")
            return
        try:
            print(data)
            message = json.loads(data)
            print(f"Đối thủ {message['player']} vừa di chuyển.")
            opponent_move = np.array(message['move'])
            return opponent_move
        except json.JSONDecodeError as e:
            print(f"Lỗi phân tích JSON: {e}")
