"""
@author: Nihal & Adi
"""

from sequence import simpleSequence
from Qlearn import Qlearn
from minimaxQ import miniMAX
import random
import time


def M_M(player, player2):
    M1 = miniMAX(player)
    M2 = miniMAX(player2)
    s = simpleSequence()
    s.printTitle("Minimax Q vs Minimax Q")
    s.print_board()
    s.printHand()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                #print(state)
                card, location = M1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                state = s.board_string() + '-' + s.getHand(player2)
                #print(state)
                card, location = M2.play(state)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.printHand()
        s.switch_player()

def Q_Q(player, player2):
    Q1 = Qlearn(player)
    Q2 = Qlearn(player2)
    s = simpleSequence()
    s.printTitle("Q Learning vs Q Learning")
    s.print_board()
    s.printHand()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                #print(state)
                card, location = Q1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                state = s.board_string() + '-' + s.getHand(player2)
                #print(state)
                card, location = Q2.play(state)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.printHand()
        s.switch_player()


def Q_M(player, player2):
    Q1 = Qlearn(player)
    M2 = miniMAX(player2)
    s = simpleSequence()
    time.sleep(10)
    s.printTitle("Minimax Q vs Q Learning")
    s.print_board()
    s.printHand()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                #print(state)
                card, location = Q1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                state = s.board_string() + '-' + s.getHand(player2)
                #print(state)
                card, location = M2.play(state)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.printHand()
        s.switch_player()

def Q_R(player):
    Q1 = Qlearn(player)
    s = simpleSequence()
    s.printTitle("Q Learning vs Random")
    s.print_board()
    s.printHand()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                #print(state)
                card, location = Q1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                #state = s.board_string() + '-' + s.getHand(player2)
                #print(state)
                card = random.choice(s.available_moves())
                #print(card.suit)
                while (card.value=='Jack'):
                    card = random.choice(s.available_moves())
                location=s.find_card_location(card)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.printHand()
        s.switch_player()

def M_R(player):
    M1 = miniMAX(player)
    s = simpleSequence()
    s.printTitle("Minimax Q vs Random")
    s.print_board()
    s.printHand()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                #print(state)
                card, location = M1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                #state = s.board_string() + '-' + s.getHand(player2)
                #print(state)
                card = random.choice(s.available_moves())
                #print(card.suit)
                while (card.value=='Jack'):
                    card = random.choice(s.available_moves())
                location=s.find_card_location(card)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.printHand()
        s.switch_player()

Q_M('B','G')
Q_Q('B','G')
Q_R('B')
M_R('B')
M_M('B', 'G')
