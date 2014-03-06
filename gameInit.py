__author__ = 'gabe'
#! /usr/bin/python
import random
import stockroles
import time
import cmdinterface

class LogManager(object):
    lineCount = 0
    def __init__(self):
        logFileName = "log/log-%d.txt" %int(time.time())
        self.f = open(logFileName, 'w')
        self.lastMsg = ""


    def add_log_line(self, msg):
        if msg != self.lastMsg:
            self.f.write(str(LogManager.lineCount)+":    "+msg+"\n")
            LogManager.lineCount += 1
        self.lastMsg = msg

def make_player_list(availableRoles, selectedRoleList, playerCount, playerNameList):
    playerObjectList = []
    random.shuffle(selectedRoleList)

    for i in range(playerCount):
        playerObjectList.append(make_player_obj(selectedRoleList[i], playerNameList[i], availableRoles))
    return playerObjectList

def make_player_obj(roleNum, nickName, availableRoles):
    roleName = availableRoles[roleNum]
    playerObject = stockroles.rolesDict[roleName](nickName)
    return playerObject

def sort_by_night_rank(playerObjectList):
    playerObjectList.sort(key = lambda x: x.nightActionRank)


def night_phase(logObj, playerObjectList, reveal):
    """Cycle through the night turns"""
    logObj.add_log_line("The Night has started")
    logObj.add_log_line(":::::::::::::::::::::")
    stockroles.Werewolf.attacksRemaining = 1
    for i in playerObjectList:
        if i.blocked == 1:
            cmdinterface.player_inaction_message(i, "blocked")
        elif i.health < 1:
            cmdinterface.player_inaction_message(i, "dead")
        else:
            logLine=i.night_turn(playerObjectList)
        logObj.add_log_line(logLine)
        print(":-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:")
    logObj.add_log_line(":::::::::::::::::::::")

    """Check for Deaths"""
    diedInTheNight = []
    for i in playerObjectList:
        if i.attacked >= 1 and i.guarded == 0:
            i.health -= 1
            if i.health < 1:
                i.death_action(playerObjectList)
                diedInTheNight.append(i)
    cmdinterface.night_death_message(diedInTheNight, reveal)

    """Reset any night only attributes"""
    for i in playerObjectList:
        i.blocked=0
        i.attacked=0
        i.guarded=0

def day_phase(playerObjectList, reveal):
    while target != "Nobody":
        target = cmdinterface.pick_day_equip_user(playerObjectList)
        if target != "Nobody":cmdinterface.use_day_equip(playerObjectList, target)



logObj = LogManager()
reveal = True

playerCount = 6
playerNameList = ["Gabe","Dowd","Tom","Becca","Onslow","Andy"]
selectedRoleList=[14, 15, 17, 19, 20, 4]
#selectedRoleList=[0, 0, 0, 0, 0, 4]
availableRoles = list(stockroles.rolesDict.keys())
availableRoles = sorted(availableRoles)

#playerCount = int(input("Enter number of players: "))
#playerNameList = cmdinterface.playerNameEntry(playerCount)
#selectedRoleList, availableRoles = cmdinterface.rolePicker(playerCount)


playerObjectList = make_player_list(availableRoles, selectedRoleList, playerCount, playerNameList)

"""Sort players by their night rank attribute."""
playerObjectList.sort(key = lambda x: x.nightActionRank)

for obj in playerObjectList: cmdinterface.simple_player_info(obj)


night_phase(logObj, playerObjectList, reveal)

day_phase(playerObjectList, reveal)

for obj in playerObjectList: cmdinterface.simple_player_info(obj)
logObj.f.close()



