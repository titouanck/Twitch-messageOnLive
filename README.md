### What does it do ? How does it work ?
The program will use the .json files provided, and launch X docker containers, each based on a file.  
In each container, a python program performs the following pseudo-code:  
```python
when CHANNEL_TO_MONITOR goes live:
    for MESSAGE in MESSAGES_TO_SEND:
        send MESSAGE on the chat of CHANNEL_TO_SEND_MESSAGE
        sleep(COOLDOWN_BETWEEN_MESSAGES)
    CLIP_OF_FIRST_SECONDS_OF_LIVE = create_clip()
    download(CLIP_OF_FIRST_SECONDS_OF_LIVE, inside "logs/{CHANNEL_TO_MONITOR}/clips")
```

---
### Clone the project
```bash
git clone https://github.com/titouanck/Twitch-messageOnLive.git
cd Twitch-messageOnLive
```

---
### Set-up the project
Inside the `configurations/` directory, you will find multiple files ending with the extension **.JSON**.  

  
To get started, you can take a look at any of the **.JSON** file present in the directory.  
For example, with `kyzen_.json` I want to send two defined messages on **kyzen_**'s chat when he goes live on Twitch:

|           |           |
|-----------|-----------|
| <img width="276" alt="Screenshot 2024-01-10 at 18 55 19" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/12aa421c-2e02-44df-b115-ec335e698089"> | <img width="548" alt="Screenshot 2024-01-10 at 19 26 43" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/a4daee1a-b7c4-469f-b92f-3b45ce83da05">

---
### Launch the project
```bash
make
```

<img width="667" alt="Screenshot 2024-01-10 at 19 48 58" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/b205b45f-4129-4d0f-a6e7-9daa18482bc8">
  

After typing `make`, follow the link to obtain an oauth user token, which will only be stored locally in an .env file.  

|           |           |
|-----------|-----------|
|  <img width="563" alt="Screenshot 2024-01-10 at 20 01 47" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/fcf7d8e0-d640-470f-81f7-5b1b377fbe66"> |  <img width="359" alt="Screenshot 2024-01-10 at 19 56 37" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/7794b3c2-fb86-441b-b19d-c821ea25ba4e">

Copy and paste the authentication token into the terminal, and press enter.  
  
<img width="670" alt="Screenshot 2024-01-10 at 20 11 31" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/e8b4f485-fbbc-4f0a-82c7-fc1916569c6e">

If your token no longer works, you can simply delete the **./docker/.env** file and type `make` again.

---
### We did it!
You should now see something like that.  
You don't ? It is possible that your docker installation requires you to be root to manipulate containers.  
If so, use `make sudo` instead of `make`
```python
Creating docker/.env file...
alpine3.19: Pulling from library/python
Status: Image is up to date for python:alpine3.19

. . .

WARNING: The JSON_FILE_TRUNC variable is not set. Defaulting to a blank string.
WARNING: The JSON_FILE variable is not set. Defaulting to a blank string.

. . .

[✔️] docker-compose built successfully
Starting mol_kyzen_ ... done
Launching docker-compose up with kyzen_.json
Starting mol_podasai ... done
Launching docker-compose up with podasai.json
Starting mol_snayzy ... done
Launching docker-compose up with snayzy.json
```

---
### Constant logs
Logs including **live status** and all **chat messages** are saved in the `/logs` directory for as long as the program is running.  
|           |           |
|-----------|-----------|
|<img width="829" alt="Screenshot 2024-01-10 at 20 50 34" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/9e870cf5-b41d-4418-a769-1ca506f15c02"> | <img width="827" alt="Screenshot 2024-01-10 at 20 41 03" src="https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/79c6b081-3ab3-42d1-9bc7-7e13d5637691"> |

---
### &nbsp;![vip](https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/b0a8e39f-f7d4-4b5d-a21d-110feaf4340e)&nbsp; A little background on this mini-project &nbsp;![vip](https://github.com/titouanck/Twitch-messageOnLive/assets/87268044/b0a8e39f-f7d4-4b5d-a21d-110feaf4340e)&nbsp;
When **kyzen_** launches his live stream, the first person to say **« bonjour »** is offered **VIP status** on his channel.  
After several failed attempts to be the first to click on the stream start notification and say **« bonjour »**, I thought it might be fun, and even a bit useful, to find a way of always being the first to say hi.
