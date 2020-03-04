"""
Author: Soumyakanti (r.soumyakanti@gmail.com)
Last Modified: 9th February, 2020

Module to save Brawl Stars battle logs continuously using shelve.
The store_battle_logs function has to be recurrently called from 
another module to continuously update the data.

Recommended time intervals:
900 seconds for Professional Players
1800 seconds for Casual to Semi Professional Players

"""


import brawlstats
import box
import shelve
import time
from colorama import Fore


token = 'Get your API token from developer.brawlstars.com and paste it here within quotes'

def battle_logs_dict(client, player_tag):
    """
    Obtains the battle logs as JSON from the official API
    and converts them to a List of Dictionaries for manipulation

    Arguments:
    ----------

    client {brawlstats OfficialAPI Client Object} -- This is your client to access the data from the brawl stars servers

    player_tag {String} -- The player tag you want the battle logs for

    Returns:
    --------

    List of Dictionaries -- Your battle logs as obtained from Brawl Stars API as a List of Dictionaries
    """
    battle_log_list = []
    battles = client.get_battle_logs(player_tag)
    for battle in battles:
        # ignoring ticketed events because not competetive
        if not battle.battle.mode in set(['roboRumble']):
            battle_log_list.append(battle.to_dict())
    return battle_log_list


def store_battle_logs(client, player_tag):
    """
    Saves the battle log data as a shelf for manipulation in the future

    Arguments:
    ----------
    client {brawlstats OfficialAPI Client Object} : This is your client to access the data  from the brawl stars servers
    player_tag {String} : The player tag you want the battle logs for
    """
    list_of_battles = battle_logs_dict(client, player_tag)
    with shelve.open('data') as db : # currently saves in the root directory
        for battle in list_of_battles:
            # uses battle time as the database key
            db[battle["battleTime"]] = battle

    print(Fore.GREEN+f'Time: {time.ctime()}|'+Fore.CYAN+f'👦 {player_tag}')


def main():

    client = brawlstats.OfficialAPI(token)

    # can contain only the following 0289PYLQGRJCUV
    player_tag = 'Paste your player tag'

    store_battle_logs(client, player_tag)
    # currently only a basic module, will add more arguments soons


if __name__ == "__main__":
    main()
