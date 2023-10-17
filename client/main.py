import socket
import threading

def receive_messages(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(2048)
            if not data:
                break
            message = data.decode()
            # クライアント自身が送信したメッセージを除外
            if not message.startswith(f"{client_address[0]}:{client_address[1]}:"):
                print(message + "\n: ")
    except ConnectionResetError:
        print("[*] Connection closed by server")

def ip_port():
    server_ip = "127.0.0.1"
    server_port = 9090

    print("please choose default:(d) or your setting:(s)")
    choose = input(": ")

    if choose == "d":
      return (server_ip, server_port)

    elif choose == "s":
      print("please write ip")
      server_ip = input(": ")
      print("please write port")
      server_port = int(input(": "))
      return (server_ip, server_port)

    else:
      return ip_port()

def main():
    ip_port_tmp = ip_port()
    server_ip = ip_port_tmp[0]
    server_port = ip_port_tmp[1]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    client_address = client_socket.getsockname()  # クライアントのアドレスを取得

    # サーバーからのメッセージを受信するスレッドを開始
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_address))
    receive_thread.start()

    print("Enter a message ('exit' to quit)")
    while True:
        message = input(": ")
        if message == "exit":
            client_socket.send(message.encode())
            break
        # メッセージをサーバーに送信
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    main()

