__author__ = "gabe"
import cmdinterface
from stockroles import Werewolf
from stockroles import wolf_team_turn
from stockroles import roles_lookup


class SilverWolf(Werewolf):
    def __init__(self, name):
        super(SilverWolf, self).__init__(name, "Silver Wolf")
        self.pack_rank = 10.0


class StalkerWolf(Werewolf):
    def __init__(self, name):
        super(StalkerWolf, self).__init__(name, "Stalker Wolf")
        self.night_action_rank = 4.0
        self.purpose = "inspect"
        self.pack_rank = 9.0

    def night_turn(self, players):
        log_line = wolf_team_turn(players)
        targets_list = []
        for i in players:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targets_list.append(i)

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )
        target = cmdinterface.target_selector(targets_list, msg)
        cmdinterface.give_player_role_info(self, target, "role")

        log_msg = (
            f"The {self.role_hr} ({self.name}) then choose to"
            f" {self.purpose} the {target.role_hr} ({target.name})."
        )
        log_line = log_line + log_msg
        return log_line


class Vukodlak(Werewolf):
    def __init__(self, name):
        super(Vukodlak, self).__init__(name, "Vukodlak")
        self.night_action_rank = 3.0
        self.purpose = "block"
        self.pack_rank = 1.0

    def night_turn(self, players):
        log_line = wolf_team_turn(players)
        targets_list = []
        for i in players:
            if not i.health < 1 and not hasattr(i, "werewolf"):
                targets_list.append(i)

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )
        target = cmdinterface.target_selector(targets_list, msg)
        target.blocked = 1

        log_msg = (
            f"The {self.role_hr} ({self.name}) then choose to"
            f" {self.purpose} the {target.role_hr} ({target.name})."
        )
        log_line = log_line + log_msg
        return log_line


extra_roles_lookup = {
    "Silver Wolf": SilverWolf,
    "Stalker Wolf": StalkerWolf,
    "Vukodlak": Vukodlak,
}

roles_lookup = {roles_lookup, extra_roles_lookup}
