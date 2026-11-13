from socket import *
import threading
import sys

def handle_client(connectionSocket):
    print(f"[{threading.current_thread().name}] Serving {connectionSocket.getpeername()}")
    try:
        message = connectionSocket.recv(1024).decode()
        if not message:
            connectionSocket.close()
            return

        filename = message.split()[1]
        with open(filename[1:], "r") as f:
            outputdata = f.read()

        connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 6789
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)  # Allow a backlog of queued connections

    print('CSNETWK Multithreaded Web Server is ready to serve...')

    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        serverSocket.close()
        sys.exit()


if __name__ == "__main__":
    main()