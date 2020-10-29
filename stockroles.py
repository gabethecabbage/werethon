__author__ = "gabe"
import cmdinterface
import logging


class Player(object):
    id_counter = 0
    """Common base class for all players"""

    def __init__(self, game, name, role):
        self.game = game
        self.name = name
        self.role_hr = role
        self.id = Player.id_counter
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

    def night_turn(self):
        log_line = f"The {self.role_hr} ({self.name}) has no night action."
        return log_line

    def death_action(self):
        self.death_info = self.attack_info
        print(self.death_info)
        logging.info(
            f"{self.role_hr} ({self.name}) was killed by "
            f"{self.death_info['attacker_role']} ({self.death_info['attacker_name']})"
        )

    def hang_action(self):
        pass

    def display_count(self):
        print("Total Players %d" % Player.player_count)

    def win_lose_logic(self):
        end_state = None
        if self.team == "Light" and len(self.game.live_players({"team": "Dark"})) == 0:
            end_state = "The Light team won by killing all the Dark forces!"
        return end_state


class Werewolf(Player):
    """
    This role performs attacks at night, they are the first to act
    and attack as a gestalt
    """

    def __init__(self, game, name):
        super(Werewolf, self).__init__(game, name, "Werewolf")
        self.team = "Dark"
        self.werewolf = True
        self.alpha_wolf = False
        self.pack_rank = 2.0
        self.night_action_rank = 1.0
        self.purpose = "maul"

    def win_lose_logic(self):
        end_state = None
        if self.game.live_players({"werewolf": True}) == self.game.live_players():
            end_state = (
                f"Werewolf Team has won by killing all other players!"
                f" Congratulations, {self.name}!"
            )
        return end_state

    def night_turn(self):
        if self.alpha_wolf:
            targets_list = self.game.live_players({"werewolf": False})
            live_wolf_players = self.game.live_players({"werewolf": True})
            wolf_names = ",".join([n.name for n in live_wolf_players])
            msg = f"Ask Werewolf team ({wolf_names}) who they want to maul."
            target = cmdinterface.target_selector(targets_list, msg, allow_blank=True)

            if target == "Nobody":
                logging.info(f"Werewolf team ({wolf_names}) chose to maul nobody")
            else:
                target.attacked = 1
                target.attack_info = {
                    "attacker_name": self.name,
                    "attacker_role": self.role_hr,
                    "attack_cause": self.purpose,
                }
                logging.info(
                    f"Werewolf team ({wolf_names}) maul"
                    f" the {target.role_hr} ({target.name})."
                    f" The attacker was {self.name}."
                )


class Fletcher(Player):
    def __init__(self, game, name):
        super(Fletcher, self).__init__(game, name, "Fletcher")
        self.team = "Light"
        self.night_action_rank = 10.0
        self.purpose = "bestow an arrow upon"

    def night_turn(self):
        targets_list = self.game.live_players(filter_out={"id": self.id})

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )
        target = cmdinterface.target_selector(targets_list, msg, allow_blank=True)

        if target == "Nobody":
            logging.info(f"{self.role_hr} ({self.name}) chose to {self.purpose} nobody")
        else:
            target.at_will_day_equip.append(Arrow(target, self))
            logging.info(
                f"{self.role_hr} ({self.name}) chose to {self.purpose} the"
                f" {target.role_hr} ({target.name})."
            )


class WitchHunter(Player):
    def __init__(self, game, name):
        super(WitchHunter, self).__init__(game, name, "Witch Hunter")
        self.team = "Light"
        self.night_action_rank = 9.0
        self.purpose = "inspect"

    def night_turn(self):
        targets_list = self.game.live_players(filter_out={"id": self.id})

        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )

        target = cmdinterface.target_selector(targets_list, msg)
        cmdinterface.give_player_role_info(self, target, "team")

        logging.info(
            f"The {self.role_hr} ({self.name}) chose to {self.purpose}"
            f" the {target.role_hr} ({target.name})."
        )


class Fool(Player):
    def __init__(self, game, name):
        super(Fool, self).__init__(game, name, "Fool")
        self.team = "Light"

    def win_lose_logic(self):
        end_state = None
        if self.death_info["attack_cause"] == "hang":
            end_state = (
                f"The {self.role_hr} has won by convincing the village to Lynch"
                f" him! Congratulations, {self.name}!"
            )
        return end_state


class Hunter(Player):
    def __init__(self, game, name):
        super(Hunter, self).__init__(game, name, "Hunter")
        self.team = "Light"

    def death_action(self):
        """On death, hunter gives self arrow and uses it"""
        self.death_info = self.attack_info
        self.at_will_day_equip.append(Arrow(self, self))
        hunter_arrow = self.at_will_day_equip[-1]
        hunter_arrow.use_equipment()
        self.at_will_day_equip.remove(hunter_arrow)
        logging.info(
            f"{self.role_hr} ({self.name}) was killed by "
            f"{self.death_info['attacker_role']} ({self.death_info['attacker_name']})"
        )


class Villager(Player):
    def __init__(self, game, name):
        super(Villager, self).__init__(game, name, "Villager")
        self.team = "Light"


class WhiteWitch(Player):
    def __init__(self, game, name):
        super(WhiteWitch, self).__init__(game, name, "White Witch")
        self.team = "Light"
        self.purpose = "save"
        self.night_action_rank = 6.0

    def night_turn(self):
        targets_list = self.game.live_players(filter_out={"id": self.id})

        """Note: Should they be able to choose no one?"""
        msg = (
            f"Ask the {self.role_hr} ({self.name}) who they would like to"
            f" {self.purpose}."
        )

        target = cmdinterface.target_selector(targets_list, msg)
        if target.attacked == 1 or target.suicided == 1:
            target.attacked = 0
            target.suicided = 0
            logging.info(
                f"{self.role_hr} ({self.name}) chose to"
                f" {self.purpose} the {target.role_hr} ({target.name})"
                " and saved them from bleeding out."
            )
        else:
            logging.info(
                f"{self.role_hr} ({self.name}) chose to"
                f" {self.purpose} the {target.role_hr} ({target.name})"
                " but they were fine."
            )


roles_lookup = {
    "Werewolf": Werewolf,
    "Villager": Villager,
    "Fletcher": Fletcher,
    "Hunter": Hunter,
    "White Witch": WhiteWitch,
    "Witch Hunter": WitchHunter,
    "Fool": Fool,
}


"""Equipment Classes"""


class Arrow:
    arrow_count = 0

    def __init__(self, owner, donor):
        self.game = owner.game
        self.owner = owner
        self.name = "arrow"
        self.arrowID = Arrow.arrow_count
        self.purpose = "shoot"
        Arrow.arrow_count += 1

    def use_equipment(self):
        targets_list = self.game.live_players(filter_out={"id": self.owner.id})
        msg = (
            f"Who did the {self.owner.role_hr} ({self.owner.name})" f" {self.purpose}?"
        )

        target = cmdinterface.target_selector(targets_list, msg)
        target.health -= 1
        target.attack_info = {
            "attacker_name": self.owner.name,
            "attacker_role": self.owner.role_hr,
            "attack_cause": self.purpose,
        }
        if target.health == 0:
            target.death_action()
