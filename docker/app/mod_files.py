# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mod_files.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: titouanck <chevrier.titouan@gmail.com>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/06 12:45:06 by titouanck         #+#    #+#              #
#    Updated: 2024/01/23 14:26:07 by titouanck        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from mod_time       import get_date, get_time
from mod_requests   import get_username
from mod_data       import get_data

JSON_FILENAME 	   = os.environ["JSON_FILE"].rstrip(".json")
PATH_DIRECTORY     = "./logs"
LOGS_SUBDIRECTORY  = ""
CHAT_SUBDIRECTORY  = "chat"

# **************************************************************************** #

def open_file(filename):
    if os.path.isfile(filename):
        file_obj = open(filename, 'a')
        file_obj.write("# **************************************** #\n")
        file_obj.write(f"[{get_time()}] \"{filename}\" already exists\n")
        file_obj.flush()
    else:
        file_obj = open(filename, 'w')
        os.chmod(filename, 0o766)
        file_obj.write(f"[{get_time()}] \"{filename}\" has been created\n")
        file_obj.flush()
    return file_obj

# **************************************************************************** #

def open_logs(filename):
    parent_directory = PATH_DIRECTORY + '/' + filename + '/' + LOGS_SUBDIRECTORY
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
    os.chmod(PATH_DIRECTORY + '/' + filename, 0o777)
    os.chmod(parent_directory, 0o777)

    open_logs.date     = get_date()
    open_logs.filename = parent_directory + '/' + open_logs.date + ".log"
    open_logs.file_obj = open_file(open_logs.filename)
    return open_logs.file_obj

def open_chat(filename):
    parent_directory = PATH_DIRECTORY + '/' + filename + '/' + CHAT_SUBDIRECTORY
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
    os.chmod(PATH_DIRECTORY + '/' + filename, 0o777)
    os.chmod(parent_directory, 0o777)

    open_chat.date     = get_date()
    open_chat.filename = parent_directory + '/' + open_chat.date + ".log"
    open_chat.file_obj = open_file(open_chat.filename)
    return open_chat.file_obj

# **************************************************************************** #

def write_logs(str):
    if open_logs.date != get_date():
        open_logs.file_obj.close()
        open_logs(JSON_FILENAME)
    str = f"[{get_time()}] {str}"
    open_logs.file_obj.write(str + "\n")
    open_logs.file_obj.flush()
    print(str)

def write_chat(str):
    if open_chat.date != get_date():
        open_chat.file_obj.close()
        open_chat(JSON_FILENAME)
    str = f"[{get_time()}] {str}"
    open_chat.file_obj.write(str + "\n")
    open_chat.file_obj.flush()
    print(str)

# **************************************************************************** #
