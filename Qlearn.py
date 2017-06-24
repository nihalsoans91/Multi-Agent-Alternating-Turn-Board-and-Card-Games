from sequence import *
import pydealer
import random
import os
import json

class Qlearn:
    qdict={} #the q values for given state and action Q(s,a)
    policy = {} #the policy State -> Action
    alpha=0.9
    gamma=1

    def __init__(self, player):
        self.player = player
        self.qfilename = 'dictionary/qVal_' + str(player) + '.txt'
        if os.path.isfile(self.qfilename):
            self.qdict = json.load(open(self.qfilename,'r'))
        else:
            self.qdict = {}
            json.dump(self.qdict, open(self.qfilename, 'w'))
        
        self.pfilename = 'dictionary/policy_' + str(player) + '.txt'
        if os.path.isfile(self.qfilename):
            self.policy = json.load(open(self.pfilename,'r'))
        else:
            self.policy = {}
            json.dump(self.policy, open(self.pfilename, 'w'))

    def learn(self,state,action):
        self.updatemyQ(state,action)
        self.updateoppQ(state,action)
        self.updatepolicy()
        json.dump(self.qdict, open(self.qfilename, 'w'))
        json.dump(self.policy, open(self.pfilename, 'w'))
        return

    def insertIntoString(self, string, index, character):
        outString = ""
        for i in range(len(string)):
            if i == index:
                outString = outString + character[0]
            else:
                outString = outString + string[i]
        return outString

    def updatemyQ(self,state,action):
        key = str(self.player) + '|' + str(state) + '|' + str(action)
        Qvalue = 0
        if key in self.qdict.keys():
            Qvalue = qdict[key]
        board = state.split('-')[0]
        board1 = board
        self.insertIntoString(board1, int(cardLocations[pydealer.Card(str(action).split()[0],str(action).split()[2])]), self.player)
        #board1[int(cardLocations[pydealer.Card(str(action).split()[0],str(action).split()[2])])] = self.player
        reward = get_reward(board,action,self.player)
        Qvalue = Qvalue + self.alpha*(reward + self.gamma * max(self.nextQvalue(board1,a) for a in self.actionsInState(board1)) - Qvalue)
        self.qdict[key] = Qvalue
        return

    def nextQvalue(self, board, action):
        #key = str(self.player) + '|' + str(board) + 
        for key in self.qdict.keys():
            p = key.split('|')[0]
            s = key.split('|')[1]
            a = key.split('|')[2]
            b = s.split('-')[0]
            if b==board and a==str(action):
                return self.qdict[key]
        return 0

    def actionsInState(self, board):
        acts = []
        for i in range(len(board)):
            if board[i] == '_' and i not in [40, 49]:
                acts.append(list(cardLocations.keys())[list(cardLocations.values()).index(str(i))])
        return acts
    
    def updateoppQ(self,state,action):
        board = state.split('-')[0]
        opp = self.getOpponent()
        key = str(opp) + '|' + str(state) + '|' + str(action)
        Qvalue = 0
        if key in self.qdict.keys():
            Qvalue = qdict[key]
        for i in range(len(board)):
            if board[i] == opp:
                c = list(cardLocations.keys())[list(cardLocations.values()).index(str(i))]
                reward = get_reward(board,action,self.player)
                Qvalue = Qvalue + self.alpha*(reward - Qvalue)
                self.qdict[key] = Qvalue
        return

    def getOpponent(self):
        if self.player == 'B':
            return 'G'
        else:
            return 'B'
    
    def updatepolicy(self):
        for key in self.qdict.keys():
            k = key.split('|')
            p = k[0]
            if p == self.player:
                s = k[1]
                a = k[2]
                b = s.split('-')[0]
                h = s.split('-')[1].split(',')
                Qs = {}
                for c in h:
                    k1 = p + '|' + s + '|' + c
                    if k1 in self.qdict.keys():
                        Qs[c] = self.qdict[k1]
                    else:
                        Qs[c] = 0
                c = list(Qs.keys())[list(Qs.values()).index(max(Qs.values()))]
                self.policy[s] = str(c)
        return



    def play(self,state):
        board = state.split('-')[0]
        hand = state.split('-')[1].split(',')
        virtualCard = ""
        arPair = {}

        if ("Jack" in [a for a, b, c in [str(card).split() for card in hand]]) and ((board.count(self.getOpponent())) > 6):
            playCard, virtualCard, reward = self.choosebestmove(state)
            arPair[playCard] = reward
        if state in self.policy.keys():
            action = self.policy[state]
            reward = self.qdict[str(self.player)+'|'+ str(state) + '|' + str(action)]
            arPair[action] = reward
        else:
            while True:
                action = random.choice(hand)
                print("Random Action: ",action)
                reward = 0
                if action.split()[0] == "Jack":
                    continue
                else:
                    arPair[action] = reward
                    break
        location = ''
        card = list(arPair.keys())[list(arPair.values()).index(max(arPair.values()))]
        print(card)
        if str(card).split()[0] == "Jack":
            location = cardLocations[pydealer.Card(str(virtualCard).split()[0],str(virtualCard).split()[2])]
            self.learn(state, virtualCard)
        else:
            location = cardLocations[pydealer.Card(str(card).split()[0],str(card).split()[2])]
            self.learn(state, card)
        return card, location
    
    def choosebestmove(self, state):
        acts = {}
        board = state.split('-')[0]
        hand = [str(c) for c in state.split('-')[1].split(',')]
        if "Jack of Hearts" in hand:
            a, r = self.removebestcoin(state)
            acts["Jack of Hearts"] = [a, r]
        elif "Jack of Spades" in hand:
            a, r = self.removebestcoin(state)
            acts["Jack of Spades"] = [a, r]

        if "Jack of Clubs" in hand:
            temp = {}
            for key in self.qdict.keys():
                if self.player == key.split('|')[0] and board == key.split('|')[1].split('-')[0]:
                    temp[key.split('|')[2]] = self.qdict[key]
            if len(temp):
                a = list(temp.keys())[list(temp.values()).index(max(temp.values()))]
                r = temp[a]
            else:
                cl = [i for i,k in enumerate(board) if k=='_']
                cl.pop(cl.index(40))
                cl.pop(cl.index(49))
                a = str(list(cardLocations.keys())[list(cardLocations.values()).index(str(random.choice(cl)))])
                r = 0
            acts["Jack of Clubs"] = [a,r]

        elif "Jack of Diamonds" in hand:
            temp = {}
            for key in self.qdict.keys():
                if self.player == key.split('|')[0] and board == key.split('|')[1].split('-')[0]:
                    temp[key.split('|')[2]] = self.qdict[key]
            if len(temp):
                a = list(temp.keys())[list(temp.values()).index(max(temp.values()))]
                r = temp[a]
            else:
                cl = [i for i,k in enumerate(board) if k=='_']
                cl.pop(cl.index(40))
                cl.pop(cl.index(49))
                a = str(list(cardLocations.keys())[list(cardLocations.values()).index(str(random.choice(cl)))])
                r = 0
            acts["Jack of Diamonds"] = [a,r]
        print(acts)
        action = list(acts.keys())[list(acts.values()).index([a for i, a in enumerate(acts.values()) if a[1] == max(rew[1] for rew in acts.values())][0])]
        return action, acts[action][0], acts[action][1]
    
    def removebestcoin(self, state):
        opp = self.getOpponent()
        board = state.split('-')[0]
        maxQ = {}
        for key in self.qdict.keys():
            if opp == key.split('|')[0] and board == key.split('|')[1].split('-')[0]:
                maxQ[key.split('|')[2]] = self.qdict[key]
        if len(maxQ):
            card = list(maxQ.keys())[list(maxQ.values()).index(max(maxQ.values()))]
        else:
            cl = [i for i,k in enumerate(board) if k==opp]
            card = str(list(cardLocations.keys())[list(cardLocations.values()).index(str(random.choice(cl)))])
            maxQ[card] = 0
        return card, maxQ[card]
