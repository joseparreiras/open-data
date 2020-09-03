import matplotlib.patches as patches
from match import *

my_match = load_match('data/events/15946.json')

my_match.summary()

my_team = my_match.team_match('Barcelona')

goals_id = []
for x in my_team.data.iterrows():
    linha = x[1]
    if not pd.isnull(linha.shot):
        if 'outcome' in linha.shot.keys():
            if linha.shot['outcome']['name'] == 'Goal':
                goals_id += [linha.id]

my_team.play(goals_id[2])
plt.plot()
plt.savefig('jogada.png', dpi=300)
# Foul summary

pd.unique([x['name'] for x in play_data.team])

pass_id = [x['name'] == 'Pass' for x in play_data.type]
pass_data = play_data.iloc[np.where(pass_id)]
for x in pass_data.iloc:
    print(x['end_location'], x['recipient']['name'])

my_player = my_match.player_match(my_match.players[15])

time = max(my_player.data.minute + my_player.data.second/60)
goals = sum([x['outcome']['name'] ==
             'Goal' for x in my_player.data.shot.dropna()])

# Dribble

carries = [x[1] for x in my_player.data.iterrows() if x[1]['type']
           ['name'] == 'Carry']
dribbles = [x[1]['dribble']
            for x in my_player.data.iterrows() if x[1]['type']['name'] == 'Dribble']
dribbles_comp = [x for x in dribbles if x['outcome']['name'] == 'Complete']

dribble_summary = {
    'carries': len(carries),
    'dribbles': len(dribbles),
    'dribbles_complete': len(dribbles_comp),
    'dribbles_incomplete': len(dribbles) - len(dribbles_comp)
}

# Defense

ball_rec_idx = np.where(
    [x['name'] == 'Ball Recovery' for x in my_player.data['type']])
ball_rec = my_player.data.iloc[ball_rec_idx]
ball_rec_failure = [
    x for x in ball_rec['ball_recovery'].dropna() if 'recovery_failure' in x.keys()]
ball_rec_offensive = [
    x for x in ball_rec['ball_recovery'].dropna() if 'offensive' in x.keys()]

interception_idx = np.where(
    [x['name'] == 'Interception' for x in my_player.data['type']])
interception = my_player.data.iloc[interception_idx].interception
interception_won = [x for x in interception if x['outcome']['name'] == 'Won']

duel_idx = np.where([x['name'] == 'Duel' for x in my_player.data['type']])
duel = my_player.data.iloc[duel_idx].duel
aerial_duel = [x for x in duel if x['type']['name'] == 'Aerial Lost']

# Shots map


def shot_arrow(loc0, loc1):
    import matplotlib.patches as patches
    style = patches.ArrowStyle('-|>', head_length=2, head_width=2)
    connection = patches.ConnectionStyle("Arc3", rad=0)
    arrow = patches.FancyArrowPatch(tuple(loc0), tuple(
        loc1), arrowstyle=style, connectionstyle=connection, linestyle='-', color='red', linewidth=2, edgecolor='black')
    return arrow


shots = [x[1]
         for x in my_player.data.iterrows() if not pd.isnull(x[1]['shot'])]
