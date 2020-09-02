import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def load_match(file):
    match_data = pd.read_json(file)
    return(match(match_data))


class match(object):
    # TODO: Change definition to FULL MATCH and CHILD MATCH. Child Match inherits the lineups from the initial match but excludes the subed-out (not subed-in) ones
    # TODO: Set the definition of ACTIVE PLAYERS in that match
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
        self.active_time = [min(time_tup), max(time_tup)]
        self.players = pd.unique([x['name']
                                  for x in self.data.player.dropna()])

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

    def position_map(self, starting=True):
        field = plt.imread('img/field2.png')
        for i in range(len(self.teams)):
            team = self.teams[i]
            average_position = {}
            team_players = self.team_match(team).players
            if starting == True:
                idx = range(11)
            else:
                idx = range(len(team_players))
            for player in team_players[idx]:
                pm = self.player_match(player)
                avg_pos = pm.average_position()
                average_position.update({player: avg_pos})

            average_position = pd.DataFrame(average_position).T

            # Figure
            fig, ax = plt.subplots()
            ax.imshow(field, zorder=0, extent=[0, 120, 0, 80])
            plt.scatter(average_position[0],
                        80-average_position[1], c='blue', s=300, edgecolor='red')
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            plt.title(team+' Average Positioning')
            return fig

    def summary(self):
        summary_tbl = {team: {} for team in self.teams}
        for team in self.teams:
            team_match = self.team_match(team)
            shots_idx = np.where(
                [x['name'] == 'Shot' for x in team_match.data.type])
            shots = team_match.data['shot'].iloc[shots_idx]
            shots_on_tgt = [x for x in shots if x['outcome']
                            ['name'] in ['Goal', 'Saved']]
            shots_off_tgt = [x for x in shots if x['outcome']['name'] in [
                'Off T', 'Post', 'Saved Off T', 'Saved To Post', 'Wayward']]
            shots_blocked = [
                x for x in shots if x['outcome']['name'] == 'Blocked']
            goals = [x for x in shots if x['outcome']['name'] == 'Goal']

            shot_summary = {
                'goals': len(goals),
                'shots': len(shots),
                'shots_on_target': len(shots_on_tgt),
                'shots_off_target': len(shots_off_tgt),
                'shots_blocked': len(shots_blocked)
            }
            summary_tbl[team].update(shot_summary)

            passes_idx = np.where(
                [x['name'] == 'Pass' for x in team_match.data.type])
            passes = team_match.data['pass'].iloc[passes_idx]

            passes_comp = [x for x in passes if not 'outcome' in x.keys()]
            passes_incomp = [x for x in passes if 'outcome' in x.keys(
            ) and x['outcome']['name'] in ['Incomplete', 'Out']]
            passes_offside = [x for x in passes if 'outcome' in x.keys(
            ) and x['outcome']['name'] in ['Pass Offside']]
            cross = [x for x in passes if 'cross' in x.keys()]
            cross_comp = [x for x in cross if not 'outcome' in x.keys()]
            cross_incomp = [x for x in cross if 'outcome' in x.keys(
            ) and x['outcome']['name'] in ['Incomplete', 'Out']]
            pass_summary = {
                'passes': len(passes),
                'passes_completed': round(len(passes_comp)/len(passes)*100, 2),
                'passes_incompleted': round(len(passes_incomp)/len(passes)*100, 2),
                'offside': len(passes_offside),
                'crosses': len(cross),
                'crosses_completed': len(cross_comp),
                'crosses_incompleted': len(cross_incomp),
            }
            summary_tbl[team].update(pass_summary)
        return pd.DataFrame(summary_tbl)


class player_match(match):
    def __init__(self, data):
        match.__init__(self, data)
        self.name = pd.unique([x['name'] for x in self.data.player])[0]

    def window(self, start, end=(100, 0)):
        if type(start) == int:
            start = (start, 0)
        if type(end) == int:
            end = (end, 0)
        time_data = self.data[['minute', 'second']]
        time_tup = [(t[1].minute, t[1].second) for t in time_data.iterrows()]
        time_idx = np.where([x >= start and x <= end for x in time_tup])[0]
        return player_match(self.data.iloc[time_idx])

    def position(self):
        position_data = self.data[['location', 'minute', 'second']].dropna()
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

    def touch_map(self, type=None):
        touch_name = ['Ball Received', 'Ball Recovery*', 'Carry', 'Dribble',
                      'Interception', 'Miscontrol', 'Pass', 'Shot']  # ? Foul Won?
        if not type == None:
            list(set(touch_name) & set(type))
        touch_idx = np.where(
            [x['name'] in touch_name for x in self.data.type])[0]
        touches = self.data.iloc[touch_idx][['location']]
        lat = [x[0][0] for x in touches.values]
        lon = [x[0][1] for x in touches.values]
        field = plt.imread('img/field2.png')
        fig, ax = plt.subplots()
        ax.imshow(field, zorder=0, extent=[0, 120, 0, 80])
        plt.scatter(lat, 80-lon, c='blue', s=50, edgecolor='red')
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        plt.title(self.name+' Touch Map')
        return fig
