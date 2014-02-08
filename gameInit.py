__author__ = 'gabe'
#! /usr/bin/python
import random
import stockroles
import cmdinterface


def makePlayerList(availableRoles, selectedRoleList, playerCount, playerNameList):
    playerObjectList = []
    random.shuffle(selectedRoleList)

    for i in range(playerCount):
        playerObjectList.append(makePlayerObjects(selectedRoleList[i], playerNameList[i], availableRoles))
    return playerObjectList

def makePlayerObjects(roleNum, nickName, availableRoles):
    roleName = availableRoles[roleNum]
    playerObject = stockroles.rolesDict[roleName](nickName)
    return playerObject

def sortByNightRank(playerObjectList):
    playerObjectList.sort(key = lambda x: x.nightActionRank)


def nightPhase(playerObjectList, reveal):
    """Cycle through the night turns"""
    stockroles.Werewolf.attacksRemaining = 1
    for i in playerObjectList:
        if i.blocked == 1:
            cmdinterface.playerInactionMessage(i, "blocked")
        elif i.health < 1:
            cmdinterface.playerInactionMessage(i, "dead")
        else:
            i.nightTurn(playerObjectList)
        print(":-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:")

    """Check for Deaths"""
    diedInTheNight = []
    for i in playerObjectList:
        if i.attacked >= 1 and i.guarded == 0:
            print(i)
            i.health -= 1
            if i.health < 1:
                i.deathAction(playerObjectList)
                diedInTheNight.append(i)
    cmdinterface.nightDeathMessage(diedInTheNight, reveal)

    """Reset any night only attributes"""
    for i in playerObjectList:
        i.blocked=0
        i.attacked=0
        i.guarded=0

def dayPhase(playerObjectList, reveal):
    useDayEquip(playerObjectList)


def useDayEquip(playerObjectList):
    playersWithEquip = ["filler string"]
    while len(playersWithEquip) > 0:
        playersWithEquip = []
        for i in playerObjectList:
            if len(i.atWillDayEquip) > 0:
                playersWithEquip.append(i)
        if len(playersWithEquip) > 0:
            msg="The following players have equipment. \n Select a player if they use anything (or Nobody to progress to the voting)."
            target = cmdinterface.targetSelector(playersWithEquip, msg, allowBlank=True)
            if target != "Nobody":
                print("What equipment did they use?")
                chosenEquip = cmdinterface.targetSelector(target.atWillDayEquip, ":::::::::")
                chosenEquip.useEquipment(playerObjectList)
                target.atWillDayEquip.remove(chosenEquip)
            else: pass



reveal = True
playerCount = 6
playerNameList = ["Gabe","Dowd","Tom","Becca","Onslow","Andy"]
selectedRoleList=[0, 15, 17, 19, 20, 4]
#selectedRoleList=[0, 0, 0, 0, 0, 4]
availableRoles = list(stockroles.rolesDict.keys())
availableRoles = sorted(availableRoles)

playerObjectList = makePlayerList(availableRoles, selectedRoleList, playerCount, playerNameList)

sortByNightRank(playerObjectList)
print("::::::::::::::::::::::::")
for obj in playerObjectList: cmdinterface.simplePlayerInfo(obj)

nightPhase(playerObjectList, reveal)

dayPhase(playerObjectList, reveal)

for obj in playerObjectList: cmdinterface.simplePlayerInfo(obj)


import cmdinterface
#playerCount = int(input("Enter number of players: "))
#playerNameList = cmdInterface.playerNameEntry(playerCount)
#selectedRoleList, availableRoles = cmdInterface.rolePicker(playerCount)

