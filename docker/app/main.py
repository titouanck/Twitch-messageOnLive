# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tchevrie <tchevrie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/06 13:26:34 by titouanck         #+#    #+#              #
#    Updated: 2024/01/10 08:47:21 by tchevrie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time, os, random, threading
from mod_files      import open_logs, open_chat, write_logs, write_chat
from mod_requests   import is_live_broadcast, get_username
from mod_irc        import IrcServer
from mod_data       import get_data

# **************************************************************************** #

def main():
    try:
        get_data()
    except Exception as e:
        print(e)
    print(get_data.channel_to_monitor)
    open_logs(f"{get_data.channel_to_monitor}->{get_data.channel_to_send_message}")
    open_chat(f"{get_data.channel_to_monitor}->{get_data.channel_to_send_message}")
    main.irc_server = IrcServer(get_data.channel_to_send_message)
    main.irc_server.get_socket()
    main.irc_server.connect()
    chat_thread = threading.Thread(target=main.irc_server.listener)
    chat_thread.start()
    routine()
    chat_thread.join()

# **************************************************************************** #

def routine():
    while True:
        if is_live_broadcast(get_data.channel_to_monitor):
            is_online()
        else:
            is_offline()

def is_online():
    title        = is_live_broadcast.data['data'][0]['title']
    game_name    = is_live_broadcast.data['data'][0]['game_name']
    viewer_count = is_live_broadcast.data['data'][0]['viewer_count']
    write_logs(get_data.channel_to_monitor + " is currently live streaming.")
    write_logs(f"{get_data.channel_to_monitor} {{game_name:'{game_name}', viewer_count:'{viewer_count}', title:'{title}'}}")
    time.sleep(60)

def is_offline():
    time_to_sleep = 60
    index = 0
    while not is_live_broadcast(get_data.channel_to_monitor):
        if index % 10 == 0:
            write_logs(f"{get_data.channel_to_monitor} is currently offline.")
        time.sleep(0.2)
        index += 1
    write_logs(get_data.channel_to_monitor + " just went LIVE!")
    for message in get_data.messages_to_send:
        main.irc_server.send_privmsg(message)
        time.sleep(get_data.cooldown_between_messages)
        time_to_sleep -= get_data.cooldown_between_messages;
    if time_to_sleep > 0:
        time.sleep(time_to_sleep)

# **************************************************************************** #

if __name__ == "__main__":
    main()

# **************************************************************************** #