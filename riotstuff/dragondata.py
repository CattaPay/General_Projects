import requests
import helpers

champs = requests.get("http://ddragon.leagueoflegends.com/cdn/12.14.1/data/en_US/champion.json").json()

cdat = champs["data"]
champdict = {}
for i in cdat:
    champdict[cdat[i]["key"]] = i

helpers.MapToFile(champdict, "champdict.csv")

summonerspells = requests.get("http://ddragon.leagueoflegends.com/cdn/12.14.1/data/en_US/summoner.json").json()

dats = summonerspells["data"]
sumdict = {}
for i in dats:
    sumdict[dats[i]["key"]] = dats[i]["name"]

helpers.MapToFile(sumdict, "spellsdict.csv")