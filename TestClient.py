from scripts.Client import Client

if __name__ == '__main__':
    client = Client()
    client.connect()
    while True:
        username = input("Enter your username: ")
        if client.inputUsername(username):
            break
        else:
            continue
    
    
    while True:
        opponent = input("Enter your opponent's username: ")
        if client.inputOpponent(opponent):
            break
        else:
            continue

    try:
        while True:
            row, col = map(int, input("Enter your move (row col): ").split())
            client.makeMove(row, col)
            client.updateMove()
    except KeyboardInterrupt:
        print("Disconnected from server.")
        client.close()

