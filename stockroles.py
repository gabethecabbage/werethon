__author__ = "gabe"
import cmdinterface


class Player(object):
    id_counter = 0
    """Common base class for all players"""

    def __init__(self, name, role):
        self.name = name
        self.role_hr = role
        self.num_id = Player.id_counter
        self.health = 1
        self.at_will_day_equip = []
        self.attacked = 0
        self.attack_info = {
            "attacker_name": None,
            "attacker_role": None,
            "attack_cause": None,
        }
        self.death_info = {
            "attacker_name": None,
            "attacker_role": None,
            "attack_cause": None,
        }
        self.suicided = 0
        self.blocked = 0
        self.guarded = 0
        self.night_action_rank = 100.0

        Player.id_counter += 1

    def night_turn(self, players):
        pass
        log_line = f"The {self.role_hr} ({self.name}) has no night action."
        return log_line

    def death_action(self, players, cause):
        self.death_info = self.attack_info
        pass

    def hang_action(self, players):
        pass

    def display_count(self):
        print("Total Players %d" % Player.player_count)

    def win_lose_logic(self, players):
        pass


class Werewolf(Player):
    """
    This role performs attacks at night, they are the first to act
    and attack as a gestalt
    """

    attacksRemaining = 0

    def __init__(self, name, role_hr):
        super(Werewolf, self).__init__(name, role_hr)
        self.team = "Dark"
        self.werewolf = True
        self.night_action_rank = 2.0
        self.purpose = "maul"

    def night_turn(self, players):
        log_line = wolf_team_turn(players)
        return log_line

    def win_lose_logic(self, players):
        win_meta = None
        livePlayers = [i for i in players if not i.health == 0]
        if len(find_live_werewolves(players)) == len(livePlayers):
            win_meta = (
                f"The Wolf Team has won by killing all other players!"
                f"Congratulations, {self.name}!"
            )
        return win_meta


class AlphaWolf(Werewolf):
    def __init__(self, name):
        super(AlphaWolf, self).__init__(name, "Alpha Werewolf")
        self.pack_rank = 1.0


class BetaWolf(Werewolf):
    def __init__(self, name):
        super(BetaWolf, self).__init__(name, "Beta Werewolf")
        self.pack_rank = 2.0


# Wolf Class helper functions
def find_live_werewolves(players):
    live_wolf_players = []
    for player in players:
        if not player.health < 1 and hasattr(player, "werewolf"):
            live_wolf_players.append(player)
    live_wolf_players = sorted(live_wolf_players, key=lambda wolf: wolf.pack_rank)
    return live_wolf_players


def wolf_team_turn(players):
    log_line = ""
    if Werewolf.attacksRemaining > 0:
        targets_list = []
        for i in players:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targets_list.append(i)

        live_wolf_players = find_live_werewolves(players)
        names_string = ",".join([n.name for n in live_wolf_players])
        msg = f"Ask Werewolf team ({names_string}) who they want to maul."
        target = cmdinterface.target_selector(targets_list, msg, allow_blank=True)

        if target == "Nobody":
            log_line = f"The Werewolf team ({names_string}) chose not to maul."
        elif target.guarded == 1:
            log_line = (
                f"The Werewolf team ({names_string}) tried to maul"
                f" {target.role_hr} ({target.name}),"
                " but they were protected tonight."
            )
        else:
            target.attacked = 1
            target.attack_info = {
                "attacker_name": live_wolf_players[-1].name,
                "attacker_role": live_wolf_players[-1].role_hr,
                "attack_cause": live_wolf_players[-1].purpose,
            }
            log_line = (
                f"The Werewolf team ({names_string}) choose to maul"
                f"{target.role_hr} ({target.name}). \n"
                f"The attacker was {live_wolf_players[-1].name}."
            )

        Werewolf.attacksRemaining -= 1
    return log_line


class Fletcher(Player):
    def __init__(self, name):
        super(Fletcher, self).__init__(name, "Fletcher")
        self.team = "Light"
        self.night_action_rank = 10.0
        self.purpose = "bestow an arrow upon"

    def night_turn(self, players):
        targets_list = []
        for i in players:
            if not i.health < 1 and i.num_id != self.num_id:
                targets_list.append(i)

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )
        target = cmdinterface.target_selector(targets_list, msg, allow_blank=True)

        if target == "Nobody":
            log_line = (
                f"The {self.role_hr} ({self.name}) chose to"
                f"{self.purpose} nobody, how dull..."
            )
        else:
            target.at_will_day_equip.append(Arrow(target, self))
            log_line = (
                f"The {self.role_hr} ({self.name}) chose to"
                f"{self.purpose} the {target.role_hr} ({target.name})."
            )
        return log_line


class WitchHunter(Player):
    def __init__(self, name):
        super(WitchHunter, self).__init__(name, "Witch Hunter")
        self.team = "Light"
        self.night_action_rank = 9.0
        self.purpose = "inspect"

    def night_turn(self, players):
        targets_list = []
        for i in players:
            if not i.health < 1 and i.num_id != self.num_id:
                targets_list.append(i)

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )

        target = cmdinterface.target_selector(targets_list, msg)
        cmdinterface.give_player_role_info(self, target, "team")

        log_line = (
            f"The {self.role_hr} ({self.name}) chose to {self.purpose}"
            f" the {target.role_hr} ({target.name})."
        )
        return log_line


class Fool(Player):
    def __init__(self, name):
        super(Fool, self).__init__(name, "Fool")
        self.team = "Light"

    def win_lose_logic(self, players):
        win_meta = None
        if self.death_info["attack_cause"] == "hang":
            win_meta = (
                f"The {self.role_hr} has won by convincing the village"
                f" to Lynch him! Congratulations, {self.name}!"
            )
        return win_meta


class Hunter(Player):
    def __init__(self, name):
        super(Hunter, self).__init__(name, "Hunter")
        self.team = "Light"

    def death_action(self, players, cause):
        """On death, hunter gives self arrow and uses it"""
        self.at_will_day_equip.append(Arrow(self, self))
        self.at_will_day_equip.arrow.useEquipment(players)
        self.at_will_day_equip.remove(Arrow)


class Villager(Player):
    def __init__(self, name):
        super(Villager, self).__init__(name, "Villager")
        self.team = "Light"


class WhiteWitch(Player):
    def __init__(self, name):
        super(WhiteWitch, self).__init__(name, "White Witch")
        self.team = "Light"
        self.purpose = "save"
        self.night_action_rank = 6.0

    def night_turn(self, players):
        targets_list = []
        for i in players:
            if i.health > 0 and i.num_id != self.num_id:
                targets_list.append(i)

        """Note: Should they be able to choose no one?"""
        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )

        target = cmdinterface.target_selector(targets_list, msg)
        target.attacked = 0
        target.suicided = 0
        if target.attacked == 1 or target.suicided == 1:
            log_line = (
                f"The {self.role_hr} ({self.name}) chose to"
                f" {self.purpose} the {target.role_hr} ({target.name})"
                "and saved them from bleeding out."
            )
        else:
            log_line = (
                f"The {self.role_hr} ({self.name}) chose to"
                f" {self.purpose} the {target.role_hr} ({target.name})"
                " but they were fine."
            )

        return log_line


roles_lookup = {
    "Alpha Wolf": AlphaWolf,
    "Beta Wolf": BetaWolf,
    "Fletcher": Fletcher,
    "Witch Hunter": WitchHunter,
    "Fool": Fool,
    "Hunter": Hunter,
    "Villager": Villager,
    "White Witch": WhiteWitch,
}


"""Equipment Classes"""


class Arrow:
    arrowCount = 0

    def __init__(self, owner, donor):
        self.owner = owner
        self.name = "arrow"
        self.arrowID = Arrow.arrowCount
        self.purpose = "shoot"
        Arrow.arrowCount += 1

    def findTargets(self, players):
        targets_list = []
        for i in players:
            if i.health > 0 and i.num_id != self.owner.num_id:
                targets_list.append(i)
        return targets_list

    def useEquipment(self, players):
        targets_list = self.findTargets(players)
        msg = (
            f"Who did the {self.owner.role_hr} ({self.owner.name})" f" {self.purpose}?"
        )

        target = cmdinterface.target_selector(targets_list, msg)
        target.health -= 1
        if target.health == 0:
            target.death_action(players, self.name)
            target.death_info = {
                "attacker_name": self.owner.name,
                "attacker_role": self.owner.role_hr,
                "attack_cause": self.purpose,
            }
