#!/usr/bin/env python

"""A simple Multi-User Dungeon (MUD) game. Players can talk to each
other, examine their surroundings and move between rooms.

author: Mark Frimston - mfrimston@gmail.com
"""

import time
from random import randint

# import the MUD server class
from mudserver import MudServer

#COLORS
RED = "\033[91m"
BLUE = "\033[96]"
STDC = "\033[93m"
ENDC = "\033[0m"

def highlight(term):
    return(RED + term + STDC)

docsHelp = "\n\r\033[36mHELP.DOC >>>>>>>>>>>>>>>>>>\n\r"\
    "During 1968 and 1969, a giant big number of events took place that had an impact\n\r"\
    "on the UFO field. The University of Colorado completed the government-financed\n\r"\
    "UFO study, with the study head Edward Condon presenting a very negative picture\n\r"\
    "of the worth of further UFO studies. These results enabled the U.S. Air Force to\n\r"\
    "close its administrative UFO office dubbed \"Project Blue Book.\" The press didn't\n\r"\
    "bother to look at the details of the University study and reacted only to Condon's\n\r"\
    "summary of the study by using the media to declare that the UFO mystery was solved.\033[0m\n\r"

# structure defining the rooms in the game. Try adding more rooms to the game!
rooms = {
    "Lobby": {
        "description": "Welcome to " + highlight("LOBBY") + " feel free to gab away.",
        "exits": {"ufos": "UFOS"},
        "docs": {"help": docsHelp},
    },
    "UFOS": {
        "description": "This is the " + highlight("UFO") + " chat channel. You shouldn't be here.",
        "exits": {"lobby": "Lobby"},
        "docs": {"none": "nbothing here"},
    }
}

startRoom = "Lobby"

# stores the players in the game
players = {}

#NPC SETUP

daveScript = ["Hello",
"How have you been?",
"I hate you",]


players[id] = {
    "name": "Dave",
    "room": "Lobby",
    "script": daveScript,
}



# start the server
mud = MudServer()
mudTimer = 0
interval = randint(25, 48)
progressIndex = 0
# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    mudTimer += 1

    if mudTimer%interval == 0:
        # go through every player in the game
        mud.send_message(id, highlight("Dave says: ") + daveScript[progressIndex])
        progressIndex += 1
        if progressIndex >= len(daveScript):
            progressIndex = 0
            for id in players:
                if players[id]["name"] == "dave":
                    del(players[id])
        interval = randint(45, 98)

    # go through any newly connected players
    for id in mud.get_new_players():

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. We set their room to
        # None initially until they have entered a name
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = {
            "name": None,
            "room": None,
        }

        # send the new player a prompt for their name
        mud.send_message(id, "Identify " + highlight("YOURSELF") + "?")

    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # go through all the players in the game
        for pid, pl in players.items():
            # send each player a message to tell them about the diconnected
            # player
            mud.send_message(pid, "{} quit the game".format(
                                                        players[id]["name"]))

        # remove the player's entry in the player dictionary
        del(players[id])

    # go through any new commands sent from players
    for id, command, params in mud.get_commands():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # if the player hasn't given their name yet, use this first command as
        # their name and move them to the starting room.
        if players[id]["name"] is None:

            players[id]["name"] = command
            players[id]["room"] = startRoom
            players[id]["progress"] = 0
            mudTimer = 0
            # go through all the players in the game
            for pid, pl in players.items():
                # send each player a message to tell them about the new player
                mud.send_message(pid, "{} entered the game".format(players[id]["name"]))

            # send the new player a welcome message
            greeting = "\x1b[2J\x1b[H\n\r++++++++++++++++++++++++++++++++++++++++\n\r" \
                "Welcome to the "+ highlight("PARABOARD") + ", {}. ".format(players[id]["name"]) \
                + "\n\rType 'help' for a list of commands." + highlight(" BE CAREFUL!")
            mud.send_message(id, greeting)

            # send the new player the description of their current room
            mud.send_message(id, rooms[players[id]["room"]]["description"])

        # each of the possible commands is handled below. Try adding new
        # commands to the game!

        # 'help' command
        elif command == "help":

            # send the player back the list of possible commands
            mud.send_message(id, "Commands:")
            mud.send_message(id, "  say <message>  - Says something out loud, "
                                 + "e.g. 'say Hello'")
            mud.send_message(id, "  look           - Examines the "
                                 + "surroundings, e.g. 'look'")
            mud.send_message(id, "  go <exit>      - Moves through the exit "
                                 + "specified, e.g. 'go outside'")
            mud.send_message(id, "  logout      - logs off chat server "
                                 + "specified, e.g. 'logout'")

        # 'say' command
        elif command == "say" or command == ">":

            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them a message telling them what the player said
                    mud.send_message(pid, "{}{}".format(highlight(players[id]["name"] + " says: "), params))

        # 'look' command
        elif command == "look":

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # progress report
            #mud.send_message(id, "Progress: " + str(players[id]["progress"]))

            # send the player back the description of their current room
            mud.send_message(id, rm["description"])

            playershere = []
            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # ... and they have a name to be shown
                    if players[pid]["name"] is not None:
                        # add their name to the list
                        playershere.append(players[pid]["name"])

            # send player a message containing the list of players in the room
            mud.send_message(id, "Players here: {}".format(", ".join(playershere)))

            # send player a message containing the list of docs from this room
            mud.send_message(id, "Docs: {}".format(", ".join(rm["docs"])))

            # send player a message containing the list of exits from this room
            mud.send_message(id, "Other rooms: {}".format(", ".join(rm["exits"])))

        # 'view' command
        elif command == "view":
            target = params.lower()
            room = rooms[players[id]["room"]]
            if target in room["docs"]:
                mud.send_message(id, room["docs"][target])

        # 'go' command
        elif command == "go":

            # store the exit name
            ex = params.lower()

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # if the specified exit is found in the room's exits list
            if ex in rm["exits"]:

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same room and isn't the player
                    # sending the command
                    if players[pid]["room"] == players[id]["room"] \
                            and pid != id:
                        # send them a message telling them that the player
                        # left the room
                        mud.send_message(pid, "{} left via exit '{}'".format(
                                                      players[id]["name"], ex))

                # update the player's current room to the one the exit leads to
                players[id]["room"] = rm["exits"][ex]
                rm = rooms[players[id]["room"]]

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same (new) room and isn't the player
                    # sending the command
                    if players[pid]["room"] == players[id]["room"] \
                            and pid != id:
                        # send them a message telling them that the player
                        # entered the room
                        mud.send_message(pid,
                                         "{} arrived via exit '{}'".format(
                                                      players[id]["name"], ex))

                # send the player a message telling them where they are now
                mud.send_message(id, "You arrive at '{}'".format(
                                                          rooms[players[id]["room"]]["description"]))

            # the specified exit wasn't found in the current room
            else:
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit '{}'".format(ex))

        # 'go' command
        elif command == "logout":
            mud.send_message(id, "^]")

        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            # mud.send_message(id, "Unknown command '{}'".format(command))
            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them a message telling them what the player said
                    mud.send_message(pid, "{}{}".format(highlight(players[id]["name"] + " says: "), params))
