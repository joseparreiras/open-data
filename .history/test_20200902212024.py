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
ball_rec = [x for x in my_player.data if x['type']['name'] == 'Ball Recovery']
