import matplotlib.patches as patches
from match import *

match_id = 15946
my_match = load_match(match_id)

# # Dribble

# carries = [x[1] for x in my_player.data.iterrows() if x[1]['type']
#            ['name'] == 'Carry']
# dribbles = [x[1]['dribble']
#             for x in my_player.data.iterrows() if x[1]['type']['name'] == 'Dribble']
# dribbles_comp = [x for x in dribbles if x['outcome']['name'] == 'Complete']

# dribble_summary = {
#     'carries': len(carries),
#     'dribbles': len(dribbles),
#     'dribbles_complete': len(dribbles_comp),
#     'dribbles_incomplete': len(dribbles) - len(dribbles_comp)
# }

# # Defense

# ball_rec_idx = np.where(
#     [x['name'] == 'Ball Recovery' for x in my_player.data['type']])
# ball_rec = my_player.data.iloc[ball_rec_idx]
# ball_rec_failure = [
#     x for x in ball_rec['ball_recovery'].dropna() if 'recovery_failure' in x.keys()]
# ball_rec_offensive = [
#     x for x in ball_rec['ball_recovery'].dropna() if 'offensive' in x.keys()]

# interception_idx = np.where(
#     [x['name'] == 'Interception' for x in my_player.data['type']])
# interception = my_player.data.iloc[interception_idx].interception
# interception_won = [x for x in interception if x['outcome']['name'] == 'Won']

# duel_idx = np.where([x['name'] == 'Duel' for x in my_player.data['type']])
# duel = my_player.data.iloc[duel_idx].duel
# aerial_duel = [x for x in duel if x['type']['name'] == 'Aerial Lost']

# # Pass Network

lineup_path = 'data/lineups/%i.json' % match_id
lineups = pd.read_json(lineup_path)
