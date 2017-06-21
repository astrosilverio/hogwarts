from __future__ import absolute_import

from braga import World
from braga.examples import duel

from engine.Parser import Parser
from examples.duel.commands import commands


def setUp():
    # Make World
    duel_world = World()
    duel_world.add_system(duel.ContainerSystem)
    duel_world.add_system(duel.EquipmentSystem)
    duel_world.add_system(duel.NameSystem)

    # Make room
    duel_room = duel_world.make_entity(
        duel.room_factory,
        description="You are in a large, dusty room, standing at one end of a long wooden table. Someone has placed a sign on an easel that says 'Duelling club'. Justin Finch-Fletchley stands at the other end of the table, wand raised. You have only practiced one spell--expelliarmus.",
        name='Duel Room'
    )

    # Make duellers
    player = duel_world.make_entity(
        duel.player_factory,
        description="You stare trepidously down the table at Justin Finch-Fletchley.",
        location=duel_room,
        name="you")

    justin = duel_world.make_entity(
        duel.player_factory,
        description="Justin Finch-Fletchley stares at you bullishly from the other end of the table.",
        location=duel_room,
        name="justin finch-fletchley")

    # Make wands
    player_wand = duel_world.make_entity(
        duel.wand_factory,
        description="Surprisingly swishy.",
        location=player,
        name="your wand",
        owner=player)

    justin_wand = duel_world.make_entity(
        duel.wand_factory,
        description="Heavy but brittle.",
        location=justin,
        name="justin's wand",
        owner=justin)

    duel_world.systems[duel.EquipmentSystem].equip(player, player_wand)
    duel_world.systems[duel.EquipmentSystem].equip(justin, justin_wand)
    duel_world.systems[duel.EquipmentSystem].update()

    duel_world.systems[duel.NameSystem].update()
    duel_world.systems[duel.ContainerSystem].update()

    parser = Parser(duel_world, duel_world.systems[duel.NameSystem], player, commands)
    parser.name_system.add_alias("my wand", player_wand)
    parser.name_system.add_alias("his wand", justin_wand)
    parser.name_system.add_alias("justin", justin)

    return parser

if __name__ == '__main__':
    parser = setUp()
    while True:
        user_input = raw_input("> ").lower()
        if user_input == 'reset':
            parser = setUp()
        else:
            print parser.execute(user_input)
