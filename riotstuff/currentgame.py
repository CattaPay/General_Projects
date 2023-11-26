import helpers
import requests


champs = requests.get("http://ddragon.leagueoflegends.com/cdn/12.14.1/data/en_US/champion.json").json()

cdat = champs["data"]


champdict = {}
for i in cdat:
    champdict[cdat[i]["key"]] = i

summonerspells = requests.get("http://ddragon.leagueoflegends.com/cdn/12.14.1/data/en_US/summoner.json").json()



name = "el problema"
dat = helpers.GetSummonerDat(name, helpers.KEY)

sumid = dat["id"]

query = helpers.NACALL + "/lol/spectator/v4/active-games/by-summoner/" + sumid + "?api_key=" + helpers.KEY
response = requests.get(query)

dat = response.json()

print(dat["gameId"])

for i in range(10):
    bruh = dat["participants"][i]
    print(bruh["summonerName"], champdict[str(bruh["championId"])])
