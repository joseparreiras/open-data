import numpy as np
import pandas as pd
import os

os.getcwd()

event_list = []
for r, d, f in os.walk('data/events/'):
    for file in f:
        event_list += [r+file]

player_list = pd.DataFrame({'id': [], 'name': []})
team_list = pd.DataFrame({'id': [], 'name': []})

for j in range(1):
    event = pd.read_json(event_list[j])
    player = {'id': [], 'name': []}
    team = {'id': [], 'name': []}
    match_id = []

    for row in event.iterrows():
        idx, data = row
        team['id'] += [data.team['id']]
        team['name'] += [data.team['name']]
        if not data.isnull().player:
            player['id'] += [data.player['id']]
            player['name'] += [data.player['name']]

    player = pd.DataFrame(player).drop_duplicates()
    team = pd.DataFrame(team).drop_duplicates()

    player_list = player_list.append(player).drop_duplicates()
    team_list = team_list.append(team).drop_duplicates()
    print(str(int(10000*j/len(event_list))/100)+'%')

player_list.to_csv('player_list.csv')
team_list.to_csv('team_list.csv')
