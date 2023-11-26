
import requests


NACALL = "https://na1.api.riotgames.com"
AMERICALL = "https://americas.api.riotgames.com"
KEY = "RGAPI-1d6f9e1c-b313-4a88-a85a-816d676f1d60"

def GetSummonerDat(name, key): # returns 
    query = NACALL + "/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + key
    response = requests.get(query)
    return(response.json())

def GetMasteries(name, key): # returns list of dicts, one for each champ
    dat = GetSummonerDat(name, key)
    sumid = dat["id"]
    query = NACALL + "/lol/champion-mastery/v4/champion-masteries/by-summoner/" + sumid + "?api_key=" + key
    response = requests.get(query)
    return(response.json())

def GetMatchIds(name, start, count, key):
    dat = GetSummonerDat(name, key)
    puuid = dat["puuid"]
    query = AMERICALL + "/lol/match/v5/matches/by-puuid/"+ puuid + "/ids?start=" + str(start) + "&count=" + str(count) + "&api_key=" + key
    response = requests.get(query)
    return(response.json())

def MapToFile(boi, filename):
    outstr = ""
    for i in boi:
        outstr += i + "," + boi[i] + "\n"
    f = open(filename, "w")
    f.write(outstr)
    f.close

def FileToMap(filename):
    outmap = {}
    f = open(filename)
    for line in f:
        bois = line.strip().split()
        outmap[bois[0]] = bois[1]
    return(outmap)






# LEAGUE = "/lol/league/v4/entries/by-summoner/" # Get league entries in all queues for a given summoner ID.
# CURRENT = "/lol/spectator/v4/active-games/by-summoner/"

# query = BASECALL + LEAGUE + sumid + "?api_key=" + KEY
# response = requests.get(query)
# leaguedat = response.json()

# print(type(leaguedat))
# print(len(leaguedat))


# response = requests.get(query)
# leaguedat = response.json()

# print(type(leaguedat))
# print(leaguedat["status"])

# query = BASECALL + "/lol/spectator/v4/featured-games"