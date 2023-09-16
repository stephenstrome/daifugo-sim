import copy
import cards

class Game:
    player_count = 0
    current_player = 0
    last_played = ()
    shibari = False # must play same suit for rest of trick
    geki_shibari = False # must play same suit and next card in order for rest of trick 
    reverse_flow = False # cards strength is in reverse order for remainder of trick
    kakumei = False
    placements = []
    passed_players = []

    def new_trick(self, current_player):
        self.last_played = ()
        self.shibari = False
        self.geki_shibari = False
        self.reverse_flow = False
        self.passed_players = []
        self.current_player = current_player
        print("The trick has ended, play will continue with player " + str(self.current_player + 1))

    def play_cards(self, next_play):
        print("test")
        last_played = next_play
    
    def validate_match(self, played_cards):
        card_value = played_cards[0][0]
        print(card_value)
        for i in range(0, len(played_cards)):
            print(played_cards[i][0])
            if(played_cards[i][0] != card_value):
                return False

        return True

    def validate_play(self, next_play, last_play):
        print(next_play)
        next_play = cards.sort_hand(next_play)
        # first play of trick, as long as cards match or it's a run, play is valid
        if(len(last_play) == 0 and (self.validate_match(next_play))):
            return True
        elif(len(next_play) == len(last_play)): # make sure same amount of cards are submitted
            if(cards.check_first_card_greater(next_play[0], last_play[0]) and (self.validate_match(next_play))):
                return True

        return False # play is not valid

    def reset_cards_selected(self,hands):
        return [],copy.deepcopy(hands[self.current_player])

    def next_player(self, current_player):
        current_player = current_player + 1
        if(current_player == self.player_count):
            current_player = 0
        return current_player

    def find_next_player(self, current_player):
        if(len(self.placements) == self.player_count - 1): # handle when all players finished but one
            while(current_player in self.placements):
                current_player = self.next_player(current_player)
        elif(len(self.placements + self.passed_players) == self.player_count - 1): # handle all players passed or finished but one
            while(current_player in self.passed_players or current_player in self.placements):
                current_player = self.next_player(current_player)
            self.new_trick(current_player)
        else: # handle getting the next player
            player_found = False
            while(not player_found):
                current_player = self.next_player(current_player)
                if(current_player not in self.passed_players and current_player not in self.placements):
                    player_found = True
        return current_player

    def start(self, hands):
        while(len(self.placements) < self.player_count - 1):
            print("Player " + str(self.current_player + 1) + ": please play some cards.")
            print("The last cards played were: " + str(self.last_played))

            action = ""
            played_cards,temp_hand = self.reset_cards_selected(hands)

            finished = False

            while(not finished):
                print("Pending cards: " + str(played_cards))
                action = input(temp_hand)
                if(action == "reset"):
                    played_cards,temp_hand = self.reset_cards_selected(hands)
                elif(action == "play"):
                    if(self.validate_play(played_cards, self.last_played)):
                        self.last_played = played_cards
                        hands[self.current_player] = temp_hand
                        if(len(hands[self.current_player]) == 0):
                            self.placements.append(self.current_player)
                            print("Congratulations! Player " + str(self.current_player + 1) + " placed in position " + str(len(self.placements)))
                        finished = True
                    else:
                        print("The cards played are invalid, please pick new cards.")
                        played_cards,temp_hand = self.reset_cards_selected(hands)
                elif(action == "skip"):
                    self.passed_players.append(self.current_player)
                    finished = True
                else:
                    if(action in temp_hand):
                        played_cards.append(action)
                        temp_hand.remove(action)
            
            self.current_player = self.find_next_player(self.current_player)

        self.placements.append(self.current_player)
        print("Uh oh! Player " + str(self.current_player + 1) + " came in last and is the daihinmin.")
            

    def __init__(self, player_count, hands):
        self.player_count = player_count
        for i,k in hands.items():
            if("3d" in k):
                self.current_player = i
        print("To set cards you want to play, write in the card value. When ready to play your cards, type \"play\". If you want to pass, type \"skip\". If you want to rethink your turn, type \"reset\".")