"""
Author: Soumyakanti (r.soumyakanti@gmail.com)
Last Modified: 10th February, 2020

Module to analyse (currently only print) the Battle log
of the entire database stored using the Store_battle_logs.py

More features coming soon.

"""


import shelve
from box import Box
import box


def battle_log(data, player_tag):
    """
    battle_log Prints out the entire battle log in a comprehensive

    Parameters
    ----------
    data : {DbfilenameShelf}
        Your battle log database saved using store_battle_logs.py

    player_tag : {String}
        Your brawl stars Player tag
    """
    listofkeys = list(data.keys())
    listofkeys.sort(reverse=True)
    total_change = 0
    for key in listofkeys:
        battle = Box(data[key])
        if not battle.battle.mode in set(['roboRumble']):
            try:
                if battle.battle.trophyChange < 0:

                    print("You lost", abs(battle.battle.trophyChange),
                          "Trophies in", battle.battle.mode)
                    if not battle.battle.mode in set(['soloShowdown', 'duoShowdown', 'roboRumble']):
                        print("Star Player was a", battle.battle.starPlayer.brawler.power, " power up ",
                              battle.battle.starPlayer.brawler.name, " played by ", battle.battle.starPlayer.name, "(", battle.battle.starPlayer.tag, ")")

                else:
                    print("You gained", battle.battle.trophyChange,
                          "Trophies in", battle.battle.mode)
                    if not battle.battle.mode in set(['soloShowdown', 'duoShowdown', 'roboRumble']):
                        print("Star Player was a", battle.battle.starPlayer.brawler.power, "power up",
                              battle.battle.starPlayer.brawler.name, "played by", battle.battle.starPlayer.name, "(", battle.battle.starPlayer.tag, ")")

                total_change += battle.battle.trophyChange

            except box.exceptions.BoxKeyError:
                if battle.battle.mode == 'duoShowdown':
                    if battle.battle.rank in set([3, 4, 5]):
                        print("No trophy changes in", battle.battle.mode)
                elif battle.battle.mode in set(['brawlBall', 'bounty', 'hotZone']):
                    if battle.battle.result == 'draw':
                        print("No trophy changes in", battle.battle.mode)

            except:
                print("You screwed something up son!")

            brawler_played = get_brawler_played(battle.battle, player_tag)
            if not brawler_played == 0:
                print("You played a", brawler_played.power, "power-up",
                      brawler_played.name, "at", brawler_played.trophies, "Trophies!")
            print('')

    print("You overall trophy turnover:", total_change)


def get_brawler_played(battle, player_tag):
    """
    get_brawler_played Returns the brawler you played in the battle.

    Parameters
    ----------
    battle : {Box}
        The battle you played.

    player_tag : {String}
        Your brawl stars player tag

    Returns
    -------
    {Box}
        The brawler you played as a Box object
    """

    if battle.mode in set(['soloShowdown', 'duoShowdown', 'roboRumble']):
        return 0
    else:
        for i in range(2):
            for j in range(3):
                if battle.teams[i][j].tag == '#'+player_tag:
                    return battle.teams[i][j].brawler


if __name__ == "__main__":

    # can contain only the following 0289PYLQGRJCUV
    player_tag = 'Paste your player tag'

    # the file you saved in the store_battle_logs.py
    with shelve.open('data') as data:
    	battle_log(data, player_tag)
