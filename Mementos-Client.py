import socket
import threading

header=64
format='utf-8'
disconnect_message="!leave"

def send(msg):
 message=msg.encode(format)
 message_length=len(message)
 send_length=str(message_length).encode(format)
 send_length+=b' '*(header-len(send_length))
 client.send(send_length)
 client.send(message)

def msg_send_func():
 while True:
  msg=input('')
  send(msg)

def msg_receive_func():
 while True:
  msg_length=client.recv(header).decode(format)
  if msg_length:
    msg_length=int(msg_length)
    msg=client.recv(msg_length).decode(format)    
    print(f"{msg}")
    
server=input("Enter IP address ")
port=input("Which port ? ")
addr=(server, int(port))
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

nickname=input("What is your nickname ? ")
send('!firstnickname '+str(nickname))
msg_send=threading.Thread(target=msg_send_func)
msg_receive=threading.Thread(target=msg_receive_func)
msg_send.start()
msg_receive.start()