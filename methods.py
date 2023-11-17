# imports required
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree
import matplotlib.pyplot as plt

'''
method to get the accuracy of predicing the result of the game based on
player stats
'''
def get_decision_tree_accuracy(df, game_id):

    # split dataset in features and target variable
    feature_cols = ['tries', 'points', 'passes', 'runs', 'tryassists']

    # declare the features
    X = df[feature_cols]

    # decalre the target variable i.e., the result
    y = df.result

    # split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y,
    test_size = 0.3, random_state = 1)

    # create the classifer object
    classifier = DecisionTreeClassifier(max_depth = 3)

    # train the classifier
    classifier = classifier.fit(X_train,y_train)

    # predict the response for test dataset
    y_pred = classifier.predict(X_test)

    # display the model accuracy
    print(f"Accuracy for GameID {game_id}: {metrics.accuracy_score(y_test, y_pred):.2f}")

    '''
    # uncomment this code for the plotting of the data

    # plot the data
    fig, axes = plt.subplots(nrows = 1, ncols = 1, figsize = (5,5), dpi = 150)
    tree.plot_tree(classifier, filled = True, fontsize = 5)
    plt.show()
    '''


# return the match stats with regards to attacking
def return_match_stats(stats):

    # set the game
    game = stats['gamePackage']['matchAttacking']

    # find the match stats data required
    data = game['col'][1][0]['data']

    # create a dataframe
    df = pd.DataFrame(data)

    # return the dataframe
    return df


# method to return player stats from either from the home or away team
def return_player_stats(stats, home_away):

    # find the player from either the home or away
    team = stats['gamePackage']['matchLineUp'][home_away]['team']

    # create a dataframe
    df = pd.DataFrame(team)

    # number correspondes to their playing position
    df.index = df.number

    # prepare the df for analysis with helper method
    df = prep_df(df)

    # return the dataframe
    return df


# return the revserve player stats
def return_player_stats_reserves(stats, home_away):

    # find the reserves
    reserves = stats['gamePackage']['matchLineUp'][home_away]['reserves']

    # create the dataframe
    df = pd.DataFrame(reserves)

    # number correspondes to their playing position
    df.index = df.number

    # return the dataframe
    return df

# helper method to prepare the dataframe for analysis
def prep_df(df):

    # declare the lists required to hold the formatted data
    id_list = []
    tries_value_list = []
    points_value_list = []
    passes_value_list = []
    runs_value_list = []
    tryassists_value_list = []

    # iterate through the df
    for index, row in df.iterrows():

        # append the stripped data to the lists
        id_list.append(row['id'])
        tries_value_list.append(int(row['tries']['value']))
        points_value_list.append(int(row['points']['value']))
        passes_value_list.append(int(row['passes']['value']))
        runs_value_list.append(int(row['runs']['value']))
        tryassists_value_list.append(int(row['tryassists']['value']))

    # recreate the dataframe with the cleaned data
    df = pd.DataFrame({"id" : id_list, "tries" : tries_value_list,
    "points" : points_value_list,
    "passes" : passes_value_list, "runs" : runs_value_list, "tryassists": tryassists_value_list})

    # return the df
    return df
