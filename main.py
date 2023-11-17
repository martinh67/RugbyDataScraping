# imports required
import requests
import json
import re
from methods import *

# main method
def main():
    '''
    game id 295492 is Wales vs Italy - Home win
    game id 295493 is Ireland vs Scotland - Home win
    game id 295494 is France vs England - Home win

    '''

    # define url to be used
    url = "https://www.espn.com/rugby/matchstats?gameId={}&league=180659"

    # the first game of the 6 nations
    game_id = 295492

    # for the first 3 games in the 6 nations i.e., 295492 to 295494
    for i in range(3):

        # update the url
        update_url = url.format(game_id)

        # create the response
        response = requests.get(update_url)

        # get the game stats
        stats = json.loads(re.search(r"window.__INITIAL_STATE__ = ({.*})",
        response.text).group(1))

        match_stats = return_match_stats(stats)

        # create a dataframe with the home stats
        home_stats = return_player_stats(stats, "home")

        # set the home result to a win i.e., 1
        home_stats['result'] = 1

        # create a dataframe with the away stats
        away_stats = return_player_stats(stats, "away")

        # set the away result to a loss i.e., 0
        away_stats['result'] = 0

        # get the home and away stats for the game by concatenating the dfs
        game_stats = pd.concat([home_stats, away_stats], join = "outer")

        # build the decision tree and get the accuracy
        get_decision_tree_accuracy(game_stats, game_id)

        # increment the game id
        game_id += 1


# magic method to run main
if __name__ == "__main__":

    # run main
    main()
