# -*- coding: cp1252 -*-
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import sqlite3
import re
conn = sqlite3.connect('relationships.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS userInfo")
sql = 'create table if not exists userInfo (id integer primary key AUTOINCREMENT not null, name text, email text, logo text); '
c.execute(sql)
conn.commit()
print 'table created'
sql = 'create table if not exists userValues (id integer primary key AUTOINCREMENT not null, closeness integer default 0, userID int); '
c.execute(sql)
conn.commit()
conn.close()
print 'table created'

#sets variables for connection to twitch chat
bot_owner = 'gnoejuan'
nick = 'humbleroboservant' 
##channel = '#gnoejuan' #Stream Channel (Twitch.Tv Stream)
channel = '#warpspiderx'
##channel = '#acpixel'
server = 'irc.twitch.tv'
password = 'oauth:ije9qznlhl7l8b28zg6lbc2awoyaya' #Password (oAuth
port = 6667
readbuffer = ""
MODT = False 

queue = 13 #possibly implement a wait timer?

irc = socket.socket()
irc.connect((server, port)) #connects to the server

#sends variables for connection to twitch chat
irc.send('PASS ' + password + '\r\n')
irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
irc.send('NICK ' + nick + '\r\n')
irc.send('JOIN ' + channel + '\r\n')
def Send_message(message): 
    irc.send("PRIVMSG " +channel + " :" + message + "\r\n")
##Dictionaries
greetings = ['Hey','Hai','Greetings', 'Hello','Hallo','hola']
ignore = ['heyguys','they', 'hail','They']
Send_message('Bot Connected')
while True:
    readbuffer = readbuffer + irc.recv(1024) 
    temp = str.split(readbuffer, "\n") 
    readbuffer = temp.pop() #gets output from IRC server
    for line in temp: 
        # Check if ping 
        if (line[0] == "PING"): 
            irc.send("PONG %s\r\n" % line[1])
        else: 
            # Splits the given string so we can work with it better 
            parts = str.split(line, ":") 
 
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]: 
                try: 
                    # Sets the message variable to the actual message sent 
                    message = parts[2][:len(parts[2]) - 1] 
                except: 
                    message = "" 
                # Sets the username variable to the actual username 
                usernamesplit = str.split(parts[1], "!") 
                username = usernamesplit[0] 
 
                # Only works after twitch is done announcing stuff (MODT = Message of the day) 
                if MODT: 
                    ##print username + ": " + message 
                        ##Check if master
                    if username.find(bot_owner) != -1:
                        ##print 'is master'
                        if message.lower().find('*cuddle*'.lower()) != -1:
                            Send_message('Master, plz')
                        ##For loops to iterate through the Dictionary
                        for item in greetings:
                            i = greetings.index(item)
                            if message.lower().find(greetings[i].lower()) != -1:
                                Send_message('Greetings, Master')
                    ##if message == "Hey": 
                        ##Send_message("Welcome to my stream, " + username)
                    ##Check if me
                    ##elif username.find(nick) != -1:
                        ##print 'is me'
                    ##Check if pleb
                    elif username.find(bot_owner) == -1:
                        ##print 'is viewer'
                        if message.lower().find('*cuddle*'.lower()) != -1:
                            Send_message('Gooby, plz')
                        match = re.search(r'([^\s]+)', message)
                        if match.group() == 'Hey' or 'Hai'or'Greetings' or 'Hello'or 'Hallo'or'hola':
                        ##For loops to iterate through the Dictionary
                        ##for item in greetings:
                            ##i = greetings.index(item)
                            ##if message.lower().find(greetings[i].lower()) != -1 and message.lower() not in ignore and username.find('XanBot') == -1 and username.find('NightBot') == -1 and message.find('?') == -1 and username.find('MooBot') == -1:
                            Send_message('Greetings, ' + username + '. Welcome to the channel!')
                            print "sent greeting" 
                for l in parts: 
                    if "End of /NAMES list" in l: 
                        MODT = True 
    


