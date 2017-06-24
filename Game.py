"""
@author: Nihal & Adi
"""

from sequence import simpleSequence
from Qlearn import Qlearn
from minimaxQ import miniMAX
import random

    
def Q_Q(player, player2):
    Q1 = Qlearn(player)
    Q2 = Qlearn(player2)
    s = simpleSequence()
    s.print_board()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                print(state)
                card, location = Q1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                state = s.board_string() + '-' + s.getHand(player2)
                print(state)
                card, location = Q2.play(state)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.switch_player()

def M_M(player, player2):
    M1 = miniMAX(player)
    M2 = miniMAX(player2)
    s = simpleSequence()
    s.print_board()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                print(state)
                card, location = M1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                state = s.board_string() + '-' + s.getHand(player2)
                print(state)
                card, location = M2.play(state)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.switch_player()

def Q_R(player):
    Q1 = Qlearn(player)
    s = simpleSequence()
    s.print_board()
    while not s.complete():
        while True:
            if player == s.player:
                state = str(s.board_string()) + '-' + s.getHand(player)
                print(state)
                card, location = Q1.play(state)
                if not s.make_move(card,location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
            else:
                state = s.board_string() + '-' + s.getHand(player2)
                print(state)
                card = random.choice(s.available_moves())
                location=s.find_card_location(card)
                if not s.make_move(card, location):
                    print("Invalid Move!! Try Again!!")
                else:
                    break
        s.switch_player()

#Q_play_random(100)
#Q_human_player('G')
#Q_Q('B','G')
for i in range(1000):
    M_M('B','G')
for i in range(1000):
    Q_Q('B','G')
#minimax_human('G')
