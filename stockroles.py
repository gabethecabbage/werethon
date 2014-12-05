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
        self.attackInfo = {'attackerName': None, 'attackerRole': None, 'attackCause': None}
        self.deathInfo = {'attackerName': None, 'attackerRole': None, 'attackCause': None}
        self.suicided = 0
        self.blocked = 0
        self.guarded = 0
        self.nightActionRank = 100.0

        Player.idCounter += 1

    def night_turn(self,playerObjectList):
        pass
        logLine = "The "+self.roleHR+" ("+self.name+") has no night action."
        return logLine

    def death_action(self, playerObjectList, cause):
        self.deathInfo = self.attackInfo
        pass

    def lynch_action(self, playerObjectList):
        pass

    def display_count(self):
        print("Total Players %d" %Player.playerCount)

    def win_lose_logic(self, playerObjectList):
        pass



"""ROLE CLASSES"""
class Werewolf(Player):
    """
    This role performs attacks at night, they are the first to act and must attack as a gestalt
    """
    attacksRemaining=0
    def __init__(self, name, roleHR):
        super(Werewolf, self).__init__(name, roleHR)
        self.team = "Dark"
        self.werewolf = True
        self.nightActionRank = 2.0
        self.purpose = "maul"

    def night_turn(self,playerObjectList):
        logLine = wolf_team_turn(playerObjectList)
        return logLine

    def win_lose_logic(self,playerObjectList):
        winMeta = None
        livePlayers = [i for i in playerObjectList if not i.health == 0]
        if len(find_live_werewolves(playerObjectList)) == len(livePlayers):
            winMeta = "The Wolf Team has won by killing all other players! Congratulations, "+self.name+"!"
        return winMeta





class AlphaWolf(Werewolf):
    def __init__(self, name):
        super(AlphaWolf, self).__init__(name, "Alpha Werewolf")
        self.packRank = 1.0

class BetaWolf(Werewolf):
    def __init__(self, name):
        super(BetaWolf, self).__init__(name, "Beta Werewolf")
        self.packRank = 2.0

class SilverWolf(Werewolf):
    def __init__(self, name):
        super(SilverWolf, self).__init__(name, "Silver Wolf")
        self.packRank = 10.0

class StalkerWolf(Werewolf):
    def __init__(self, name):
        super(StalkerWolf, self).__init__(name, "Stalker Wolf")
        self.nightActionRank = 4.0
        self.purpose = "inspect"
        self.packRank = 9.0

    def night_turn(self,playerObjectList):
        logLine = wolf_team_turn(playerObjectList)
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targetsList.append(i)

        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target=cmdinterface.target_selector(targetsList, msg)
        cmdinterface.give_player_role_info(self, target, "role")
        logLine = logLine+"The "+self.roleHR+" ("+self.name+") then chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

class Succubus(Werewolf):
    def __init__(self, name):
        super(Succubus, self).__init__(name, "Succubus")
        self.nightActionRank = 3.0
        self.purpose = "block"
        self.packRank = 1.0

    def night_turn(self,playerObjectList):
        logLine = wolf_team_turn(playerObjectList)
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targetsList.append(i)

        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg)
        target.blocked=1
        logLine = logLine+"The "+self.roleHR+" ("+self.name+") then chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

"""Additional wolf class functions"""
def find_live_werewolves(playerObjectList):
    liveWolfPlayers=[]
    for player in playerObjectList:
        if not player.health < 1 and hasattr(player, "werewolf"):
            liveWolfPlayers.append(player)
    liveWolfPlayers = sorted(liveWolfPlayers, key=lambda wolf: wolf.packRank)
    return liveWolfPlayers


def wolf_team_turn(playerObjectList):
    logLine = ""
    if Werewolf.attacksRemaining > 0:
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targetsList.append(i)

        liveWolfPlayers=find_live_werewolves(playerObjectList)
        namesString=",".join([n.name for n in liveWolfPlayers])
        msg="Ask the Werewolf team ("+namesString+") who they would like to maul."
        target= cmdinterface.target_selector(targetsList, msg, allowBlank=True)

        if target == "Nobody":
            logLine = "The Werewolf team ("+namesString+") chose to maul no one. Very sneaky, eh? "
        elif target.guarded == 1:
            logLine = "The Werewolf team ("+namesString+") tried to maul "+target.roleHR+" ("+target.name+"), but they were protected tonight. "
        else:
            target.attacked = 1
            target.attackInfo = {'attackerName': liveWolfPlayers[-1].name, 'attackerRole': liveWolfPlayers[-1].roleHR, 'attackCause': liveWolfPlayers[-1].purpose}
            logLine = "The Werewolf team ("+namesString+") chose to maul "+target.roleHR+" ("+target.name+"). "
            logLine = logLine + "The attacker was " + liveWolfPlayers[-1].name

        Werewolf.attacksRemaining -= 1
    return logLine


class SerialKiller(Player):
    def __init__(self, name):
        super(SerialKiller, self).__init__(name, "Serial Killer")
        self.team = "Dark"
        self.nightActionRank = 5.0
        self.purpose = "stab"

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg)
        target.attacked = 1
        target.attackInfo = {'attackerName': self.name, 'attackerRole': self.roleHR, 'attackCause': self.purpose}
        logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

    def win_lose_logic(self, playerObjectList):
        winMeta = None
        livePlayers = [i for i in playerObjectList if not i.health == 0]
        if self.health == 1 and len(livePlayers) == 1:
            winMeta = "The "+self.roleHR+" has won by killing all other players! Congratulations, "+self.name+"!"
        return winMeta

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

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg, allowBlank=True)
        if target == "Nobody":
            logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" nobody, how dull..."
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

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if i.health > 0 and i.numID != self.lastPlayerGuarded:
                targetsList.append(i)
    #Should they be able to choose no one?
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg)
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

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg)
        cmdinterface.give_player_role_info(self, target, "role")
        logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

"""COMPLETE LATER"""
class Thief(Player):
    def __init__(self, name):
        super(Thief, self).__init__(name, "Thief")
        self.team = "Light"
        self.purpose = "steal the role of"

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg, allowBlank=True)

        if target == "Nobody":
            logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" nobody, how dull..."

        elif target.team == "Dark" or target.role == "Silversmith":
            self.attacked = 1
            logLine = "The "+self.roleHR+" ("+self.name+") was killed trying to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."


        return logLine

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

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if not i.health < 1 and i.numID != self.numID:
                targetsList.append(i)
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target=cmdinterface.target_selector(targetsList, msg)
        cmdinterface.give_player_role_info(self, target, "team")
        logLine = "The "+self.roleHR+" ("+self.name+") chose to "+self.purpose+" the "+target.roleHR+" ("+target.name+")."
        return logLine

class Elder(Player):
    def __init__(self, name):
        super(Elder, self).__init__(name, "Elder")
        self.team = "Light"
        self.health += 1

    def death_action(self, playerObjectList, cause):
        if cause == "Lynched":
            for i in playerObjectList:
                if i.team != "Dark":
                    i.blocked = 1

class Fool(Player):
    def __init__(self, name):
        super(Fool, self).__init__(name, "Fool")
        self.team = "Light"

    def win_lose_logic(self, playerObjectList):
        winMeta = None
        if self.deathInfo['attackCause'] == "lynch":
            winMeta = "The "+self.roleHR+" has won by convincing the village to Lynch him! Congratulations, "+self.name+"!"
        return winMeta


class Hunter(Player):
    def __init__(self, name):
        super(Hunter, self).__init__(name, "Hunter")
        self.team = "Light"

    def death_action(self, playerObjectList, cause):
        """On death, hunter gives self arrow and uses it"""
        self.atWillDayEquip.append(Arrow(self,self))
        self.atWillDayEquip.arrow.useEquipment(playerObjectList)
        self.atWillDayEquip.remove(Arrow)

class Lord(Player):
    def __init__(self, name):
        super(Lord, self).__init__(name, "Lord")
        self.team = "Light"
        self.veto = 1

    def lynch_action(self, playerObjectList):
       msg="Did the "+self.roleHR+" ("+self.name+") use there lynching veto this round?"
       if self.veto == 1:
            if cmdinterface.boolean_selector((yes,no), msg) == yes:
                self.veto == 0


"""COMPLETE LATER"""
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

    def night_turn(self,playerObjectList):
        targetsList=[]
        for i in playerObjectList:
            if i.health > 0 and i.numID != self.numID:
                targetsList.append(i)
    #Should they be able to choose no one?
        msg="Ask the "+self.roleHR+" ("+self.name+") who they would like to "+self.purpose+"."
        target= cmdinterface.target_selector(targetsList, msg)
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

"""Equipment Classes"""
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

    def useEquipment(self, playerObjectList):
        targetsList = self.findTargets(playerObjectList)
        msg="Who did the "+self.owner.roleHR+" ("+self.owner.name+") "+self.purpose+"?"
        target = cmdinterface.target_selector(targetsList, msg)
        target.health -= 1
        if target.health == 0:
            target.death_action(playerObjectList, self.name)
            target.deathInfo = {'attackerName': self.owner.name, 'attackerRole': self.owner.roleHR, 'attackCause': self.purpose}
