#! /usr/bin/python
__author__ = 'gabe'

import random
import stockroles
import time
import cmdinterface
import copy

def main():
    logObj = LogManager()
    reveal = True

    availableRoles = list(stockroles.rolesDict.keys())
    availableRoles = sorted(availableRoles)

    playerCount = int(input("Enter number of players: "))
    playerNameList = cmdinterface.playerNameEntry(playerCount)
    selectedRoleList, availableRoles = cmdinterface.rolePicker(playerCount)
    playerObjectList = make_player_list(availableRoles, selectedRoleList, playerCount, playerNameList)

    for obj in playerObjectList: cmdinterface.simple_player_info(obj)
    day_night_cycle(logObj, playerObjectList, reveal)
    for obj in playerObjectList: cmdinterface.simple_player_info(obj)
    logObj.f.close()


class LogManager(object):
    lineCount = 0
    def __init__(self):
        logFileName = "log/log-%d.txt" %int(time.time())
        """create a log file in the log directory with a file name appended with the current unix time"""
        self.f = open(logFileName, 'w')
        self.lastMsg = "" #this string stores the last know log entry in the object, part of the ugly hack below


    def add_log_line(self, msg):
        if msg != self.lastMsg: #check log item isn't same as last
            """this is a nasty hack to stop a duplication issue in the log I couldn't be bothered to debug"""
            self.f.write(str(LogManager.lineCount)+":    "+msg+"\n") #write log message
            LogManager.lineCount += 1 #roll over to next line of log
        self.lastMsg = msg

"""Makes a list to store player objects and the shuffles the order to keep play to role assignment random"""
def make_player_list(availableRoles, selectedRoleList, playerCount, playerNameList):
    playerObjectList = []
    random.shuffle(selectedRoleList)

    for i in range(playerCount): #creates each player in a loop
        playerObjectList.append(make_player_obj(selectedRoleList[i], playerNameList[i], availableRoles))
    """Sort players by their night rank attribute. This determins the order they act in the night"""
    playerObjectList.sort(key=lambda x: x.nightActionRank)
    return playerObjectList

def make_player_obj(roleNum, nickName, availableRoles):
    roleName = availableRoles[roleNum]
    playerObject = stockroles.rolesDict[roleName](nickName)
    return playerObject

def win_lose_check(playerObjectList, won):
    for plyr in playerObjectList:
        winMeta = plyr.win_lose_logic(playerObjectList)
        if winMeta != None:
            print(winMeta)
            exit()


def night_phase(logObj, playerObjectList, reveal):
    """Cycle through the night turns"""
    logObj.add_log_line("The Night has started")
    logObj.add_log_line(":::::::::::::::::::::")
    stockroles.Werewolf.attacksRemaining = 1 #gives the werewolf objects all one joint attack
    """for each player, run there night turn"""
    for i in playerObjectList:
        #checks the player can use there night turn function before running it
        if i.blocked == 1:
            logLine = cmdinterface.player_inaction_message(i, "blocked")
        elif i.health < 1:
            logLine = cmdinterface.player_inaction_message(i, "dead")
        else:
            logLine = i.night_turn(playerObjectList)
        logObj.add_log_line(logLine)
        print(":-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:")
    logObj.add_log_line(":::::::::::::::::::::")

    """Check for Deaths"""
    diedInTheNight = []
    for plyr in playerObjectList:
        if plyr.attacked >= 1 and plyr.guarded == 0:
            plyr.health -= 1
            #dock 1 hp per unguarded attack
            if plyr.health < 1:
                plyr.death_action(playerObjectList, "Night Attack")
                plyr.deathInfo = copy.deepcopy(plyr.attackInfo)
                diedInTheNight.append(plyr)
    #returns a list of the dead and bool of the reveal rule
    cmdinterface.night_death_message(diedInTheNight, reveal)

    """Reset any night only attributes, these properties currently cant travel over day-night cycles"""
    for plyr in playerObjectList:
        plyr.blocked = 0
        plyr.attacked = 0
        plyr.guarded = 0
        plyr.attackInfo = None

def day_phase(playerObjectList, reveal):
    diedInTheDay = []
    equipUser = None

    while equipUser != "Nobody":
        equipUser = cmdinterface.pick_day_equip_user(playerObjectList)
        if equipUser != "Nobody":
            cmdinterface.use_day_equip(playerObjectList, equipUser)

def lynching(playerObjectList):
    lynchablePlayers = []

    for player in playerObjectList:
        if player.health > 0:
            player.lynch_action(playerObjectList)
            lynchablePlayers.append(player)

    lynchVictim = cmdinterface.target_selector(lynchablePlayers, "Select the player the group voted to lynch.", True)
    lynchVictim.health -= 1
    if lynchVictim.health < 1:
        lynchVictim.death_action(playerObjectList, "lynch")
        lynchVictim.deathInfo = {'attackerName': "Town", 'attackerRole': "Town", 'attackCause': "lynch"}

def day_night_cycle(logObj, playerObjectList, reveal):
    won = 0
    while won == 0:
        night_phase(logObj, playerObjectList, reveal)
        win_lose_check(playerObjectList, won)
        day_phase(playerObjectList, reveal)
        win_lose_check(playerObjectList, won)
        lynching(playerObjectList)
        win_lose_check(playerObjectList, won)

logObj = LogManager()
reveal = True

playerCount = 6
playerNameList = ["Gabe","Dowd","Tom","Becca","Onslow","Andy"]
selectedRoleList=[14, 15, 17, 19, 20, 4]
availableRoles = list(stockroles.rolesDict.keys())
availableRoles = sorted(availableRoles)


playerObjectList = make_player_list(availableRoles, selectedRoleList, playerCount, playerNameList)

for obj in playerObjectList: cmdinterface.simple_player_info(obj)
day_night_cycle(logObj, playerObjectList, reveal)
for obj in playerObjectList: cmdinterface.simple_player_info(obj)
logObj.f.close()



