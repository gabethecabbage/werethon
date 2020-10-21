__author__ = "gabe"
import cmdinterface


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

    def death_action(self, cause):
        self.death_info = self.attack_info
        pass

    def hang_action(self):
        pass

    def display_count(self):
        print("Total Players %d" % Player.player_count)

    def win_lose_logic(self):
        pass


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
                f"The Wolf Team has won by killing all other players!"
                f" Congratulations, {self.name}!"
            )
        return end_state

    def night_turn(self):
        log_line = ""
        if self.alpha_wolf:
            targets_list = self.game.live_players({"werewolf": False})
            live_wolf_players = self.game.live_players({"werewolf": True})
            wolf_names = ",".join([n.name for n in live_wolf_players])
            msg = f"Ask Werewolf team ({wolf_names}) who they want to maul."
            target = cmdinterface.target_selector(targets_list, msg, allow_blank=True)

            if target == "Nobody":
                log_line = f"The Werewolf team ({wolf_names}) chose not to maul."
            elif target.guarded == 1:
                log_line = (
                    f"The Werewolf team ({wolf_names}) tried to maul"
                    f" {target.role_hr} ({target.name}),"
                    " but they were protected tonight."
                )
            else:
                target.attacked = 1
                target.attack_info = {
                    "attacker_name": self.name,
                    "attacker_role": self.role_hr,
                    "attack_cause": self.purpose,
                }
                log_line = (
                    f"The Werewolf team ({wolf_names}) choose to maul"
                    f"{target.role_hr} ({target.name}). \n"
                    f"The attacker was {self.name}."
                )
        return log_line


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

        log_line = (
            f"The {self.role_hr} ({self.name}) chose to {self.purpose}"
            f" the {target.role_hr} ({target.name})."
        )
        return log_line


class Fool(Player):
    def __init__(self, game, name):
        super(Fool, self).__init__(game, name, "Fool")
        self.team = "Light"

    def win_lose_logic(self):
        end_state = None
        if self.death_info["attack_cause"] == "hang":
            end_state = (
                f"The {self.role_hr} has won by convincing the village"
                f" to Lynch him! Congratulations, {self.name}!"
            )
        return end_state


class Hunter(Player):
    def __init__(self, game, name):
        super(Hunter, self).__init__(game, name, "Hunter")
        self.team = "Light"

    def death_action(self, cause):
        """On death, hunter gives self arrow and uses it"""
        self.at_will_day_equip.append(Arrow(self, self))
        hunter_arrow = self.at_will_day_equip[-1]
        hunter_arrow.use_equipment()
        self.at_will_day_equip.remove(hunter_arrow)


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
            log_line = (
                f"The {self.role_hr} ({self.name}) chose to"
                f" {self.purpose} the {target.role_hr} ({target.name})"
                " and saved them from bleeding out."
            )
        else:
            log_line = (
                f"The {self.role_hr} ({self.name}) chose to"
                f" {self.purpose} the {target.role_hr} ({target.name})"
                " but they were fine."
            )

        return log_line


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
        if target.health == 0:
            target.death_action(self.name)
            target.death_info = {
                "attacker_name": self.owner.name,
                "attacker_role": self.owner.role_hr,
                "attack_cause": self.purpose,
            }
