import itertools
import pydealer
import random
import pygame, sys, os

#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

pygame.init()

cardLocations = {pydealer.Card(value='2', suit='Diamonds'): '28', pydealer.Card(value='3', suit='Diamonds'): '27', pydealer.Card(value='4', suit='Diamonds'): '26', pydealer.Card(value='5', suit='Diamonds'): '25', pydealer.Card(value='6', suit='Diamonds'): '24', pydealer.Card(value='7', suit='Diamonds'): '23', pydealer.Card(value='8', suit='Diamonds'): '22', pydealer.Card(value='9', suit='Diamonds'): '12', pydealer.Card(value='10', suit='Diamonds'): '13', pydealer.Card(value='Queen', suit='Diamonds'): '14', pydealer.Card(value='King', suit='Diamonds'): '15', pydealer.Card(value='Ace', suit='Diamonds'): '16', pydealer.Card(value='2', suit='Clubs'): '35', pydealer.Card(value='3', suit='Clubs'): '36', pydealer.Card(value='4', suit='Clubs'): '37', pydealer.Card(value='5', suit='Clubs'): '38', pydealer.Card(value='6', suit='Clubs'): '39', pydealer.Card(value='7', suit='Clubs'): '29', pydealer.Card(value='8', suit='Clubs'): '19', pydealer.Card(value='9', suit='Clubs'): '9', pydealer.Card(value='10', suit='Clubs'): '8', pydealer.Card(value='Queen', suit='Clubs'): '7', pydealer.Card(value='King', suit='Clubs'): '18', pydealer.Card(value='Ace', suit='Clubs'): '17', pydealer.Card(value='2', suit='Hearts'): '6', pydealer.Card(value='3', suit='Hearts'): '5', pydealer.Card(value='4', suit='Hearts'): '4', pydealer.Card(value='5', suit='Hearts'): '3', pydealer.Card(value='6', suit='Hearts'): '2', pydealer.Card(value='7', suit='Hearts'): '1', pydealer.Card(value='8', suit='Hearts'): '11', pydealer.Card(value='9', suit='Hearts'): '21', pydealer.Card(value='10', suit='Hearts'): '31', pydealer.Card(value='Queen', suit='Hearts'): '32', pydealer.Card(value='King', suit='Hearts'): '33', pydealer.Card(value='Ace', suit='Hearts'): '34', pydealer.Card(value='2', suit='Spades'): '48', pydealer.Card(value='3', suit='Spades'): '47', pydealer.Card(value='4', suit='Spades'): '46', pydealer.Card(value='5', suit='Spades'): '45', pydealer.Card(value='6', suit='Spades'): '44', pydealer.Card(value='7', suit='Spades'): '43', pydealer.Card(value='8', suit='Spades'): '42', pydealer.Card(value='9', suit='Spades'): '41', pydealer.Card(value='10', suit='Spades'): '30', pydealer.Card(value='Queen', suit='Spades'): '20', pydealer.Card(value='King', suit='Spades'): '10', pydealer.Card(value='Ace', suit='Spades'): '0'}
jboard=10
iboard=5
seq=5
    

def ns(board,i,j,player):
    points=0
    ti=i # temporary i
    tj=j # temporary j
    if(ti-1>=0):
        while(board[ti-1][tj]==player): #should be ==2 and not borad[i][j]
            points=points+1
            ti=ti-1
            if(ti-1<=0):
                break
    ti=i
    tj=j
    if(ti+1<iboard):
        while(board[ti+1][tj]==player):
            points=points+1
            ti=ti+1
            if(ti+1>=iboard):
                break
    return points
        
        
# Calculates the coins East and west
def ew(board,i,j,player):
    nocoins=1
    points=0
    none=board[4][0]
    ti=i # temporary i
    tj=j # temporary j
    if(tj-1>=0):
        while(board[ti][tj-1]==player):
            points=points+1
            tj=tj-1
            if(tj-1<=0):
                break
    ti=i
    tj=j
    if(tj+1<jboard):
        while(board[ti][tj+1]==player):
            points=points+1
            tj=tj+1
            if(tj+1>=jboard):
                break
            ##print(tj)
    return points


# Calculates the coins for the right diagonal -> /
def rd(board,i,j,player):
    points=0
    ti=i # temporary i
    tj=j # temporary j
    if(ti-1>=0 and tj+1<jboard):
        while(board[ti-1][tj+1]==player ):
            points=points+1
            ti=ti-1
            tj=tj+1
            if(ti-1<=0 or tj+1>=jboard):
                break
    ti=i
    tj=j
    if(ti+1<iboard and tj-1>=0):
        while(board[ti+1][tj-1]==player):
            points=points+1
            ti=ti+1
            tj=tj-1
            if(ti+1>=iboard or tj-1<=0):
                break
    return points


# Calculates the coins for the right diagonal -> \
def ld(board,i,j,player):
    points=0
    ti=i # temporary i
    tj=j # temporary j
    if(ti+1<iboard and tj+1<jboard):
        while(board[ti+1][tj+1]==player):
            points=points+1
            ##print(points,":",i,",",j)
            
            ti=ti+1
            tj=tj+1
            if(ti+1>=iboard or tj+1>=jboard):
                break
    ti=i
    tj=j
    if(ti+1<iboard and tj-1<=0):
        ##print("i,j:",i,",",j,"while(board[ti+1][tj+1] ",board[ti+1][tj+1],"==player )")
        while(board[ti+1][tj-1]==player):
            points=points+1
            
            tj=tj-1
            ti=ti+1
            if(tj+1>=jboard or tj-1<0):
                break
    return points

def get_reward(board,card,player, location=None):
    reward=0
    board=str_2_mat(board)
    if location == None:
        location=cardLocations[pydealer.Card(str(card).split()[0],str(card).split()[2])]
    if(int(location)>=10):
        i=int(location[0])
        j=int(location[1])
    else:
        i=0
        j=int(location)
    #print("location=",location)           
    if(i-1>=0 and j-1>=0):
        reward=reward+max(ns(board,i-1,j-1,player),ew(board,i-1,j-1,player),rd(board,i-1,j-1,player),ld(board,i-1,j-1,player))
    if(i-1>=0):
        reward=reward+max(ns(board,i-1,j,player),ew(board,i-1,j,player),rd(board,i-1,j,player),ld(board,i-1,j,player))
    if(i-1>=0 and j+1<jboard):
        reward=reward+max(ns(board,i-1,j+1,player),ew(board,i-1,j+1,player),rd(board,i-1,j+1,player),ld(board,i-1,j+1,player))
    if(j+1<jboard):
        reward=reward+max(ns(board,i,j+1,player),ew(board,i,j+1,player),rd(board,i,j+1,player),ld(board,i,j+1,player))
    if(i+1<iboard and j+1<jboard):
        reward=reward+max(ns(board,i+1,j+1,player),ew(board,i+1,j+1,player),rd(board,i+1,j+1,player),ld(board,i+1,j+1,player))
    if(i+1<iboard and j-1>=0):
        reward=reward+max(ns(board,i+1,j-1,player),ew(board,i+1,j-1,player),rd(board,i+1,j-1,player),ld(board,i+1,j-1,player))
    if(j-1>=0):
        reward=reward+max(ns(board,i,j-1,player),ew(board,i,j-1,player),rd(board,i,j-1,player),ld(board,i,j-1,player))
    if(i+1<iboard):
        reward=reward+max(ns(board,i+1,j,player),ew(board,i+1,j,player),rd(board,i+1,j,player),ld(board,i+1,j,player))
    #else:
        ##print("exception has occured while reevaluating the reward!!")
        #return
    #print(reward)
    return reward

#converts to matrix
def str_2_mat(board):
    mat=[['_' for j in range(10)] for i in range(5)]
    p=0
    for i in range(5):
        for j in range(10):
            mat[i][j]=board[p]
            p=p+1
    return mat

class simpleSequence(object):
    cardLocations = {pydealer.Card(value='2', suit='Diamonds'): '28', pydealer.Card(value='3', suit='Diamonds'): '27', pydealer.Card(value='4', suit='Diamonds'): '26', pydealer.Card(value='5', suit='Diamonds'): '25', pydealer.Card(value='6', suit='Diamonds'): '24', pydealer.Card(value='7', suit='Diamonds'): '23', pydealer.Card(value='8', suit='Diamonds'): '22', pydealer.Card(value='9', suit='Diamonds'): '12', pydealer.Card(value='10', suit='Diamonds'): '13', pydealer.Card(value='Queen', suit='Diamonds'): '14', pydealer.Card(value='King', suit='Diamonds'): '15', pydealer.Card(value='Ace', suit='Diamonds'): '16', pydealer.Card(value='2', suit='Clubs'): '35', pydealer.Card(value='3', suit='Clubs'): '36', pydealer.Card(value='4', suit='Clubs'): '37', pydealer.Card(value='5', suit='Clubs'): '38', pydealer.Card(value='6', suit='Clubs'): '39', pydealer.Card(value='7', suit='Clubs'): '29', pydealer.Card(value='8', suit='Clubs'): '19', pydealer.Card(value='9', suit='Clubs'): '9', pydealer.Card(value='10', suit='Clubs'): '8', pydealer.Card(value='Queen', suit='Clubs'): '7', pydealer.Card(value='King', suit='Clubs'): '18', pydealer.Card(value='Ace', suit='Clubs'): '17', pydealer.Card(value='2', suit='Hearts'): '6', pydealer.Card(value='3', suit='Hearts'): '5', pydealer.Card(value='4', suit='Hearts'): '4', pydealer.Card(value='5', suit='Hearts'): '3', pydealer.Card(value='6', suit='Hearts'): '2', pydealer.Card(value='7', suit='Hearts'): '1', pydealer.Card(value='8', suit='Hearts'): '11', pydealer.Card(value='9', suit='Hearts'): '21', pydealer.Card(value='10', suit='Hearts'): '31', pydealer.Card(value='Queen', suit='Hearts'): '32', pydealer.Card(value='King', suit='Hearts'): '33', pydealer.Card(value='Ace', suit='Hearts'): '34', pydealer.Card(value='2', suit='Spades'): '48', pydealer.Card(value='3', suit='Spades'): '47', pydealer.Card(value='4', suit='Spades'): '46', pydealer.Card(value='5', suit='Spades'): '45', pydealer.Card(value='6', suit='Spades'): '44', pydealer.Card(value='7', suit='Spades'): '43', pydealer.Card(value='8', suit='Spades'): '42', pydealer.Card(value='9', suit='Spades'): '41', pydealer.Card(value='10', suit='Spades'): '30', pydealer.Card(value='Queen', suit='Spades'): '20', pydealer.Card(value='King', suit='Spades'): '10', pydealer.Card(value='Ace', suit='Spades'): '0'}
    
    size = width, height = 1450, 732
    screen = pygame.display.set_mode(size,pygame.FULLSCREEN,0)
    #print_board()
    reward =[[]]
    winning_combos = ([0, 10, 20, 30, 40], [1, 11, 21, 31, 41], [2, 12, 22, 32, 42], [3, 13, 23, 33, 43], [4, 14, 24, 34, 44], [5, 15, 25, 35, 45], [6, 16, 26, 36, 46], [7, 17, 27, 37, 47], [8, 18, 28, 38, 48], [9, 19, 29, 39, 49], [0, 1, 2, 3, 4], [10, 11, 12, 13, 14], [20, 21, 22, 23, 24], [20, 31, 32, 33, 34], [40, 41, 42, 43, 44], [1, 2, 3, 4, 5], [11, 12, 13, 14, 15], [21, 22, 23, 24, 25], [31, 32, 33, 34, 35], [41, 42, 43, 44, 45], [2, 3, 4, 5, 6], [12, 13, 14, 15, 16], [22, 23, 24, 25, 26], [32, 33, 34, 35, 36], [42, 43, 44, 45, 46], [3, 4, 5, 6, 7], [13, 14, 15, 16, 17], [23, 24, 25, 26, 27], [33, 34, 35, 36, 37], [43, 44, 45, 46, 47], [4, 5, 6, 7, 8], [14, 15, 16, 17, 18], [24, 25, 26, 27, 28], [34, 35, 36, 37, 38], [44, 45, 46, 47, 48], [5, 6, 7, 8, 9], [15, 16, 17, 18, 19], [25, 26, 27, 28, 29], [35, 36, 37, 38, 39], [45, 46, 47, 48, 49], [4, 13, 22, 31, 40], [5, 14, 23, 32, 41], [6, 15, 24, 33, 42], [7, 16, 25, 34, 43], [8, 17, 26, 35, 44], [9, 18, 27, 36, 45], [11, 22, 33, 44], [1, 12, 23, 34, 45], [2, 13, 24, 35, 46], [3, 14, 25, 36, 47], [4, 15, 26, 37, 48], [5, 16, 27, 38, 49])
    
    def __init__(self,squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(50)]
        else:
            self.squares = squares
        self.player = 'B'
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.p1_hand = pydealer.Stack()
        self.p2_hand = pydealer.Stack()
        self.deal_cards()


    def str_2_card(self,move):
        tempDeck = pydealer.Deck()
        hand=tempDeck.get(move)
        return hand
        

    def deal_cards(self):
        #global deck, p1_hand, p2_hand
        for i in range(10):
            if i%2 == 0:
                self.p1_hand.add(self.deck.deal())
            else:
                self.p2_hand.add(self.deck.deal())
    
    def print_board(self):
        #for element in [self.squares[i:i + 10] for i in range(0, len(self.squares), 10)]:
            ##print(element)
        board = pygame.image.load("board.png")
        bCoin = pygame.image.load("blue_coin.png")
        gCoin = pygame.image.load("green_coin.png")
        self.screen.blit(board, (250,100))
        for i in range(10):
            for j in range(5):
                rl = j * 125 + 137
                cl = i * 94 + 272
                e = self.squares[j*10+i]
                if e == 'B':
                    self.screen.blit(bCoin, (cl, rl))
                elif e == 'G':
                    self.screen.blit(gCoin, (cl, rl))
        pygame.display.flip()
        #self.printHand()

            
    def board_string(self):
        board_list = self.squares
        string = ''
        for i in board_list: 
            if i == None:
                string += '_'
            else:
                string += str(i)
        return string
            
    def available_moves(self):
        if self.player == 'B':
            r = [k for k in self.p1_hand]
            ##print(r)
            return r
        elif self.player == 'G':
            r = [k for k in self.p2_hand]
            ##print(r)
            return r
    
    def get_squares(self,player):
        return [k for k, v in enumerate(self.squares) if v == player]
        
    def make_move(self, card, location):
        empty = self.check_coin(location)
        if empty:
            self.place_coin(location, self.player)
        else:
            self.remove_coin(location)
        if self.player == 'B':
            self.p1_hand.get(str(card))
            self.p1_hand.add(self.deck.deal())
        elif self.player == 'G':
            self.p2_hand.get(str(card))
            self.p2_hand.add(self.deck.deal())
        return True

    def getHand(self, player):
        hand = ""
        if player == 'B':
            for card in self.p1_hand:
                hand = hand + "," + str(card)
        else:
            for card in self.p2_hand:
                hand = hand + "," + str(card)
        return hand[1:]

    def remove_coin(self, location):
        self.squares[int(location)] = None
        self.print_board()

    def place_coin(self, location, player):
        location = str(location)
        self.squares[int(location)] = player
        bCoin = pygame.image.load("blue_coin.png")
        gCoin = pygame.image.load("green_coin.png")
        #print("location",location)
        if len(location)==1:
            rl = 0 * 125 + 137
            cl = int(location[0]) * 94 + 272
        else:
            rl = int(location[0]) * 125 + 137
            cl = int(location[1]) * 94 + 272
        if player == 'B':
            self.screen.blit(bCoin, (cl, rl))
        elif player == 'G':
            self.screen.blit(gCoin, (cl, rl))
        pygame.display.flip()
        pygame.time.wait(200)
        #for element in [self.squares[i:i + 10] for i in range(0, len(self.squares), 10)]:
            #rint(element)


    def find_card_location(self, card):
        return self.cardLocations[card]

    def check_coin(self, location):
        if self.squares[int(location)]:
            return False
        else:
            return True
        
    def winner(self):
        b = [i for i,k in enumerate(self.squares) if k == 'B']
        g = [i for i,k in enumerate(self.squares) if k == 'G']
        b.extend([40,49])
        g.extend([40,49])
        for i in itertools.combinations(b,5):
            if list(i) in self.winning_combos:
                self.printComplete("Blue Won!")
                return 1
        for i in itertools.combinations(g,5):
            if list(i) in self.winning_combos:
                self.printComplete("Green Won!")
                return -1
        return 0
    
    def printComplete(self, cText):
        font = pygame.font.SysFont("comicsansms", 72)
        text = font.render(str(cText), True, (0, 0, 0))
        self.screen.blit(text, (725 - text.get_width() // 2, 366 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)

    def printTitle(self, cText):
        font = pygame.font.SysFont("comicsansms", 60)
        text = font.render(str(cText), True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0,0,0), (0, 0, 1450, 100), 0)
        self.screen.blit(text, (725 - text.get_width() // 2, 10))
        pygame.display.flip()

    def printHand(self):
        font = pygame.font.SysFont("comicsansms", 25)
        pygame.draw.rect(self.screen, (0,0,0), (0, 0, 250, 600), 0)
        pygame.draw.rect(self.screen, (0,0,0), (1200, 0, 1450, 600), 0)
        text = font.render("BLUE", True, (51, 51, 204))
        self.screen.blit(text, (125 - text.get_width() // 2, 100))
        y = 150
        for card in self.p1_hand:
            text = font.render(str(card), True, (51, 51, 204))
            self.screen.blit(text, (125 - text.get_width() // 2, y))
            y = y+50
        text = font.render("GREEN", True, (18, 161, 18))
        self.screen.blit(text, (1325 - text.get_width() // 2, 100))
        y = 150
        for card in self.p2_hand:
            text = font.render(str(card), True, (18, 161, 18))
            self.screen.blit(text, (1325 - text.get_width() // 2, y))
            y = y + 50
        pygame.display.flip()

    def complete(self):
        #print("Deck: ",len(self.deck),", P1: ", len(self.p1_hand),", P2: ", len(self.p2_hand))
        if self.winner(): return True
        if len(self.p1_hand)<=0 or len(self.p2_hand)<=0:
            self.printComplete("Draw! No cards left!")
            return True
        if len(self.deck)<=0:
            self.printComplete("Draw! No cards left!")
            return True
        return False
        
    def switch_player(self):
        if self.player == 'G': self.player = 'B'
        else: self.player = 'G'
