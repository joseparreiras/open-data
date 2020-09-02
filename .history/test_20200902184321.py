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
