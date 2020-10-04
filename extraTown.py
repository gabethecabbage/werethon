__author__ = "gabe"
import cmdinterface
from stockroles import Player
from stockroles import roles_lookup


class Guardian(Player):
    def __init__(self, name):
        super(Guardian, self).__init__(name, "Guardian")
        self.team = "Light"
        self.night_action_rank = 1.0
        self.purpose = "protect"
        self.lastPlayerGuarded = None

    def night_turn(self, players):
        targets_list = []
        for i in players:
            if i.health > 0 and i.num_id != self.lastPlayerGuarded:
                targets_list.append(i)

        """Note: Should they be able to choose no one?"""
        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )
        target = cmdinterface.target_selector(targets_list, msg)
        target.guarded = 1
        self.lastPlayerGuarded = target.num_id


class Seer(Player):
    def __init__(self, name):
        super(Seer, self).__init__(name, "Seer")
        self.team = "Light"
        self.night_action_rank = 7.0
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
        cmdinterface.give_player_role_info(self, target, "role")
        log_line = (
            f"The {self.role_hr} ({self.name}) chose to {self.purpose}"
            f" the {target.role_hr} ({target.name})."
        )
        return log_line


class Elder(Player):
    def __init__(self, name):
        super(Elder, self).__init__(name, "Elder")
        self.team = "Light"
        self.health += 1

    def death_action(self, players, cause):
        if cause == "Hanged":
            for i in players:
                if i.team != "Dark":
                    i.blocked = 1


class Lord(Player):
    def __init__(self, name):
        super(Lord, self).__init__(name, "Lord")
        self.team = "Light"
        self.veto = 1

    def hang_action(self, players):
        msg = f"Did the {self.role_hr} ({self.name}) use there hanging veto?"
        if self.veto == 1:
            if cmdinterface.boolean_selector(("yes", "no"), msg) == "yes":
                self.veto == 0


extra_roles_lookup = {"Guardian": Guardian, "Seer": Seer, "Elder": Elder, "Lord": Lord}

roles_lookup = {roles_lookup, extra_roles_lookup}


"""COMPLETE LATER
class Cupid(Player):
    def __init__(self, name):
        super(Cupid, self).__init__(name, "Cupid")
        self.team = "Light"


class Insomniac(stockroles.Player):
    def __init__(self, name):
        super(Insomniac, self).__init__(name, "Insomniac")
        self.team = "Light"


class Thief(Player):
    def __init__(self, name):
        super(Thief, self).__init__(name, "Thief")
        self.team = "Light"
        self.purpose = "steal the role of"

    def night_turn(self, players):
        targets_list = []
        for i in players:
            if not i.health < 1 and i.num_id != self.num_id:
                targets_list.append(i)

        msg = f'Ask the {self.role_hr} ({self.name}) who they would like to'\
              f' {self.purpose}.'

        target = cmdinterface.target_selector(targets_list,
                                              msg,
                                              allow_blank=True)

        if target == "Nobody":
            log_line = f'The {self.role_hr} ({self.name}) chose to'\
                       f' {self.purpose} nobody, how dull...'

        elif target.team == "Dark" or target.role == "Silversmith":
            self.attacked = 1
            log_line = f'The {self.role_hr} ({self.name}) died trying to'\
                       f' {self.purpose} the {target.role_hr} ({target.name}).'

        return log_line


class Warlock(Player):
    def __init__(self, name):
        super(Warlock, self).__init__(name, "Warlock")
        self.team = "Light"


class Silversmith(Player):
    def __init__(self, name):
        super(Silversmith, self).__init__(name, "Silversmith")
        self.team = "Light"
"""
