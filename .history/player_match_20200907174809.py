
class player_match(match):
    """A player match class

    Args:
        match (match): The match the player was involved
    """

    def __init__(self, data, lineups):
        match.__init__(self, data, lineups)
        self.name = pd.unique([x['name'] for x in self.data.player])[0]

    def window(self, start, end=(100, 0)):
        if type(start) == int:
            start = (start, 0)
        if type(end) == int:
            end = (end, 0)
        time_data = self.data[['minute', 'second']]
        time_tup = [(t[1].minute, t[1].second) for t in time_data.iterrows()]
        time_idx = np.where([x >= start and x <= end for x in time_tup])[0]
        return player_match(self.data.iloc[time_idx], self.lineups)

    def average_position(self):
        """Calculates the players average position
        """

        def location(data):
            location_data = data[[
                'location', 'minute', 'second']].dropna()
            location_data['duration'] = 1
            location_data['lat'] = [x[0] for x in location_data.location]
            location_data['lon'] = [x[1] for x in location_data.location]
            return location_data[['lat', 'lon', 'duration']]
        position = location(self.data)
        time_total = position.duration.sum()
        avg_lat = (position.lat*position.duration).sum()/time_total
        avg_lon = (position.lon*position.duration).sum()/time_total
        return (avg_lat, avg_lon)

    def summary():
        summary_tbl = {team: {} for team in self.teams}
        match_duration = sum(self.data.duration.dropna())
        # Shots
        shots_idx = np.where(
            [x['name'] == 'Shot' for x in self.data.type])
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

        # Passes
        passes_idx = np.where(
            [x['name'] == 'Pass' for x in self.data.type])
        passes = self.data['pass'].iloc[passes_idx]
        assist = sum(['goal_assist' in x.keys()
                      for x in my_player.data['pass'].dropna()])
        passes_comp = [x for x in passes if not 'outcome' in x.keys()]
        passes_incomp = [x for x in passes if 'outcome' in x.keys(
        ) and x['outcome']['name'] in ['Incomplete', 'Out']]
        passes_offside = [x for x in passes if 'outcome' in x.keys(
        ) and x['outcome']['name'] in ['Pass Offside']]
        passes_to_shot = [x for x in passes if 'shot_assist' in x.keys()]
        cross = [x for x in passes if 'cross' in x.keys()]
        cross_comp = [x for x in cross if not 'outcome' in x.keys()]
        cross_incomp = [x for x in cross if 'outcome' in x.keys(
        ) and x['outcome']['name'] in ['Incomplete', 'Out']]
        pass_summary = {
            'assist': len(assist),
            'passes': len(passes),
            'passes_completed': round(len(passes_comp)/len(passes)*100, 2),
            'passes_incompleted': round(len(passes_incomp)/len(passes)*100, 2),
            'passes_to_shot': len(passes_to_shot),
            'offside': len(passes_offside),
            'crosses': len(cross),
            'crosses_completed': len(cross_comp),
            'crosses_incompleted': len(cross_incomp),
        }
        summary_tbl[team].update(pass_summary)

        # Fouls
        foul_idx = np.where(
            [x['name'] == 'Foul Committed' for x in self.data.type])[0]
        yellow_cards_foul = [x for x in self.data.foul_committed.dropna(
        ) if 'card' in x.keys() and x['card']['name'] in ['Yellow Card', 'Second Yellow']]
        yellow_cards_beh = [x for x in self.data.bad_behaviour.dropna(
        ) if 'card' in x.keys() and x['card']['name'] in ['Yellow Card', 'Second Yellow']]
        yellow_cards = yellow_cards_foul+yellow_cards_beh

        red_cards_foul = [x for x in self.data.foul_committed.dropna(
        ) if 'card' in x.keys() and x['card']['name'] in ['Red Card', 'Second Yellow']]
        red_cards_beh = [x for x in self.data.bad_behaviour.dropna(
        ) if 'card' in x.keys() and x['card']['name'] in ['Red Card', 'Second Yellow']]
        red_cards = red_cards_foul+red_cards_beh

        foul_summary = {
            'fouls': len(foul_idx),
            'yellow_cards': len(yellow_cards),
            'red_cards': len(red_cards)
        }

        return pd.DataFrame(summary_tbl)
