__author__ = 'gabe'

def rolePicker(playerCount):
    availableRoles = list(stockRoles.rolesDict.keys())
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


def playerNameEntry(playerCount):
    playerNameList = []
    while len(playerNameList) != playerCount:
        playerNameList = input("Enter the players nickname, space delimited :").split()
        if playerCount != len(playerNameList):
            print("Your player count does not match the number of nick names entered")

    return playerNameList

def simplePlayerInfo(playerObj):
    print("Nickname: %s" %playerObj.name)
    print("Role: %s" %playerObj.roleHR)
    print("Health: %s" %playerObj.health)
    print("------------------------------------")

def targetSelector(targetsList, msg=":::::::::", allowBlank=False):
    print(msg)
    for i in range(len(targetsList)):
        print(str(i)+": "+targetsList[i].name)
    if allowBlank == True:
        i = len(targetsList)
        print(str(i)+": Nobody")
        targetsList.append("Nobody")
    t=int(input("Select the corresponding number: "))
    return targetsList[t]

def givePlayerRoleInfo(player, target, infoType):
    if infoType == "role":
        print("You may show the "+player.roleHR+" ("+player.name+") that "+target.name+" is a "+target.roleHR+".")

    if infoType == "team":
        print("You may show the "+player.roleHR+" ("+player.name+") that "+target.name+" is a "+target.team+" team member.")

def playerInactionMessage(player, cause):
    print(player.roleHR+" ("+player.name+") may not act tonight, they are "+cause)

def nightDeathMessage(listOfDead, reveal):
    if len(listOfDead) > 0:
        print("The following players died in the night:")
        for i in listOfDead:
            if reveal == True:
                print(i.name+" the "+i.roleHR)
            else:
                print(i.name)
    else:
        print("There were no deaths this night")