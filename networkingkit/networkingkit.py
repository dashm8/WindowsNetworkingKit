import os
import socket
import time
import ssh_paramiko

def netcat(inp):
    try:
        addr = inp.split(" ")[1]
        port = inp.split(" ")[2]
    except Exception:
        print("[!] useage nc <address> <port>")
    try:
        sock = socket.socket()
        sock.connect((addr,int(port)))
        while 1:
            senddata = input(">")
            if senddata == "exit": sock.close(); break
            sock.send(senddata)
            data = sock.recv(1024)
            print(repr(data))
    except Exception as e:
        print(e)

def netcatserver(inp):
    try:
        port = int(inp.split(' ')[1])
    except Exception:
        print("[!] useage ncserver <port>")
    try:
        sock = socket.socket()
        sock.bind(('0.0.0.0',port))
        sock.listen(1)
        conn , addr = sock.accept()
        while 1:
            data = conn.recv(1024)
            if not data: break
            senddata = input(">")
            if senddata == "exit": break
            conn.sendall(senddata)
        conn.close()
    except Exception as e:
        print(e)

def ssh(inp):
    try:
        rs = ssh_paramiko.RemoteServer()
        rs.password = inp.split(' ')[2]
        rs.username = (inp.split('@')[0])[4:]
        rs.connect_server(inp.split('@')[1].split(' ')[0],False)
    except Exception:
        print("[!] usage ssh <username>@<server> <password>")
    try:
        while 1:
            cmd = input(">")
            if cmd == "exit": break
            rs.execute_cmd(cmd)
    except Exception as e:
        print(e)


def handler(inp):
    inp = str(inp)
    if inp.startswith("ssh"):
        ssh(inp)
        return None
    if inp.startswith("nc"):
        netcat(inp)
        return None
    if inp.startswith("ncserver"):
        netcatserver(inp)
        return None

    
def Console():
    while 1:
        handler(input(">"))
        time.sleep(0.5)


