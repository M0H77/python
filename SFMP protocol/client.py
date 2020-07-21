"""
author: Mohammed Alhamadah
description: CSEC 201 lab2 part2
purpose: implementing SFMP protocol
"""
import socket
import sys
import os
def put(sourcefile, destfile):
    with open(sourcefile) as f:
        f = f.readlines()
        data_in_file = ""
        for line in f:
            data_in_file += line
    req_msg = "PUT#"+destfile+"#"+data_in_file
    return req_msg

def get(client_sock, sourcefile, destfile):

    get_msg = "GET#" + sourcefile      # request source file data from server
    client_sock.send(get_msg.encode())

    get_resp = client_sock.recv(4096).decode().split("#")  # receive source file data from server


    if get_resp[0] == "ERROR":  # check if the server sent an error message
        print(get_resp[1])
    else:
        # print(get_resp[1])
        destfile = check_path(destfile)
        f = open(destfile, "w")        # write data to dest file
        f.write(get_resp[1])
        f.close()
        print("GET command completed successfully")

def check_path(destfile):
    path=destfile
    path = path.split("/")
    joined_path = ''
    for i in range(len(path)-1):
        joined_path = joined_path + path[i] + "/"

    if os.path.isdir(joined_path):
        return destfile
    else:
        joined_path=joined_path[1:]
        directory = "."+joined_path
        os.mkdir(directory)
        return destfile

def main():
    # port = 55555
    # client_sock = socket.socket()
    # client_sock.connect(('localhost', port))
    #
    # put_msg = put_client("hello.txt", "hello2.txt")
    # client_sock.send(put_msg.encode())
    #
    # GET(client_sock, "hello.txt", "hello2.txt")


    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        client_sock = socket.socket()
        client_sock.connect((ip, port))
        while True:
            try:
                user_input = str(input("Enter command> "))
                command = user_input.split()[0]
                if command=="quit":
                    print("bye..")
                    client_sock.send(b"quit")
                    break
                sourcefile = user_input.split()[1]
                destfile = user_input.split()[2]
                if command == "PUT":
                    print("transferring file to server...")
                    put_msg = put(sourcefile, destfile)
                    client_sock.send(put_msg.encode())
                    print("PUT command completed successfully")

                elif command == "GET":
                    print("retrieving file from server...")
                    get(client_sock, sourcefile, destfile)

                else:
                    print("illegal input\nusage:\n    PUT/GET sourcefile destfile\n    type 'quit' to exit")
            except FileNotFoundError as e:
                print("Failed to execute " + command + " command: " + str(e))
            except:
                print("illegal input\nusage:\n    PUT/GET sourcefile destfile\n    type 'quit' to exit")
    except:
        print("USAGE: python3 client.py ip port")

main()






