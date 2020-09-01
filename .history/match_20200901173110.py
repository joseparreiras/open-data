import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def load_match(file):
    match_data = pd.read_json(file)
    return(match(match_data))


class match(object):
    def __init__(self, data):
        import pandas as pd
        import numpy as np

        def list_player(data):
            return [x['name'] for x in data.player.dropna()]

        self.data = pd.DataFrame(data)
        game_start = np.where(
            [x['name'] == 'Starting XI' for x in self.data.type])[0]
        self.teams = pd.unique([x['name'] for x in self.data.team])
        time_data = self.data[['minute', 'second']]
        time_tup = [(t[1].minute, t[1].second) for t in time_data.iterrows()]
        self.horizon = [min(time_tup), max(time_tup)]
        self.players = pd.unique([x['name']
                                  for x in self.data.player.dropna()])
        if(self.horizon[0] == (0, 0)):
            self.formation = {}
            self.lineup = pd.DataFrame(
                {'team': [], 'player': [], 'position': [], 'jersey_number': []})
            for i in self.data.iloc[game_start].iterrows():
                team_data = pd.Series(i[1]).copy()
                team_name = team_data.team['name']
                formation = team_data.tactics['formation']

                for x in team_data.tactics['lineup']:
                    x['player'] = x['player']['name']
                    x['position'] = x['position']['name']

                lineup = pd.DataFrame(team_data.tactics['lineup'])
                lineup['team'] = team_name

                self.formation.update({team_name: formation})
                self.lineup = pd.concat([self.lineup, lineup])

    def window(self, start, end=(100, 0)):
        if type(start) == int:
            start = (start, 0)
        if type(end) == int:
            end = (end, 0)
        time_data = self.data[['minute', 'second']]
        time_tup = [(t[1].minute, t[1].second) for t in time_data.iterrows()]
        time_idx = np.where([x >= start and x <= end for x in time_tup])[0]
        return match(self.data.iloc[time_idx])

    def team_match(self, team_name):
        team_idx = np.where(
            [x['name'] == team_name for x in self.data.team])[0]
        return match(self.data.iloc[team_idx])

    def player_match(self, player_name):
        not_null_player = self.data.iloc[[
            not x for x in pd.isnull(self.data.player)]]
        player_idx = np.where(
            [x['name'] == player_name for x in not_null_player.player])[0]
        return player_match(not_null_player.iloc[player_idx])
    
    def position_map(self, team):
        teams = self.teams
        if team == teams[0]:
            idx_set = range(11)
        else:
            idx_set = range(11,22)
        average_position = {}
        for player in self.lineup.player.iloc[idx_set]:
            pm = self.player_match(player)
            avg_pos = pm.average_position()
            average_position.update({player: avg_pos})

        average_position = pd.DataFrame(average_position).T

        field = plt.imread('img/field2.png')
        fig, ax = plt.subplots()
        ax.imshow(field, zorder=0, extent=[0, 120, 0, 80])
        plt.scatter(average_position[0].iloc[idx_set],
                    average_position[1].iloc[idx_set], c='blue', s=300, edgecolor='red')
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        lineup = self.lineup[idx_set]
        for x in average_position.iterrows():
            name = x[0]
            lat, lon = x[1]
            idx = np.where(lineup.player == name)[0]
            jersey = str(int(lineup.jersey_number.iloc[idx]))
            plt.text(lat, lon, jersey, horizontalalignment='center',
                    verticalalignment='center', c='white')
        plt.plot()

class player_match(match):
    def __init__(self, data):
        match.__init__(self, data)

    def position(self):
        position_data = self.data[['location', 'minute', 'second']].dropna()
        # position_data['duration'] = (position_data.minute*60+position_data.second).diff().replace(np.nan,0)
        position_data['duration'] = 1
        position_data['lat'] = [x[0] for x in position_data.location]
        position_data['lon'] = [x[1] for x in position_data.location]
        return position_data[['lat', 'lon', 'duration']]

    def average_position(self):
        position = self.position()
        time_total = position.duration.sum()
        avg_lat = (position.lat*position.duration).sum()/time_total
        avg_lon = (position.lon*position.duration).sum()/time_total
        return (avg_lat, avg_lon)

    def touch_map(self):
        map = plt.subplot()


my_match = load_match(event_list[0])
# my_final_match = my_match.window(start=(90, 0))
# my_match.window(15)
# my_match.team_match('Barcelona')
my_player = my_match.player_match(my_match.players[15])
my_player.average_position()

my_match.position_map('Barcelona')

team = 'Barcelona'

teams = my_match.teams
if team == teams[0]:
    idx_set = range(11)
else:
    idx_set = range(11,22)
average_position = {}
for player in my_match.lineup.player.iloc[idx_set]:
    pm = my_match.player_match(player)
    avg_pos = pm.average_position()
    average_position.update({player: avg_pos})

average_position = pd.DataFrame(average_position).T

field = plt.imread('img/field2.png')
fig, ax = plt.subplots()
ax.imshow(field, zorder=0, extent=[0, 120, 0, 80])
plt.scatter(average_position[0].iloc[:11],
            average_position[1].iloc[:11], c='blue', s=300, edgecolor='red')
ax.get_yaxis().set_visible(False)
ax.get_xaxis().set_visible(False)
lineup = my_match.lineup[idx_set]
for x in average_position.iterrows():
    name = x[0]
    lat, lon = x[1]
    idx = np.where(lineup.player == name)[0]
    jersey = str(int(lineup.jersey_number.iloc[idx]))
    plt.text(lat, lon, jersey, horizontalalignment='center',
            verticalalignment='center', c='white')
plt.plot()