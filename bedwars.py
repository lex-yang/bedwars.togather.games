from threading import Timer
from datetime import datetime
import json
from tgmcee import core
from tgmcee.positions import *
from tgmcee import datastore as ds

_DEBUG = True

SPAWN_POINT = world(12, 31, 4)

LOBBY_POINT = world(0, 86, 235)
EYE_OF_STORM = world(0, 34, 235)

CENTER_OF_AUDIENCE_AREA = world(0, 78, 235)
AA_SIZE = 60
WALL_HEIGHT = 10

EAST_ISLAND = world(49, 39, 235)
SOUTH_ISLAND = world(0, 39, 284)
WEST_ISLAND = world(-49, 39, 235)
NORTH_ISLAND = world(0, 39, 186)

GAME_HOST = 'lex_yangt'


def CHAT_MSG(msg):
    core.mc_command('w {} {}'.format(GAME_HOST, msg))


def on_connected():
    print("I'm connected to the /v1 namespace!")
    core.set_host(GAME_HOST)
    
    # Quick Teleport Commands
    core.register_chat_command('.to', teleport_to)

    # Create Audience Area
    core.register_chat_command('.create', create_area)


##
##  Player Events
##
def on_player_join(player_id, x, y, z):
    print('Player Joint: ID = {}, pos = ({}, {}, {})'.format(player_id, x, y, z))
    pass

def on_player_leave(player_id, x, y, z):
    pass

##
##  Host Command
##
def tp_to_campus(player_id, cmd, args):
    pass

##
##  Chat Command
##
def teleport_to(cmd, args):
    if len(args) < 2:
        CHAT_MSG('.to {e|s|w|n|eye|lobby|spawn} ')
        return

    arg = args[1].lower()
    dest = None
    if arg == 'e':
        dest = EAST_ISLAND
    elif arg == 's':
        dest = SOUTH_ISLAND
    elif arg == 'w':
        dest = WEST_ISLAND
    elif arg == 'n':
        dest = NORTH_ISLAND
    elif arg == 'eye':
        dest = EYE_OF_STORM
    elif arg == 'lobby':
        dest = LOBBY_POINT
    elif arg == 'spawn':
        dest = SPAWN_POINT
    else:
        CHAT_MSG('Wrong argument !!! ')
        CHAT_MSG('.to {e|s|w|n|eye|lobby|spawn} ')
        return

    core.mc_command('tp {} {}'.format(GAME_HOST, dest.to_string()), _DEBUG)

def create_area(cmd, args):
    global AA_SIZE

    clear = False
    if len(args) < 2:
        CHAT_MSG('.create {aa|tk|wall} [size] [] clear')
        CHAT_MSG('aa = audience area')
        CHAT_MSG('tk = ticking area')
        CHAT_MSG('wall = walls surround audience area')
        return

    if len(args) > 2:
        if args[2] == 'clear':
            clear = True
        else:
            AA_SIZE = int(args[2])

    anchors = [
        pos(AA_SIZE, 0, AA_SIZE),
        pos(AA_SIZE, 0, -AA_SIZE),
        pos(-AA_SIZE, 0, -AA_SIZE),
        pos(-AA_SIZE, 0, AA_SIZE)]

    arg = args[1].lower()
    block = 'air' if clear else 'barrier'

    if arg == 'aa':
        for a in anchors:
            response, error = core.mc_command('fill {} {} {}'.format(CENTER_OF_AUDIENCE_AREA.add(a), CENTER_OF_AUDIENCE_AREA, block), _DEBUG)
            print(response)
    elif arg == 'wall':
        p = []
        for a in anchors:
            p.append(CENTER_OF_AUDIENCE_AREA.add(a))

        p.append(p[0])
        wallDelta = pos(0, WALL_HEIGHT, 0)
        for i in range(4):
           response, error = core.mc_command('fill {} {} {}'.format(p[i], p[i + 1].add(wallDelta), block), _DEBUG)

    elif arg == 'tk':
        if clear:
            core.mc_command('tickingarea remove_all')
            return

        no = 1
        for a in anchors:
            response, error = core.mc_command('tickingarea add {} {} p{} true'.format(
                CENTER_OF_AUDIENCE_AREA.add(a),
                CENTER_OF_AUDIENCE_AREA,
                no), _DEBUG)
            print(response)
            no += 1

############
# Initialization ...
#         
core.init(on_connected, on_player_join, on_player_leave)
ds.init(3)