import socket
import threading
word_list=('angle','knee','ant','knife','apple','knot','arch','leaf','arm','leg','army','library','baby','line','bag','lip','ball','lock','band','map','basin','match','basket','monkey','bath','moon','bed','mouth','bee','muscle','bell','nail','berry','neck','bird','needle','blade','nerve','board','net','boat','nose','bone','nut','book','office','boot','orange','bottle','oven','box','parcel','boy','pen','brain','pencil','brake','picture','branch','pig','brick','pin','bridge','pipe','brush','plane','bucket','plate','bulb','plough','button','pocket','cake','pot','camera','potato','card','prison','carriage','pump','cart','rail','cat','rat','chain','receipt','cheese','ring','chess','rod','chin','roof','church','root','circle','sail','clock','school','cloud','scissors','coat','screw','collar','seed','comb','sheep','cord','shelf','cow','ship','cup','shirt','curtain','shoe','cushion','skin','dog','skirt','door','snake','drain','sock','drawer','spade','dress','sponge','drop','spoon','ear','spring','egg','square','engine','stamp','eye','star','face','station','farm','stemfeather','stick','finger','stocking','fish','stomach','flag','store','floor','street','fly','sun','foot','table','fork','tail','fowl','thread','frame','throat','garden','thumb','girl','ticket','glove','toe','goat','tongue','gun','tooth','hair','town','hammer','train','hand','tray','hat','tree','head','trousers','heart','umbrella','hook','wall','horn','watch','horse','wheel','hospital','whip','house','whistle','island','window','jewel','wing','kettle','wire','key','worm')
#199 words
import random

header=64
port=5051
server=socket.gethostbyname(socket.gethostname())
addr=(server,port)
format='utf-8'
disconnect_message="!leave"

hangman=False
hangman_word=''
hangman_tries=0
Hangman_characters=[]

codenames=False
codenames_blue_op=0
codenames_red_op=0
codenames_turn='Red'
codenames_word_list=[]
class codenames_word():
 def __init__(self,word):
  self.word=word
  self.hidden_colour='\033[30m'
  self.open_colour='\033[30m'

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)

def send(msg):
 message=msg.encode(format)
 message_length=len(message)
 send_length=str(message_length).encode(format)
 send_length+=b' '*(header-len(send_length))
 for i in range(len(conns)):
  try:
   conns[i].send(send_length)
   conns[i].send(message)
  except:
   pass

def handle_client(conn, addr, number):
 print(f"[CONNECTION FROM] {addr}")
 global conns
 conns.append(conn)
 global nicknames
 nicknames.append(addr)
 global hangman
 global hangman_word
 global hangman_tries
 global hangman_characters
 
 connected=True 
 while connected:
  msg_length=conn.recv(header).decode(format)
  if msg_length:
   msg_length=int(msg_length)
   msg=conn.recv(msg_length).decode(format)
   
   print(f"[{addr}] {msg}")
   
   if msg==disconnect_message:
    connected=False
    break
    
   
   if msg[:10]=='!nickname ':
    send(f"{addr}'s nickname is now {msg[10:]}")
    addr=msg[10:]
    nicknames[number]=addr
    
   elif msg[:15]=='!firstnickname ':
    addr=msg[15:]
    send(f"{addr} has joined the chat")
    nicknames[number]=addr
   
   elif msg[:5]=='!uwu ':
    msg=list(msg[5:])
    for i in range(len(msg)):
     if msg[i]=='r' or msg[i]=='l':
      msg[i]='w'
     elif msg[i]=='R' or msg[i]=='L':
      msg[i]='W'
    msg="".join(msg)
    send(f"[{addr}] {msg}")
    
   elif msg[:9]=='!hangman ':
    hangman_word=msg[9:]
    message='How many tries ?'.encode(format)
    message_length=len(message)
    send_length=str(message_length).encode(format)
    send_length+=b' '*(header-len(send_length))
    conn.send(send_length)
    conn.send(message)
    while True:
     msg_length=conn.recv(header).decode(format)
     if msg_length:
      msg_length=int(msg_length)
      msg=conn.recv(msg_length).decode(format)
      try:
       hangman_tries=int(msg)
       break
      except:
       message='Not a number'.encode(format)
       message_length=len(message)
       send_length=str(message_length).encode(format)
       send_length+=b' '*(header-len(send_length))
       conn.send(send_length)
       conn.send(message)
    send(f"We are now playing Hangman with {hangman_tries} tries, {addr} is hosting")
    hangman_characters=[]
    for i in range(len(hangman_word)):
     hangman_characters.append("_")
    send('')
    send('')
    send('')
    send("".join(hangman_characters))
    hangman=True
    
   elif msg[:10]=='!codenames':
    send("We are now playing Codenames")
    game_codenames(conn,msg[10:])
     
   else:
     if hangman==True:
      send(f"[{addr}] {msg}")
      game_hangman(msg)
     if codenames==True and msg[0]=='!':
       send(f"[{addr}] {msg}")
       game_codenames(conn,msg[1:])
     else:
      send(f"[{addr}] {msg}")
     
 
 send(f"{addr} has left the chat")
 conns.pop(number) 
 print(conns)
 nicknames.pop(number) 
 print(nicknames)
 conn.close()

def start():
 server.listen()
 print(f"[LISTENING] server is listening on {server}")
 while True:
  conn, addr=server.accept()
  thread=threading.Thread(target=handle_client, args=(conn, addr, len(conns)))
  thread.start()
  print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
  


def game_hangman(bitch):
 global hangman
 global hangman_word
 global hangman_tries
 global hangman_characters
 if bitch in hangman_characters:
  send("You already did that one, dumbass")
  hangman_tries-=1
 else:
  for t in range(len(hangman_word)):
   if hangman_word[t-1]==bitch:
    hangman_characters[t-1]=bitch
  send('')
  send('')
  send('')
  send("".join(hangman_characters))
  if bitch not in hangman_word:
   send("Nope, go fuck yourself")
   hangman_tries-=1
  if "".join(hangman_characters)==hangman_word:
   send("Yay, you won !")
   hangman_tries=0
 if hangman_tries==0:
  hangman=False
  send('Game over')
  
def game_codenames(player,bitch):
 global conns
 global nicknames
 global codenames
 global codenames_blue_op
 global codenames_red_op
 global codenames_turn
 global word_list
 global codenames_word_list
 if codenames==False:
  var=random.randint(0,len(conns)-1)
  codenames_blue_op=conns[var]
  send(f" {nicknames[var]} is the \033[94mBlue\033[30m operator")
  while True:
   var2=random.randint(0,len(conns)-1)
   if var2!=var:
    codenames_red_op=conns[var2]
    send(f" {nicknames[var2]} is the \033[91mRed\033[30m operator")
    break
  codenames_word_list.clear()
  for i in range(25):
   while True:
    while True:
     var=random.randint(0,198)
     varvar=0
     for q in range(len(codenames_word_list)):
      if codenames_word_list[q].word==word_list[var]:
       varvar=1
       break
     if varvar==0:
      break
    word=codenames_word(word_list[var])
    codenames_word_list.append(word)
    break
  for i in range(8):
   while True:
    var=random.randint(0,24)
    if codenames_word_list[var].hidden_colour=='\033[30m':
     codenames_word_list[var].hidden_colour='\033[94m'
     break
  for i in range(8):
   while True:
    var=random.randint(0,24)
    if codenames_word_list[var].hidden_colour=='\033[30m':
     codenames_word_list[var].hidden_colour='\033[91m'
     break
  
  message=''
  var=0
  for i in range(25):
   var+=1
   message+=codenames_word_list[i].hidden_colour+codenames_word_list[i].word+'\033[30m, '
   if var==5:
    message+='\n'
    var=0
  message=message.encode(format)
  message_length=len(message)
  send_length=str(message_length).encode(format)
  send_length+=b' '*(header-len(send_length))
  codenames_blue_op.send(send_length)
  codenames_blue_op.send(message)
  message2='You are the \033[94mBlue\033[30m operator'
  message2=message2.encode(format)
  message_length2=len(message2)
  send_length2=str(message_length2).encode(format)
  send_length2+=b' '*(header-len(send_length2))
  codenames_blue_op.send(send_length2)
  codenames_blue_op.send(message2)
  codenames_red_op.send(send_length)
  codenames_red_op.send(message)
  message2='You are the \033[91mRed\033[30m operator'
  message2=message2.encode(format)
  message_length2=len(message2)
  send_length2=str(message_length2).encode(format)
  send_length2+=b' '*(header-len(send_length2))
  codenames_red_op.send(send_length2)
  codenames_red_op.send(message2)
  message=''
  var=0
  for i in range(25):
   var+=1
   message+=codenames_word_list[i].word+', '
   if var==5:
    message+='\n'
    var=0
  send(message)
  send(f"{codenames_turn} is starting")
  codenames=True
 
 else:
  if player==codenames_blue_op or player==codenames_red_op:
   send("Oi, the operators can't guess")
  else:
   for i in range(25):
    if bitch==codenames_word_list[i].word:
     if codenames_word_list[i].hidden_colour=='\033[94m':
      send(f"{codenames_word_list[i].hidden_colour}{codenames_word_list[i].word}\033[30m was \033[94mBLUE\033[30m")
      if codenames_turn=='Red':
       send("It's now \033[94mBlue\033[30m's turn")
       codenames_turn='Blue'
     elif codenames_word_list[i].hidden_colour=='\033[91m':
      send(f"{codenames_word_list[i].hidden_colour}{codenames_word_list[i].word}\033[30m was \033[91mRED\033[30m")
      if codenames_turn=='Blue':
       send("It's now \033[91mRed\033[30m's turn")
       codenames_turn='Red'
     elif codenames_word_list[i].hidden_colour=='\033[30m':
      send(f"{codenames_word_list[i].hidden_colour}{codenames_word_list[i].word}\033[30m was \033[90mGRAY\033[30m")
      codenames_word_list[i].hidden_colour='\033[90m'
      if codenames_turn=='Blue':
       send("It's now \033[91mRed\033[30m's turn")
       codenames_turn='Red'
      else:
       send("It's now \033[94mBlue\033[30m's turn")
       codenames_turn='Blue'
     else:
      send(f"{codenames_word_list[i].hidden_colour}{codenames_word_list[i].word}\033[30m was already guessed")
      break
     codenames_word_list[i].open_colour=codenames_word_list[i].hidden_colour
     codenames_word_list[i].hidden_colour='\033[90m'
     message=''
     var=0
     for i in range(25):
      var+=1
      message+=codenames_word_list[i].hidden_colour+codenames_word_list[i].word+'\033[30m, '
      if var==5:
       message+='\n'
       var=0
     message=message.encode(format)
     message_length=len(message)
     send_length=str(message_length).encode(format)
     send_length+=b' '*(header-len(send_length))
     message2='Operator view:'
     message2=message2.encode(format)
     message_length2=len(message2)
     send_length2=str(message_length2).encode(format)
     send_length2+=b' '*(header-len(send_length2))
     codenames_blue_op.send(send_length2)
     codenames_blue_op.send(message2)
     codenames_blue_op.send(send_length)
     codenames_blue_op.send(message)
     codenames_red_op.send(send_length2)
     codenames_red_op.send(message2)
     codenames_red_op.send(send_length)
     codenames_red_op.send(message)
     message=''
     var=0
     for i in range(25):
      var+=1
      message+=codenames_word_list[i].open_colour+codenames_word_list[i].word+'\033[30m, '
      if var==5:
       message+='\n'
       var=0
     send(message)
     
     var=8
     varvar=8
     for i in range(25):
      if codenames_word_list[i].open_colour=='\033[94m':
       var-=1
      elif codenames_word_list[i].open_colour=='\033[91m':
       varvar-=1
     if var==0:
      send('\033[94mBlue\033[30m wins yay')
      codenames=False
     elif varvar==0:
      send('\033[91mRed\033[30m wins yay')
      codenames=False
     break
  


conns=[]
nicknames=[]
print("Server is starting up")
start()