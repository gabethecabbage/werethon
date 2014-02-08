__author__ = 'gabe'
import cmdinterface
import time

class Player(object):
    idCounter = 0
    #Common base class for all players
    def __init__(self, name, role):
        self.name = name
        self.roleHR = role
        self.numID = Player.idCounter
        self.health = 1
        self.atWillDayEquip = []
        self.attacked = 0
        self.suicided = 0
        self.blocked = 0
        self.guarded = 0
        self.nightActionRank = 100.0

        Player.idCounter += 1

    def nightTurn(self,playerObjectList):
        pass
        logLine = "The "+self.roleHR+" ("+self.name+") has no night action."
        return logLine

    def deathAction(self, playerObjectList):
        pass

    def displayCount(self):
        print("Total Players %d" %Player.playerCount)

"""ROLE CLASSES"""
class Werewolf(Player):
    attacksRemaining=0
    def __init__(self, name, roleHR):
        super(Werewolf, self).__init__(name, roleHR)
        self.team = "Dark"
        self.werewolf = True
        self.nightActionRank = 2.0
        self.purpose = "maul"

    def nightTurn(self,playerObjectList):
        logLine = wolfTeamTurn(playerObjectList)
        return logLine



class AlphaWolf(Werewolf):
    def __init__(self, name):
        super(AlphaWolf, self).__init__(name, "Alpha Werewolf")

class BetaWolf(Werewolf):
    def __init__(self, name):
        super(BetaWolf, self).__init__(name, "Beta Werewolf")

class SilverWolf(Werewolf):
    def __init__(self, name):
        super(SilverWolf, self).__init__(name, "Silver Wolf")

class StalkerWolf(Werewolf):
    def __init__(self, name):
        super(StalkerWolf, self).__init__(name, "Stalker Wolf")
        self.nightActionRank = 4.0
        self.purpose = "inspect"

    def nightTurn(self,playerObjectList):
        logLine = wolfTeamTurn(playerObjectList)
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targetsList.append(i)

        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg)
        cmdinterface.givePlayerRoleInfo(self, target, "role")
        logLine = logLine+"The "+self.roleHR+" ("+self.name+") then chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

class Succubus(Werewolf):
    def __init__(self, name):
        super(Succubus, self).__init__(name, "Succubus")
        self.nightActionRank = 3.0
        self.purpose = "block"

    def nightTurn(self,playerObjectList):
        logLine = wolfTeamTurn(playerObjectList)
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targetsList.append(i)

        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg)
        target.blocked=1
        logLine = logLine+"The "+self.roleHR+" ("+self.name+") then chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

"""Additional wolf class functions"""
def findLiveWereWolves(playerObjectList):
    wolfList=[]
    wolfCount=0
    wolfPlayerNames=[]
    for i in playerObjectList:
        if not i.health<1 and hasattr(i, "werewolf"):
            wolfPlayerNames.append(i.name)

    return wolfPlayerNames

def wolfTeamTurn(playerObjectList):
    logLine = ""
    if Werewolf.attacksRemaining > 0:
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targetsList.append(i)

        wolfPlayerNames=findLiveWereWolves(playerObjectList)
        namesString=",".join(wolfPlayerNames)
        msg="Ask the Werewolf team ("+namesString+") who they would like to maul."
        target= cmdinterface.targetSelector(targetsList, msg, allowBlank=True)

        if target == "Nobody":
            logLine = "The Werewolf team ("+namesString+") chose to maul no one. Very sneaky, eh? "
        elif target.guarded == 1:
            logLine = "The Werewolf team ("+namesString+") tried to maul "+target.roleHR+" ("+target.name+"), but they were protected tonight. "
        else:
            target.attacked = 1
            logLine = "The Werewolf team ("+namesString+") chose to maul "+target.roleHR+" ("+target.name+"). "

        Werewolf.attacksRemaining -= 1
    return logLine


class SerialKiller(Player):
    def __init__(self, name):
        super(SerialKiller, self).__init__(name, "Serial Killer")
        self.team = "Dark"
        self.nightActionRank = 5.0
        self.purpose = "stab"

    def nightTurn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg)
        target.attacked = 1
        logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        returnlogLine

"""COMPLETE LATER"""
class Cupid(Player):
    def __init__(self, name):
        super(Cupid, self).__init__(name, "Cupid")
        self.team = "Light"

class Fletcher(Player):
    def __init__(self, name):
        super(Fletcher, self).__init__(name, "Fletcher")
        self.team = "Light"
        self.nightActionRank = 10.0
        self.purpose = "bestow an arrow upon"

    def nightTurn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg, allowBlank=True)
        if target == "Nobody": logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" nobody, how dull..."
        else:
            target.atWillDayEquip.append(Arrow(target,self))
            logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

class Guardian(Player):
    def __init__(self, name):
        super(Guardian, self).__init__(name, "Guardian")
        self.team = "Light"
        self.nightActionRank = 1.0
        self.purpose = "protect"
        self.lastPlayerGuarded = None

    def nightTurn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if i.health > 0 and i.numID != self.lastPlayerGuarded:
                targetsList.append(i)
    #Should they be able to choose no one?
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg)
        target.guarded = 1
        self.lastPlayerGuarded = target.numID

class Insomniac(Player):
    def __init__(self, name):
        super(Insomniac, self).__init__(name, "Insomniac")
        self.team = "Light"

class Seer(Player):
    def __init__(self, name):
        super(Seer, self).__init__(name, "Seer")
        self.team = "Light"
        self.nightActionRank = 7.0
        self.purpose = "inspect"

    def nightTurn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg)
        cmdinterface.givePlayerRoleInfo(self, target, "role")
        logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

"""COMPLETE LATER"""
class Thief(Player):
    def __init__(self, name):
        super(Thief, self).__init__(name, "Thief")
        self.team = "Light"

"""COMPLETE LATER"""
class Warlock(Player):
    def __init__(self, name):
        super(Warlock, self).__init__(name, "Warlock")
        self.team = "Light"

class WitchHunter(Player):
    def __init__(self, name):
        super(WitchHunter, self).__init__(name, "Witch Hunter")
        self.team = "Light"
        self.nightActionRank = 9.0
        self.purpose = "inspect"

    def nightTurn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target=cmdinterface.targetSelector(targetsList, msg)
        cmdinterface.givePlayerRoleInfo(self, target, "team")
        logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

class Elder(Player):
    def __init__(self, name):
        super(Elder, self).__init__(name, "Elder")
        self.team = "Light"
        self.health += 1

class Fool(Player):
    def __init__(self, name):
        super(Fool, self).__init__(name, "Fool")
        self.team = "Light"

class Hunter(Player):
    def __init__(self, name):
        super(Hunter, self).__init__(name, "Hunter")
        self.team = "Light"

class Lord(Player):
    def __init__(self, name):
        super(Lord, self).__init__(name, "Lord")
        self.team = "Light"

class Silversmith(Player):
    def __init__(self, name):
        super(Silversmith, self).__init__(name, "Silversmith")
        self.team = "Light"

class Villager(Player):
    def __init__(self, name):
        super(Villager, self).__init__(name, "Villager")
        self.team = "Light"

class WhiteWitch(Player):
    def __init__(self, name):
        super(WhiteWitch, self).__init__(name, "White Witch")
        self.team = "Light"
        self.purpose = "save"
        self.nightActionRank = 6.0

    def nightTurn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if i.health > 0 and i.numID != self.numID:
                targetsList.append(i)
    #Should they be able to choose no one?
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.targetSelector(targetsList, msg)
        target.attacked = 0
        target.suicided = 0
        if target.attacked == 1 or target.suicided == 1:
            logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+") and saved them from bleeding out."
        else: logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+") but they were fine."
        return logLine

rolesDict = {"Alpha Wolf": AlphaWolf, "Beta Wolf": BetaWolf, "Serial Killer": SerialKiller, "Silver Wolf": SilverWolf,
    "Stalker Wolf": StalkerWolf, "Succubus": Succubus, "Cupid": Cupid, "Fletcher": Fletcher, "Guardian": Guardian,
    "Insomniac": Insomniac, "Seer": Seer, "Thief": Thief, "Warlock": Warlock, "Witch Hunter": WitchHunter, "Elder": Elder,
    "Fool": Fool, "Hunter": Hunter, "Lord": Lord, "Silversmith": Silversmith, "Villager": Villager, "White Witch": WhiteWitch}
"""
0 Alpha Wolf
1 Beta Wolf
2 Cupid
3 Elder
4 Fletcher
5 Fool
6 Guardian
7 Hunter
8 Insomniac
9 Lord
10 Seer
11 Serial Killer
12 Silver Wolf
13 Silversmith
14 Stalker Wolf
15 Succubus
16 Thief
17 Villager
18 Warlock
19 White Witch
20 Witch Hunter
"""

class Arrow:
    arrowCount = 0
    def __init__(self, owner, donor):
        self.owner = owner
        self.name = "arrow"
        self.arrowID = Arrow.arrowCount
        self.purpose = "shoot"
        Arrow.arrowCount += 1

    def findTargets(self, playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if i.health > 0 and i.numID != self.owner.numID:
                targetsList.append(i)
        return targetsList

    def useEquipment(self,playerObjectList):
        targetsList = self.findTargets(playerObjectList)
        msg="Who did "+self.owner.roleHR+" ("+self.owner.name+") "+self.purpose+"?"
        target = cmdinterface.targetSelector(targetsList, msg)
        target.health -= 1
        if target.health == 0:
            target.deathAction(playerObjectList)