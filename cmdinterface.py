__author__ = "gabe"

import stockroles

"""DROPPED
def role_picker(player_count):
    all_role_names = list(stockroles.roles_lookup.keys())
    all_role_names = sorted(all_role_names)
    roleList = []
    while len(roleList) != player_count:
        for i in range(len(all_role_names)):
            print(i, all_role_names[i])
        roleList = input("Enter the roles required:").split()
        if len(roleList) != player_count:
            print("You have not selected enough roles for your player count")

    for i in range(len(roleList)):
        roleList[i] = int(roleList[i])

    return roleList, all_role_names


def player_name_entry(player_count):
    player_names = []
    while len(player_names) != player_count:
        player_names = input("Enter the players nickname:").split()
        if player_count != len(player_names):
            print("Your player count does not match the number of nick names")

    return player_names
"""


def target_selector(targets_list, msg=":::::::::"):
    print(msg)
    for i in range(len(targets_list)):
        print(str(i) + ": " + targets_list[i].name)
    t = int(input("Select the corresponding number: "))
    return targets_list[t]


def boolean_selector(boolList, msg=":::::::::"):
    """Asks for the user to pick one of two values e.g. true/false, yes/no"""
    i = 0
    while i != 1:
        print(msg)
        ans = input("(" + boolList[0] + " or " + boolList[1] + "?) :")
        if ans != boolList[0] or ans != boolList[1]:
            print("That's not an option you tit!")
        else:
            i = 1

    return ans


def give_player_role_info(player, target, infoType):
    if infoType == "role":
        msg = (
            f"You may show the {player.role_hr} ({player.name}) that"
            f" {target.name} is a {target.role_hr}"
        )

    if infoType == "team":
        msg = (
            f"You may show the {player.role_hr} ({player.name}) that"
            f" {target.name} is a {target.team} team member"
        )
    print(msg)
    return msg


def player_inaction_message(player, cause):
    msg = f"{player.role_hr} ({player.name}) may not act, they are {cause}"
    print(msg)
    return msg


def night_death_message(listOfDead, reveal):
    if len(listOfDead) > 0:
        print("The following players died in the night:")
        for i in listOfDead:
            if reveal:
                print(i.name + " the " + i.role_hr)
            else:
                print(i.name)
    else:
        print("There were no deaths this night")
