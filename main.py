#! /usr/bin/python
__author__ = "gabe"

import random
import stockroles
import time
import cmdinterface
import logging


class Game(object):
    def __init__(self, player_names, role_names, reveal):
        log_file_name = f"log/log-{int(time.time())}.txt"
        logging.basicConfig(filename=log_file_name, level=logging.INFO)
        self.reveal = reveal
        self.player_names = player_names
        self.role_names = random.shuffle(role_names)
        self.day_counter = 0

        self.players = []
        for role, name in zip(role_names, player_names):
            self.players.append(stockroles.roles_lookup[role](self, name))
        """Sort players by their night rank attribute"""
        self.players.sort(key=lambda x: x.night_action_rank)

        for obj in self.players:
            cmdinterface.simple_player_info(obj)
        end_state = self.day_night_cycle(reveal)
        for obj in self.players:
            cmdinterface.simple_player_info(obj)
        print(end_state)
        print("End of script")

    def live_players(
        self, filter_in={}, filter_out={}, sort_var="night_action_rank"
    ):
        """Return filtered and sorted list of live players"""
        live_filtered = [p for p in self.players if p.health > 0]

        for key, value in filter_in.items():
            live_filtered = [
                p for p in live_filtered if getattr(p, key, False) == value
            ]

        for key, value in filter_out.items():
            live_filtered = [
                p for p in live_filtered if getattr(p, key, False) != value
            ]
        live_filtered = sorted(live_filtered, key=lambda p: getattr(p, sort_var))
        return live_filtered

    def night_phase(self, reveal):
        """Cycle through the night turns"""
        logging.info(f"Night {self.day_counter + 1} has started")

        """Reset any night only attributes"""
        for p in self.live_players():
            p.blocked = 0
            p.attacked = 0
            p.guarded = 0
            p.attack_info = None

        """Set the highest ranking wolf to alpha if none found"""
        if len(self.live_players({"alpha_wolf": True})) < 1:
            live_wolf_players = self.live_players(
                {"werewolf": True}, {}, "pack_rank"
            )
            live_wolf_players[0].alpha_wolf = True

        """for each player, run there night turn"""
        for p in self.live_players():
            """checks the player can use their night turn"""
            if p.blocked == 1:
                logging.info(cmdinterface.player_inaction_message(p, "blocked"))
            else:
                p.night_turn()

        """Check for Deaths"""
        died_in_the_night = []
        for p in self.live_players():
            if p.attacked >= 1 and p.guarded == 0:
                p.health -= 1
                """dock 1 hp per unguarded attack"""
                if p.health < 1:
                    p.death_action()
                    p.death_info = p.attack_info
                    died_in_the_night.append(p)
        """returns a list of the dead and bool of the reveal rule"""
        cmdinterface.night_death_message(died_in_the_night, reveal)

    def day_phase(self, reveal):
        died_in_the_day = []
        equip_user = None

        logging.info(f"Day {self.day_counter + 1} started")

        while equip_user != "Nobody":
            equip_user = cmdinterface.pick_day_equip_user(self.live_players())
            if equip_user != "Nobody":
                cmdinterface.use_day_equip(self.live_players(), equip_user)

        self.day_counter += 1


    def hanging(self):
        hang_msg = "Select the player the group voted to hang."
        hang_victim = cmdinterface.target_selector(self.live_players(), hang_msg, True)
        if hang_victim != "Nobody":
            hang_victim.health -= 1
            hang_victim.attack_info = {
                "attacker_name": "Town",
                "attacker_role": "Town",
                "attack_cause": "hang",
            }
            if hang_victim.health < 1:
                hang_victim.death_action()

    def win_lose_check(self):

        for p in self.players:
            end_state = p.win_lose_logic()
            if end_state is not None:
                logging.info(end_state)
                return end_state
        return None

    def day_night_cycle(self, reveal):
        while True:
            self.night_phase(reveal)
            end_state = self.win_lose_check()
            if end_state is not None:
                break

            self.day_phase(reveal)
            end_state = self.win_lose_check()
            if end_state is not None:
                break

            self.hanging()
            end_state = self.win_lose_check()
            if end_state is not None:
                break

        return end_state


test_player_names = ["Gabe", "Dowd", "Tom", "Becca", "Onslow", "Andy"]
test_role_names = [
    "Werewolf",
    "Werewolf",
    "Hunter",
    "Witch Hunter",
    "Fletcher",
    "Villager",
]


def main():
    Game(test_player_names, test_role_names, True)


if __name__ == "__main__":
    # execute only if run as a script
    main()
