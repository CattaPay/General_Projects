
import helpers
import requests

name = "el problema"


dat = helpers.GetSummonerDat(name, helpers.KEY)

print(dat)

start = 0
count = 100
matchids = helpers.GetMatchIds(name, start, count, helpers.KEY)
matchid = matchids[0]
query = helpers.AMERICALL + "/lol/match/v5/matches/"+ matchid + "?api_key=" + helpers.KEY
#print(query)
response = requests.get(query)
dat = response.json() # dat contains metadata and info. Metadata is participants and matchId, info is all info about the game

info = dat["info"] # dictionary containing deets on game

#print(matchids)


# print(info["gameCreation"]) # timestamp of game creation on server
# print(info["gameDuration"]) # time in seconds of game (used to be milliseconds)
# print(info["gameEndTimestamp"]) # timestamp of game end
# print(info["gameId"]) # game id
# print(info["gameMode"]) # type of game
# print(info["gameName"]) # name of the game
# print(info["gameStartTimestamp"]) # timestamp of game start on server
# print(info["gameType"]) # matchmade or custom?
# print(info["gameVersion"]) # version of the game
# print(info["mapId"]) # id of the map
# print(info["participants"]) # stats for everyone in the game (list len 10)
    # print(len(info["participants"][0]) # dictionary of stats for participant
# print(info["platformId"]) # server of the game?
# print(info["queueId"]) # id of queue
# print(info["teams"]) # list of 2 teams
    # print(info["teams"][0]) # dictionary of bans, objectives, teamid, and winner
# print(info["tournamentCode"]) # tournament code

print()
print()
for i in range(5):
    bruh = info["participants"][i]
    print(bruh["individualPosition"], bruh["teamPosition"])
print()
print()
for i in range(5, 10):
    bruh = info["participants"][i]
    print(bruh["individualPosition"], bruh["teamPosition"])

#print(bruh.keys())