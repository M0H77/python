"""
author: Mohammed Alhamadah
description: CSEC 201 lab2 part2
purpose: implementing SFMP protocol
"""
import socket
import time
import threading
import sys
import os

def handler(client_sock):
    while True:
        time.sleep(5)
        req = client_sock.recv(4096)
        print("client massage has been received: " + req.decode())
        put_req = req.decode().split("#")
        command = put_req[0]
        try:
            if command=="PUT":
                print("doing PUT...")
                destfile= put_req[1]
                msg = put_req[2]
                put(destfile,msg)
                print("PUT command completed successfully")
            elif command=="GET":
                print("doing GET...")
                sourcefile = put_req[1]
                msg =get(sourcefile).encode()
                client_sock.send(b"GET#"+msg)
                print("GET command completed successfully")
            elif command == "quit":
                client_sock.close()
                break
        except Exception as e:
            print("Failed to execute "+command+ " command : " + str(e))
            error_msg="ERROR#Failed to execute "+command+ " command : " + str(e)
            client_sock.send(error_msg.encode())



def start_server (port):
    server_sock = socket.socket()
    server_sock.bind(('',port))
    server_sock.listen()
    print("listening...")
    return server_sock


def put(destfile,msg):
    destfile=check_path(destfile)
    f = open(destfile, "w")
    f.write(msg)
    f.close()

def get(sourcefile):
    with open(sourcefile) as f:
        f = f.readlines()
        data_in_file = ""
        for line in f:
            data_in_file += line
    get_resp = data_in_file
    return get_resp

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
    try:
        port = int(sys.argv[1])
        server_sock = start_server(port)
        while True:
            client_sock, addr = server_sock.accept()
            client_handler = threading.Thread(target=handler, args=(client_sock,))
            client_handler.start()
    except:
        print("USAGE: python3 server.py port")


main()
# python3 server.py 55555