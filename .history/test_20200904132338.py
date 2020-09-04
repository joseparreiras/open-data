import matplotlib.patches as patches
from match import *

match_id = 15946
my_match = load_match(match_id)

my_team = my_match.team_match('Barcelona')

my_team.position_map()

my_player = my_team.player_match(my_match.players[15])

my_player.window(start=0, end=30).heatmap()
plt.show()
