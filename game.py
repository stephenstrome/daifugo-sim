import copy
import cards
from trick import Trick

class Game:
    player_count = 0
    current_player = 0
    last_played = ()
    kakumei = False
    placements = []
    disqualified = []
    

    def new_trick(self, current_player):
        self.last_played = ()
        self.shibari = False
        self.geki_shibari = False
        self.reverse_flow = False
        self.run_validated = False
        self.passed_players = []
        self.current_player = current_player
        print("The trick has ended, play will continue with player " + str(self.current_player + 1))

    def play_cards(self, next_play):
        last_played = next_play

    def start(self, hands):
        while(len(self.placements + self.disqualified) < self.player_count - 1):
            trick = Trick((self.placements + self.disqualified), self.current_player, self.kakumei)
            while(not trick.finished):
                hands[trick.current_player] = trick.play(hands[trick.current_player])
                if(trick.cards_to_pass > 0):
                    player_receiving,new_hand,passed_cards = trick.pass_cards(hands[trick.current_player], self.player_count, self.placements)
                    trick.cards_to_pass = 0
                    hands[player_receiving] = cards.sort_hand(hands[player_receiving] + passed_cards)
                    hands[trick.current_player] = new_hand
                if(len(hands[trick.current_player]) == 0):
                    if(trick.special_played):
                        self.disqualified.append(trick.current_player)
                        print("Player " + str(self.current_player + 1) + " has been disqualified for going out on a special card.")
                    else:
                        self.placements.append(trick.current_player)
                        print("Congratulations! Player " + str(self.current_player + 1) + " placed in position " + str(len(self.placements)))
                if(trick.kakumei_trigger):
                    self.kakumei = not self.kakumei
                    trick.kakumei_trigger = False
                if(not trick.finished):
                    self.current_player = trick.find_next_player(self.player_count)

        self.placements.append(self.current_player)
        if(len(self.disqualified) > 0):
            print("The following players placed last due to playing a special card to go out:")
            for i in self.disqualified:
                print(str(i + 1))
        else:
            print("Uh oh! Player " + str(self.current_player + 1) + " came in last and is the daihinmin.")
            

    def __init__(self, player_count, hands):
        self.player_count = player_count
        for i,k in hands.items():
            if("3d" in k):
                self.current_player = i
        print("To set cards you want to play, write in the card value. When ready to play your cards, type \"play\". If you want to pass, type \"skip\". If you want to rethink your turn, type \"reset\".")