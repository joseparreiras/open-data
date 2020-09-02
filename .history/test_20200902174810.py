import matplotlib.patches as patches
from match import *

my_match = load_match('data/events/15946.json')

# my_match.summary()

# my_player = my_match.player_match(my_match.players[15])
# my_player.summary()
# my_match.touch_map('Shot')
# plt.show()

# Foul summary


pass_id = [x['name'] == 'Pass' for x in play_data.type]
pass_data = play_data.iloc[np.where(pass_id)]
for x in pass_data.iloc:
    print(x['end_location'], x['recipient']['name'])
