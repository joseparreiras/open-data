import matplotlib.patches as patches
from match import *

my_match = load_match('data/events/15946.json')

# my_match.summary()

# my_player = my_match.player_match(my_match.players[15])
# my_player.summary()
# my_match.touch_map('Shot')
# plt.show()

# Foul summary

play_id = my_match.data.iloc[2000].id
play_ref = my_match.data.iloc[np.where(
    [x == play_id for x in my_match.data.id])].iloc[0]
team_ref = play_ref.team['name']
play_idx = np.where(
    [x == play_ref.possession for x in my_match.data.possession])
play_data = my_match.data.iloc[possession_idx]
type_list = pd.unique([x['name'] for x in play_data.type])
field = plt.imread('img/field2.png')
fig, ax = plt.subplots()
#ax.imshow(field, zorder=0, extent=[0, 120, 0, 80])
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_visible(False)
for x in play_data.iterrows():
    play = x[1]
    play_loc = play.location
    play_type = play.type['name']
    if not play_type == 'Pressure':
        if play_type == 'Ball Recovery':
            plt.scatter(play_loc[0], play_loc[1], s=10, c='yellow')
    elif play_type == 'Ball Receipt*':
        plt.scatter(play_loc[0], play_loc[1], s=10, c='blue')
    elif play_type == 'Carry':
        carry_loc = play.carry['end_location']
        plt.scatter(carry_loc[0], carry_loc[1], s=10, c='purple')
        carry_dloc = [carry_loc[0]-play_loc[0], carry_loc[1]-play_loc[1]]
    elif play_type == 'Pass':
        pass_end = play['pass']['end_location']
        if 'outcome' in play.keys():
            outcome = play['outcome']['name']
        arrow = patches.FancyArrowPatch(
            tuple(play_loc), tuple(pass_end), arrowstyle='-|>')
        plt.gca().add_patch(arrow)
        #plt.arrow(play_loc[0], play_loc[1], pass_dloc[0], pass_dloc[1],length_includes_head = True, head_width = 1)

plt.xlim(0, 120)
plt.ylim(0, 80)
plt.show()
