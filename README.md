# Mementos
Python/Socket based texting app/intranet if I feel like adding more features. It includes the server and client sides

To boot it up, run the server code on a computer, and choose a port (ports like in wifi, usually 5050 is available, if not choose 5051 or some other number until it works). Then you can run the server side on seperate or the same computer and connect by entering the IP and port. DO watch out for firewalls

I put a few commands in it, useable by starting messages with ! Included are !nickname, to set your nickname, !hangman to play hangman, !codenames to play codenames (I'm not sure if I actually coded that one in tho), and !uwu to uwu-ify your message (priorities). Obviously you can add your own commands by going in the server code and finding the if msg[:10]=='!nicknames ': line and copying it to suit what you want
