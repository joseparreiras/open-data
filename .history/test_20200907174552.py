import matplotlib.patches as patches
from match import *
from player_match import *

match_id = 15946
my_match = load_match(match_id)

my_team = my_match.team_match('Barcelona')

my_team.position_map()

my_player = my_team.player_match(my_match.players[15])

my_player.window(start=0, end=30).heatmap()
plt.show()

data = my_match.data

team_name = 'Barcelona'

team_name = my_match.teams[1]

team_idx = np.where(
    [x['name'] == team_name for x in data.team])[0]

data.iloc[team_idx].dropna()

data.iloc[team_idx].block.dropna()

block_deflection = [x for x in data.block.dropna() if 'deflection' in x.keys()]
block_offensive = [x for x in data.block.dropna() if 'offensive' in x.keys()]
block_save = [x for x in data.block.dropna() if 'save_block' in x.keys()]
block_counterpass = [
    x for x in data.block.dropna() if 'counterpass' in x.keys()]

blocks = block_deflection+block_offensive+block_save+block_counterpass

print(team_name)
print(len(blocks))
print(len(block_deflection))
print(len(block_offensive))
print(len(block_save))
print(len(block_counterpass))

# Tactics and Active Tactics
self = my_match

active_tactic = None
