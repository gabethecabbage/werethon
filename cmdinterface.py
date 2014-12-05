__author__ = 'gabe'

import stockroles

def role_picker(playerCount):
    availableRoles = list(stockroles.rolesDict.keys())
    availableRoles = sorted(availableRoles)
    roleList = []
    while len(roleList) != playerCount:
        for i in range(len(availableRoles)):
            print(i, availableRoles[i])
        roleList = input("Enter the roles required, space delimited :").split()
        if len(roleList) != playerCount:
            print("You have not selected enough roles for your player count")

    for i in range(len(roleList)):
        roleList[i] = int(roleList[i])

    return roleList, availableRoles


def player_name_entry(playerCount):
    playerNameList = []
    while len(playerNameList) != playerCount:
        playerNameList = input("Enter the players nickname, space delimited :").split()
        if playerCount != len(playerNameList):
            print("Your player count does not match the number of nick names entered")

    return playerNameList

def simple_player_info(playerObj):
    print("Nickname: %s" %playerObj.name)
    print("Role: %s" %playerObj.roleHR)
    print("Health: %s" %playerObj.health)
    print("------------------------------------")

def target_selector(targetsList, msg=":::::::::", allowBlank=False):
    print(msg)
    for i in range(len(targetsList)):
        print(str(i)+": "+targetsList[i].name)
    if allowBlank == True:
        i = len(targetsList)
        print(str(i)+": Nobody")
        targetsList.append("Nobody")
    t=int(input("Select the corresponding number: "))
    return targetsList[t]

def boolean_selector(boolList, msg=":::::::::"):
    """Asks for the user to pick one of two values e.g. true/false, yes/no, poop/pee, you decide!"""
    i = 0
    while i != 1:
        print(msg)
        ans = input("(" + boolList[0] + " or " + boolList[1] + "?) :")
        if ans != boolList[0] or ans != boolList[1]: print("That's not an option you tit!")
        else: i = 1

    return ans

def give_player_role_info(player, target, infoType):
    if infoType == "role":
        print("You may show the "+player.roleHR+" ("+player.name+") that "+target.name+" is a "+target.roleHR+".")

    if infoType == "team":
        print("You may show the "+player.roleHR+" ("+player.name+") that "+target.name+" is a "+target.team+" team member.")

def player_inaction_message(player, cause):
    msg = player.roleHR+" ("+player.name+") may not act tonight, they are "+cause
    print(msg)
    return msg

def night_death_message(listOfDead, reveal):
    if len(listOfDead) > 0:
        print("The following players died in the night:")
        for i in listOfDead:
            if reveal == True:
                print(i.name+" the "+i.roleHR)
            else:
                print(i.name)
    else:
        print("There were no deaths this night")
    print(":::::::::::::::::::::::::::::::::::")

def pick_day_equip_user(playerObjectList):
        playersWithEquip = []
        for player in playerObjectList:
            if len(player.atWillDayEquip) > 0:
                playersWithEquip.append(player)
        if len(playersWithEquip) > 0:
            msg="The following players have equipment. \nSelect a player if they use anything (or Nobody to progress to the voting)."
            equipUser = target_selector(playersWithEquip, msg, allowBlank=True)
            return equipUser
        else:
            return "Nobody"

def use_day_equip(playerObjectList, equipUser):
        print("What equipment did they use?")
        chosenEquip = target_selector(equipUser.atWillDayEquip, ":::::::::")
        chosenEquip.useEquipment(playerObjectList)
        equipUser.atWillDayEquip.remove(chosenEquip)
