import os #os module imported here
import json 
import sys
from twitch import TwitchClient # Python Twitch API wrapper
from pprint import pprint # data structure formatting

directory = os.getcwd() # get present working directory location here
cnt = 0 # keep a count of json files found
jsonfiles = [] # list to store all json files found at location
emotedict = {}

# Twitch auth
client = TwitchClient(client_id='<uyd30soyglmbs9eabkuapa6dzsdywk>')
emoteset = [0] # Emotesets by int to retrieve
emotes = client.chat.get_emoticons_by_set(emoteset) # Contains dict of emotes

# Parse emote names through returned dict and add to mapping
for x in emotes['emoticon_sets']['0']:
    emotedict[x['code']] = 0

# Identify files in directory
for file in os.listdir(directory):
    try:
        if file.endswith(".json"):
            jsonfiles.append(str(file))
            cnt = cnt + 1

            with open(file) as f:
                data = json.load(f)

            # Access chat message in json and create mapping
            # of freq of emotes
            for entry in data:
                if 'message' not in entry:
                    continue
                else:
                    msgarr = entry['message']['body'].split(" ")
                    for word in msgarr:
                        if word in emotedict:
                            emotedict[word] = emotedict[word] + 1

    except Exception as e:
        raise e
        print ("No files in directory!")

print (emotedict)

# log files found of each type
for jsonfile in jsonfiles:
    print (jsonfile)

print ("Total files found:", cnt)