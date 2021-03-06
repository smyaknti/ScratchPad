"""
Author: Soumyakanti (r.soumyakanti@gmail.com)
Last Modified: 4th March, 2020

Module to analyse (currently only print) the Battle log
of the entire database stored using the Store_battle_logs.py

Changes: 
1. Added comprehensive battle logs! Enjoy!
2. Extensive Code Cleanup
3. Elaborate Trophy changes
4. Colourful and organised CLI output

"""


import shelve
from box import Box
import box
import pprint
import time
from colorama import Fore, init
init(autoreset=True)

width_index = 5
width_brawler = 8
width_gamemode = 13
width_powerplay = 35

name_lookup = {
   'soloShowdown': 'Solo Showdown',
   'duoShowdown' : 'Duo Showdown',
   'brawlBall' : 'Brawl Ball',
   'gemGrab': 'Gem Grab',
   'heist': 'Heist',
   'siege': 'Siege',
   'bounty': 'Bounty',
   'bigGame': 'Big Game',
   'roboRumble':'Robo Rumble',
   'bossFight':'Boss Fight',
   'hotZone':'Hot Zone'
}
soloPP = {
   1:38,
   2:34,
   3:30,
   4:26,
   5:22,
   6:18,
   7:14,
   8:10,
   9:6,
   10:2
}

duoPP = {
   1:34,
   2:26,
   3:18,
   4:10,
   5:2
}

def is_powerplay(battle):
   try:
      if battle.battle.mode == 'soloShowdown':
         if soloPP[battle.battle.rank] == battle.battle.trophyChange:
            return True
         else: return False
      elif battle.battle.mode == 'duoShowdown':
         if duoPP[battle.battle.rank] == battle.battle.trophyChange:
            return True
         else: return False
      else:
         if battle.battle.trophyChange > 8:
            return True
         else:
            if battle.battle.result == 'defeat' and battle.battle.trophyChange > 0:
               return True
            else: return False
   except box.exceptions.BoxKeyError:
      pass

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
    player_tag = '#'+player_tag.upper()
    if battle.mode in set([ 'bigGame','roboRumble']):
        return None
    elif battle.mode == 'soloShowdown':
            for i in range (10):
                if battle.players[i].tag == player_tag:
                    return battle.players[i].brawler
    elif battle.mode == 'duoShowdown':
        for i in range (5):
            for j in range(2):
                if battle.teams[i][j].tag == player_tag:
                    return battle.teams[i][j].brawler
    else: 
        for i in range(2):
            for j in range(3):
                if battle.teams[i][j].tag == player_tag:
                    return battle.teams[i][j].brawler



def sign(value): return ('-','+')[value >= 0]

def colourise(value):
    if value in set(['+', 'victory']):
        return Fore.GREEN
    elif value in set(['-','defeat']):
        return Fore.RED

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

    print(f'{"Num.":^{width_index}}|{"Game Mode":^{width_gamemode+1}}|{"Brawler":^{width_brawler+9}}|{"Outcome":^{20}}\n{"-"*60}')
    brawler_trophy_change = {}
    if player_tag[0] == '#':
        player_tag = player_tag[1:]
    listofkeys = list(data.keys())
    listofkeys.sort(reverse=True)
    trophy_change = 0
    index = 1
    

    for key in listofkeys:
        battle = Box(data[key])
        powerPlay = is_powerplay(battle)
        brawler = get_brawler_played(battle.battle,player_tag)
        if battle.battle.mode in set(['bigGame','roboRumble']):
            pass
        elif battle.battle.mode in set([ 'soloShowdown','duoShowdown']): 
            if battle.battle.type == 'ranked' and brawler != None:
                if powerPlay:
                    pptext = f'Power Play ({brawler.trophies})'
                    brawler_details = f'{Fore.MAGENTA}{brawler.name:>{width_brawler}}\n{pptext:>{width_powerplay}}'
                else:
                    brawler_details = f'{Fore.LIGHTBLUE_EX}{brawler.name:>{width_brawler}} ({brawler.trophies})'
            elif brawler != None:
                brawler_details = f'{Fore.WHITE}{brawler.name:>{width_brawler}} (Fri)'  
            try:
                print(f'{index:>{width_index}}. {Fore.GREEN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Rank: {battle.battle.rank} {colourise(sign(battle.battle.trophyChange))}({sign(battle.battle.trophyChange)}{abs(battle.battle.trophyChange)})')
                trophy_change += battle.battle.trophyChange
                if powerPlay:
                    if 'POWER-PLAY Points' in brawler_trophy_change:
                        brawler_trophy_change['POWER-PLAY Points']+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change['POWER-PLAY Points']=battle.battle.trophyChange
                else:
                    if brawler.name in brawler_trophy_change:
                        brawler_trophy_change[brawler.name]+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change[brawler.name]=battle.battle.trophyChange
                
            except box.exceptions.BoxError:
                print(f'{index:>{width_index}}. {Fore.GREEN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Rank: {battle.battle.rank}')

        else:
            if battle.battle.type == 'ranked' and brawler != None:
                if powerPlay:
                    pptext = f'Power Play ({brawler.trophies})'
                    brawler_details = f'{Fore.MAGENTA}{brawler.name:>{width_brawler}}\n{pptext:>{width_powerplay}}'
                else:
                    brawler_details = f'{Fore.LIGHTBLUE_EX}{brawler.name:>{width_brawler}} ({brawler.trophies})'
            elif brawler != None:
                  brawler_details = f'{Fore.WHITE}{brawler.name:>{width_brawler}} (Fri)' 
            try:
                print(f'{index:>{width_index}}. {Fore.CYAN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Result: {colourise(battle.battle.result)}{battle.battle.result} {colourise(sign(battle.battle.trophyChange))}({sign(battle.battle.trophyChange)}{abs(battle.battle.trophyChange)})')
                trophy_change += battle.battle.trophyChange
                if powerPlay:
                    if 'POWER-PLAY Points' in brawler_trophy_change:
                        brawler_trophy_change['POWER-PLAY Points']+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change['POWER-PLAY Points']=battle.battle.trophyChange
                else:
                    if brawler.name in brawler_trophy_change:
                        brawler_trophy_change[brawler.name]+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change[brawler.name]=battle.battle.trophyChange
            except box.exceptions.BoxKeyError:
                print(f'{index:>{width_index}}. {Fore.CYAN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Result: {colourise(battle.battle.result)}{battle.battle.result}{Fore.RESET}')
        index += 1
    brawler_trophy_changes = ''
    for key, value in brawler_trophy_change.items():
        brawler_trophy_changes += f'{key:<{17}} : {colourise(sign(value))}{sign(value)}{abs(value):>{4}}{Fore.RESET} \n'
    if 'POWER-PLAY Points' in brawler_trophy_change:
            deduct_from_total = brawler_trophy_change['POWER-PLAY Points']
    else: deduct_from_total = 0
    print(f'\nFor {len(listofkeys)} games, total Trophy change was {colourise(sign(trophy_change))}{sign(trophy_change)}{abs(trophy_change-deduct_from_total)}{Fore.RESET}\n{"-"*50}\n{brawler_trophy_changes} {Fore.RESET}')


if __name__ == "__main__":

    # can contain only the following 0289PYLQGRJCUV
    player_tag = 'Paste your player tag'

    # the file you saved in the store_battle_logs.py
    with shelve.open('data') as data:
    	battle_log(data, player_tag)
