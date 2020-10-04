#! /usr/bin/python
__author__ = "gabe"

import random
import stockroles
import time
import cmdinterface
import copy


def main():
    log = LogManager()
    reveal = True

    all_role_names = list(stockroles.roles_lookup.keys())
    all_role_names = sorted(all_role_names)

    player_count = int(input("Enter number of players: "))
    player_names = cmdinterface.playerNameEntry(player_count)
    role_names, all_role_names = cmdinterface.rolePicker(player_count)
    players = make_player_list(all_role_names, role_names, player_count, player_names)

    for obj in players:
        cmdinterface.simple_player_info(obj)
    day_night_cycle(log, players, reveal)
    for obj in players:
        cmdinterface.simple_player_info(obj)
    log.f.close()


class LogManager(object):
    line_count = 0

    def __init__(self):
        log_file_name = "log/log-%d.txt" % int(time.time())
        """create a log file in the log directory with a file name appended
        with the current unix time"""
        self.f = open(log_file_name, "w")

    def add_log_line(self, msg):
        self.f.write(str(LogManager.line_count) + ":    " + msg + "\n")
        LogManager.line_count += 1
        self.lastMsg = msg


def make_player_list(all_role_names, role_names, player_count, player_names):
    """Maps Players to shuffled list of role names"""
    players = []
    random.shuffle(role_names)

    for i in range(player_count):
        players.append(make_player_obj(role_names[i], player_names[i], all_role_names))
    """Sort players by their night rank attribute"""
    players.sort(key=lambda x: x.night_action_rank)
    return players


def make_player_obj(role_num, nickname, all_role_names):
    role_name = all_role_names[role_num]
    player = stockroles.roles_lookup[role_name](nickname)
    return player


def win_lose_check(players):
    live_players = [i for i in players if not i.health == 0]
    live_dark_team = [i for i in live_players if i.team == "Dark"]
    if len(live_dark_team) == 0:
        win_meta = "The Village has won by killing all the Dark forces!"
        return win_meta
    for plyr in players:
        win_meta = plyr.win_lose_logic(players)
        if win_meta is not None:
            return win_meta
    return None


def night_phase(log, players, reveal):
    """Cycle through the night turns"""
    log.add_log_line("The Night has started")
    log.add_log_line(":::::::::::::::::::::")
    stockroles.Werewolf.attacksRemaining = 1
    """for each player, run there night turn"""
    for i in players:
        """checks the player can use their night turn"""
        if i.blocked == 1:
            log_line = cmdinterface.player_inaction_message(i, "blocked")
        elif i.health < 1:
            log_line = cmdinterface.player_inaction_message(i, "dead")
        else:
            log_line = i.night_turn(players)
        log.add_log_line(log_line)
        print(":-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:")
    log.add_log_line(":::::::::::::::::::::")

    """Check for Deaths"""
    died_in_the_night = []
    for plyr in players:
        if plyr.attacked >= 1 and plyr.guarded == 0:
            plyr.health -= 1
            """dock 1 hp per unguarded attack"""
            if plyr.health < 1:
                plyr.death_action(players, "Night Attack")
                plyr.death_info = copy.deepcopy(plyr.attack_info)
                died_in_the_night.append(plyr)
    """returns a list of the dead and bool of the reveal rule"""
    cmdinterface.night_death_message(died_in_the_night, reveal)

    """Reset any night only attributes"""
    for plyr in players:
        plyr.blocked = 0
        plyr.attacked = 0
        plyr.guarded = 0
        plyr.attack_info = None


def day_phase(players, reveal):
    died_in_the_day = []
    equip_user = None
    live_players = [i for i in players if not i.health == 0]

    while equip_user != "Nobody":
        equip_user = cmdinterface.pick_day_equip_user(live_players)
        if equip_user != "Nobody":
            cmdinterface.use_day_equip(live_players, equip_user)
            live_players = [i for i in players if not i.health == 0]


def hanging(players):
    hangable_players = []

    for player in players:
        if player.health > 0:
            player.hang_action(players)
            hangable_players.append(player)

    hang_msg = "Select the player the group voted to hang."
    hang_victim = cmdinterface.target_selector(hangable_players, hang_msg, True)
    if hang_victim != "Nobody":
        hang_victim.health -= 1
        if hang_victim.health < 1:
            hang_victim.death_action(players, "hang")
            hang_victim.death_info = {
                "attacker_name": "Town",
                "attacker_role": "Town",
                "attack_cause": "hang",
            }


def day_night_cycle(log, players, reveal):
    while True:
        night_phase(log, players, reveal)
        win_meta = win_lose_check(players)
        if win_meta is not None:
            break

        day_phase(players, reveal)
        win_meta = win_lose_check(players)
        if win_meta is not None:
            break

        hanging(players)
        win_meta = win_lose_check(players)
        if win_meta is not None:
            break

    return win_meta


log = LogManager()
reveal = True

player_count = 6
player_names = ["Gabe", "Dowd", "Tom", "Becca", "Onslow", "Andy"]
print(stockroles.roles_lookup)
role_names = [0, 1, 5, 5, 5, 5]
all_role_names = list(stockroles.roles_lookup.keys())
all_role_names = sorted(all_role_names)


players = make_player_list(all_role_names, role_names, player_count, player_names)

for obj in players:
    cmdinterface.simple_player_info(obj)
win_meta = day_night_cycle(log, players, reveal)
for obj in players:
    cmdinterface.simple_player_info(obj)
print(win_meta)
log.f.close()
print("End of script")
