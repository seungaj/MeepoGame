from game import *
from actor import *
import pytest
import pygame
import os

# USE PYGAME VARIABLES INSTEAD
keys_pressed = [0] * 323

# Setting key constants because of issue on devices
pygame.K_RIGHT = 1
pygame.K_DOWN = 2
pygame.K_LEFT = 3
pygame.K_UP = 4
pygame.K_LCTRIL = 5
pygame.K_z = 6
RIGHT = pygame.K_RIGHT
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
UP = pygame.K_UP
CTRL = pygame.K_LCTRL
Z = pygame.K_z


def setup_map(map: str) -> 'Game':
    """Returns a game with map1"""
    game = Game()
    game.new()
    game.load_map(os.path.abspath(os.getcwd()) + '/maps/' + map)
    game.new()
    game._update()
    game.keys_pressed = keys_pressed
    return game


def set_keys(up, down, left, right, CTRL=0, Z=0):
    keys_pressed[pygame.K_UP] = up
    keys_pressed[pygame.K_DOWN] = down
    keys_pressed[pygame.K_LEFT] = left
    keys_pressed[pygame.K_RIGHT] = right


def test1_move_player_up():
    """
    Check if player is moved up correctly
    """
    game = setup_map("student_map1.txt")
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    assert result == True
    assert game.player.y == 1


def test2_push_block():
    """
    Check if player pushes block correctly
    """
    game = setup_map("student_map2.txt")
    set_keys(0, 0, 0, 1)
    wall = \
    [i for i in game._actors if isinstance(i, Block) and i.word == "Wall"][0]
    result = game.player.player_move(game)
    assert game.player.x == 3
    assert wall.x == 4


def test3_create_rule_wall_is_push():
    """
    Check if player creates wall is push rule correctly
    """
    game = setup_map("student_map2.txt")
    set_keys(0, 0, 0, 1)
    wall = \
    [i for i in game._actors if isinstance(i, Block) and i.word == "Wall"][0]
    result = game.player.player_move(game)
    game._update()
    assert game._rules[0] == "Wall isPush"
    assert game.player.x == 3
    assert wall.x == 4


def test_4_follow_rule_wall_is_push():
    """
    Check if player follows rules correctly
    """
    game = setup_map("student_map3.txt")
    set_keys(0, 0, 0, 1)
    wall_object = game._actors[game._actors.index(game.player) + 1]
    result = game.player.player_move(game)
    assert game.player.x == 2
    assert wall_object.x == 3


def test_5_no_push():
    """
    Check if player is not able to push because of rule not existing
    """
    game = setup_map("student_map4.txt")
    set_keys(0, 0, 0, 1)
    wall_object = game._actors[game._actors.index(game.player) + 1]
    result = game.player.player_move(game)
    assert game.player.x == 2
    assert wall_object.x == 2


def test6_move_player_up_left():
    """
    Check if player is moved up then left correctly
    """
    game = setup_map("student_map1.txt")
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    assert game.player.y == 1
    assert game.player.x == 5

def test7_player_cannot_move():
    """
    Check if player and tile cannot move when stopped by other actor that
    cannot be moved
    """
    game = setup_map("student_map2.txt")
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    tile = [i for i in game._actors if isinstance(i, Is)][1]
    assert game.player.y == 1
    assert tile.y == 2

def test8_create_rule_rock_is_push_and_push():
    """
    Check if player creates wall is push rule correctly
    """
    game = setup_map("student_map4.txt")
    for _ in range(3):
        set_keys(0, 0, 0, 1)
        result = game.player.player_move(game)
    tile = \
        [i for i in game._actors if isinstance(i, Block) and i.word == "Rock"][0]
    game._update()
    assert game._rules[0] == "Rock isPush"
    assert game.player.x == 4
    assert tile.x == 5
    for _ in range(2):
        set_keys(0, 0, 1, 0)
        result = game.player.player_move(game)
    rock = \
        [i for i in game._actors if isinstance(i, Rock)][0]
    assert game.player.x == 2
    assert rock.x == 1


def test9_wall_is_lose():
    """
    Check if player creates wall is lose rule correctly and if player is at Wall
    and game is still running.
    """
    game = setup_map("student_map5.txt")
    for _ in range(4):
        set_keys(0, 0, 0, 1)
        result = game.player.player_move(game)
    for _ in range(3):
        set_keys(0, 1, 0, 0)
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    for _ in range(3):
        set_keys(0, 1, 0, 0)
        result = game.player.player_move(game)
    game._update()
    assert game._rules[0] == "Wall isLose"
    assert game.player.x == 9
    assert game.player.y == 8
    assert game._running == True


def test10_no_player():
    """
    Check if player is None if no rule indicating player
    """
    game = setup_map("student_map3.txt")
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    game._update()
    assert game.player == None


def test11_flag_is_win():
    """
    Check if player creates flag is win rule correctly
    """
    game = setup_map("student_map5.txt")
    for _ in range(4):
        set_keys(0, 0, 0, 1)
        result = game.player.player_move(game)
    for _ in range(5):
        set_keys(0, 1, 0, 0)
        result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    for _ in range(7):
        set_keys(0, 1, 0, 0)
        result = game.player.player_move(game)
    for _ in range(2):
        set_keys(0, 0, 0, 1)
        result = game.player.player_move(game)
    set_keys(0, 1, 0, 0)
    result = game.player.player_move(game)
    set_keys(0, 0, 0, 1)
    result = game.player.player_move(game)
    for _ in range(7):
        set_keys(1, 0, 0, 0)
        result = game.player.player_move(game)
    for _ in range(6):
        set_keys(0, 0, 0, 1)
        result = game.player.player_move(game)
    set_keys(1, 0, 0, 0)
    result = game.player.player_move(game)
    game._update()
    flag = \
        [i for i in game._actors if isinstance(i, Flag)][0]
    assert game._rules[0] == "Flag isVictory"
    assert game.player.x == 19
    assert game.player.y == 5
    assert flag.x == 19
    assert flag.y == 5
    assert flag._is_win == True


def test12_player_image():
    """
    Check if player image changes
    """
    game = setup_map("student_map3.txt")
    a = game.player.image
    set_keys(0, 0, 1, 0)
    result = game.player.player_move(game)
    game._update()
    b = game.player.image
    ans = a != b
    assert ans == True


if __name__ == "__main__":

    import pytest
    pytest.main(['student_tests.py'])

