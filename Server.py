import socket
import threading
import json

IP = 'localhost'
PORT = 5555
clients = {}

def handle_client(conn, addr):
    print(f"Địa chỉ {addr} đã kết nối.")

    while True:
        username = conn.recv(1024).decode()
        if username in clients:
            conn.sendall("Tên người chơi đã tồn tại vui lòng nhập lại.".encode())
        else:
            clients[username] = {'conn': conn, 'in_game': False, 'opponent': None}
            conn.sendall("Tạo thành công người chơi.".encode())
            break
    
    try:
        while True:
            data = conn.recv(1024)
            message = json.loads(data.decode())
            opponent = message['opponent']

            if opponent not in clients:
                conn.sendall("Không tìm thấy đối thủ.".encode())
                continue

            if 'waiting' not in clients[opponent]:
                clients[opponent]['waiting'] = False

            if clients[opponent]['in_game']:
                conn.sendall("Đối thủ đang trong trận đấu.".encode())
                continue

            if clients[opponent]['waiting']:
                clients[username]['in_game'] = True
                clients[username]['opponent'] = opponent
                clients[username]['waiting'] = False

                clients[opponent]['in_game'] = True
                clients[opponent]['opponent'] = username
                clients[opponent]['waiting'] = False

                conn.sendall(f"Đã kết nối với đối thủ {opponent}. Trò chơi bắt đầu.".encode())
                clients[opponent]['conn'].sendall(f"Đã kết nối với đối thủ {username}. Trò chơi bắt đầu.".encode())
                print(f"{username} và {opponent} đã bắt đầu trò chơi.")

            else:
                clients[username]['waiting'] = True
                conn.sendall(f"Đối thủ {opponent} đang chờ kết nối. Hãy đợi cho đến khi họ tham gia.".encode())
            
            # Xử lý trận đấu
            while True:
                data = conn.recv(1024).decode()
                message = json.loads(data)
                opponent = message['opponent']
                self_move = message['move']

                if opponent in clients:
                    opponent_conn = clients[opponent]['conn']

                    opponent_conn.sendall(json.dumps({
                        'player': username,
                        'move': self_move
                    }).encode())

                    print(f"Đã gửi dữ liệu từ người chơi {opponent} đến {username}")

    finally:
        print(f"Người chơi {username} đã ngắt kết nối.")
        if clients[username]['opponent']:
            opponent = clients[username]['opponent']
            clients[opponent]['in_game'] = False
            clients[opponent]['opponent'] = None
            clients[opponent]['waiting'] = True
        del clients[username]
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print(f"Máy chủ hoạt động với địa chỉ: {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
