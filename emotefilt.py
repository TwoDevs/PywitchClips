import os #os module imported here
import json 
import sys
from twitch import TwitchClient # Python Twitch API wrapper
from pprint import pprint # data structure formatting

directory = os.getcwd() # get present working directory location here
cnt = 0 # keep a count of json files found
jsonfiles = [] # list to store all json files found at location
emotedict = {} # dict of dicts of emotes per json

# Twitch auth info
client = TwitchClient(client_id='<uyd30soyglmbs9eabkuapa6dzsdywk>')
emoteset = [0] # Emotesets to retrieve; input is int list
emotes = client.chat.get_emoticons_by_set(emoteset) # Contains dict of emotes

# Identify files in directory
for file in os.listdir(directory):
    try:
        # JSON file assumed to be output from rechat-dl.py
        if file.endswith(".json"):
            jsonfiles.append(str(file))

            # Initialize dict mapping for json
            tmpdict = {}
            for x in emotes['emoticon_sets']['0']:
                tmpdict[x['code']] = 0

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
                        if word in tmpdict:
                            tmpdict[word] = tmpdict[word] + 1

            # Add dict to json dict
            emotedict[cnt] = tmpdict
            cnt = cnt + 1

    except Exception as e:
        raise e
        print ("No files in directory!")

# print out dictionary
pprint (emotedict)

# log files found of each type
for jsonfile in jsonfiles:
    print (jsonfile)

print ("Total files found:", cnt)