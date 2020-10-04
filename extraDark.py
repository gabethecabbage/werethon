__author__ = "gabe"
import cmdinterface
from stockroles import Player
from stockroles import roles_lookup


class SerialKiller(Player):
    def __init__(self, name):
        super(SerialKiller, self).__init__(name, "Serial Killer")
        self.team = "Dark"
        self.night_action_rank = 5.0
        self.purpose = "stab"

    def night_turn(self, players):
        targets_list = []
        for i in players:
            if not i.health < 1 and i.num_id != self.num_id:
                targets_list.append(i)

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f"{self.purpose}."
        )
        target = cmdinterface.target_selector(targets_list, msg)
        target.attacked = 1
        target.attack_info = {
            "attacker_name": self.name,
            "attacker_role": self.role_hr,
            "attack_cause": self.purpose,
        }
        log_line = (
            f"The {self.role_hr} ({self.name}) choose to"
            f"{self.purpose} the {target.role_hr} ({target.name})."
        )
        return log_line

    def win_lose_logic(self, players):
        win_meta = None
        livePlayers = [i for i in players if not i.health == 0]
        if self.health == 1 and len(livePlayers) == 1:
            win_meta = (
                f"The {self.role_hr} has won by killing all players!"
                f"Congratulations, {self.name}!"
            )

        return win_meta


extra_roles_lookup = {"Serial Killer": SerialKiller}

roles_lookup = {roles_lookup, extra_roles_lookup}
