import socket
import threading

# ログを格納するリスト
server_log = []

# クライアントリスト（ソケットとアドレスのペア）
client_list = []

def handle_client(client_socket, client_address):
    try:
        print(f"[*] Connected!! [ Source: {client_address}]")
        # クライアントがサーバーに接続したら他のクライアントに通知
        join_message = f"join {client_address[0]}:{client_address[1]}".encode()
        broadcast_message(client_socket, join_message)

        while True:
            data = client_socket.recv(2048)
            if not data:
                break  # データがない場合は通信を終了
            data_str = data.decode()
            print(f"[*] Received Data from {client_address}: {data_str}")
            response = f"{client_address[0]}:{client_address[1]}:".encode() + data
            broadcast_message(client_socket, response)
    except ConnectionResetError:
        print(f"[*] Connection closed by {client_address}")
    finally:
        client_socket.close()
        # クライアントが "exit" したことを他のクライアントに通知
        exit_message = f"exit {client_address[0]}:{client_address[1]}".encode()
        broadcast_message(client_socket, exit_message)

def send_log_to_clients(client_socket):
    global server_log
    for log_entry in server_log:
        try:
            client_socket.send(log_entry.encode())
        except ConnectionResetError:
            print(f"[*] Connection closed by client")

def log_message(client_address, message):
    global server_log
    # メッセージを特定のフォーマットに整形
    formatted_message = f"{client_address[0]}:{client_address[1]} {message}\n"
    server_log.append(formatted_message)
    # ログが追加されたらクライアントにも送信
    send_log_to_clients(client_address)

def broadcast_message(sender_socket, message):
    for client_socket, _ in client_list:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except ConnectionResetError:
                print(f"[*] Connection closed by client")
                client_socket.close()

def accept_clients():
    while True:
        client_socket, address = tcp_server.accept()
        client_ip = address[0]
        client_list.append((client_socket, address))
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()
        print(f"[*] Accepted connection from: {client_ip}")

# サーバーの設定
server_ip = "127.0.0.1"
server_port = 9090

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((server_ip, server_port))
tcp_server.listen(5)

print(f"[*] Listening on {server_ip}:{server_port}")

# サーバーログ送信スレッドを起動
log_sender_thread = threading.Thread(target=send_log_to_clients, args=(tcp_server,))
log_sender_thread.start()

# クライアント受け入れスレッドを起動
accept_clients_thread = threading.Thread(target=accept_clients)
accept_clients_thread.start()

