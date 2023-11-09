import re

with open('../data/input/test_log.txt', 'r') as f:
    log = f.read()

# |poke|p1|Landorus-Therian, L50, M|
# |poke|p1|Iron Hands, L50|
# |poke|p1|Ogerpon-Hearthflame, L50, F|
# |poke|p1|Chien-Pao, L50|
# |poke|p1|Gholdengo, L50|
# |poke|p1|Urshifu-*, L50, M|
# |poke|p2|Rotom-Heat, L50|
# |poke|p2|Arcanine-Hisui, L50, M|
# |poke|p2|Flutter Mane, L50|
# |poke|p2|Tornadus, L50, M|
# |poke|p2|Landorus-Therian, L50, M|
# |poke|p2|Urshifu-*, L50, F|

matches_team = re.findall(r'\|poke\|p[1-2]\|(.+?)[-|,]', log)

team1 = matches_team[:6]
team2 = matches_team[6:]


# |player|p1|BungerWarrior|266|1327
# |player|p2|diegodm2694|2|1391

matches_player = re.findall(r'\|player\|p[1-2]\|(.+?)\|', log)

player1 = matches_player[0]
player2 = matches_player[1]

# |win|diegodm2694
match_winner = re.findall(r'\|win\|(.+?)\n', log)[0]

