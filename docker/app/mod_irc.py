# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mod_irc.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: titouanck <chevrier.titouan@gmail.com>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/06 16:41:32 by titouanck         #+#    #+#              #
#    Updated: 2024/01/23 14:37:06 by titouanck        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket, time, os, select
from mod_files      import write_chat
from mod_requests   import get_username

USER_TOKEN      = os.environ["USER_TOKEN"]
TWITCH_USERNAME = get_username()

# **************************************************************************** #

class IrcServer:

    def __init__(self, channel):
        self.socket = None
        self.channel = channel
    
    def get_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect(("irc.chat.twitch.tv", 6667))

        self.send_data(f"PASS oauth:{USER_TOKEN}")
        self.send_data(f"NICK {TWITCH_USERNAME}")
        self.send_data(f"JOIN #{self.channel}")
    
    def parse(self, irc_message):
        messages     = ["PING", "PRIVMSG"]
        index        = None
        message_type = None
        
        for some_message in messages:
            if some_message in irc_message:
                length = len(irc_message.split(some_message)[0])
                if index is None or length < index:
                    message_type = some_message
                    index = length
        if message_type == "PING":
            content = irc_message.split("PING :")[1]
        elif message_type == "PRIVMSG":
            username = irc_message[1:].split("!")[0]
            content = f"{username}: " + irc_message.split(f"PRIVMSG #{self.channel} :")[1]
        else:
            content = irc_message
        return message_type, content

    def send_data(self, data):
        self.socket.send((data + '\n').encode("UTF-8"))

    def send_privmsg(self, message):
        self.send_data(f"PRIVMSG #{self.channel} :{message}")
        write_chat(f">> {TWITCH_USERNAME}: {message}")

    def send_pong(self, message):
        self.send_data(f"PONG :{message}")
        write_chat(f">> /PONG {message}")

    def listener(self):
        while True:
            try:
                response = self.socket.recv(1024).decode("utf-8")
                if len(response) == 0:
                    write_chat(f"<!> DEBUG/ERROR <!> :len(response)=0&response={response}")
                    self.get_socket()
                    self.connect()
                while "\n" in response:
                    splited_response = response.split("\n", 1)
                    response = splited_response[1]
                    message_type, content = self.parse(splited_response[0])
                    if message_type == "PRIVMSG":
                        write_chat(f"<< {content}")
                    else:
                        if message_type != None:
                            write_chat(f"<< /{message_type} {content}")
                        else:
                            write_chat(f"<< {content}")
                        if message_type == "PING":
                            self.send_pong(content)
            except OSError as e:
                self.get_socket()
                self.connect()
                write_chat("ERROR: program just went into: except OSError as e")

# **************************************************************************** #
