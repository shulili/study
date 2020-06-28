import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
port = 0


def usage():
    print("Python NetCat\n")
    print("Usage: nc.py -t [target_host] -p [target_port]")
    print("-l --listen ")
    print("-c --command")
    print("-h --help")
    print("Examples: ")
    print("nc.py -t 127.0.0.1 -p 5555 -l -c")
    print("nc.py -t 127.0.0.1 -p 5555 ")
    sys.exit(0)


def main():
    global listen
    global command
    global upload
    global execute
    global target
    global port
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:c',
                                   ["help", "listen", "execute", "target", "port", "command"])
    except getopt.GetoptError as a:
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-c', '--command'):
            command = True
        else:
            assert False, "Unhandled Options"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.readline()
        client_sender(buffer)
    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))
    client.send(buffer.encode('utf-8'))
    while True:
        recv_len = 1
        response = b""
        while recv_len:
            data = client.recv(4096)
            recv_len = len(data)
            response += data
            if recv_len < 4096:
                break
        print(response.decode('utf-8'))
        buffer = sys.stdin.readline()
        client.send(buffer.encode('utf-8'))


def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.decode('utf-8')
    command = command.rstrip()
    print("" + command)
    if len(command):
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = b"[-] Faild to execute command. \r\n"
        return output
    else:
        output = b"[-] Faild to execute command. \r\n"
        return output


def client_handler(client_socket):
    global execute
    global command
    if command:
        cmd_buffer = client_socket.recv(1024)
        output = run_command(cmd_buffer)
        client_socket.send(output)
        while True:
            cmd_buffer = client_socket.recv(1024)
            output = run_command(cmd_buffer)
            client_socket.send(output)


if __name__ == '__main__':
    main()
