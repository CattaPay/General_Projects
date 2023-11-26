
from sapai.pets import Pet
from sapai.teams import Team
from sapai.shop import Shop
from sapai.player import Player
from sapai.agents import CombinatorialSearch

# fiddling with shops
# shop = Shop()
# shop.freeze(0)
# print(shop)
# shop.roll()
# print(shop)

# fiddling with players

me = Player(gold = 5)
#print(me)
search = CombinatorialSearch(verbose = True, max_actions = 100)

search.search(me)

