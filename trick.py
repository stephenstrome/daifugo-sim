import copy
import cards

class Trick:
    finished = False
    shibari = False # must play same suit for rest of trick
    geki_shibari = False # must play same suit and next card in order for rest of trick 
    reverse_flow = False # cards strength is in reverse order for remainder of trick
    passed_players = []
    last_played = ()
    current_player = None
    run_validated = False

    def end_trick(self):
        self.finished = True

    def check_special(self, played_cards):
        special_played = False
        for card in played_cards:
            if(card[0] == "8"):
                special_played = True
                self.end_trick()
            elif(card[0] == "J"):
                special_played = True
                if(self.run_validated):
                    self.reverse_flow = not self.reverse_flow
                else:
                    self.reverse_flow = True
        return special_played

    def validate_run(self, played_cards):
        if(len(played_cards) >= 3):
            current_card = played_cards[0]
            for i in range(1, len(played_cards)):
                if(cards.check_next_in_order(current_card, played_cards[i]) and cards.same_suit(current_card, played_cards[i])):
                    current_card = played_cards[i]
                else:
                    return False
            return True
        return False
    
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
        valid = False
        # first play of trick, as long as cards match or it's a run, play is valid
        if(len(last_play) == 0):
            if(self.validate_match(next_play)):
                self.run_validated = False
                valid = True
            elif(self.validate_run(next_play)):
                self.run_validated = True
                valid = True
        elif(len(next_play) == len(last_play)): # make sure same amount of cards are submitted
            potential_better_card = next_play[0]
            potential_worse_card = last_play[0]
            if(self.reverse_flow): # if flow reverse, then the last play should be greater than the previous play
                potential_better_card = last_play[0]
                potential_worse_card = next_play[0]
            if(cards.check_first_card_greater(potential_better_card, potential_worse_card) and ((self.run_validated == False and self.validate_match(next_play)) or (self.run_validated == True and self.validate_run(next_play)))):
                valid = True
        return valid # play is not valid
    
    def reset_cards_selected(self,hand):
        return [],copy.deepcopy(hand)
    
    def next_player(self, current_player, player_count):
        current_player = current_player + 1
        if(current_player == player_count):
            current_player = 0
        return current_player

    def find_next_player(self, player_count):
        self.current_player = self.next_player(self.current_player, player_count)
        while(self.current_player in self.passed_players):
            self.current_player = self.next_player(self.current_player, player_count)
        if(len(self.passed_players) == player_count - 1): # handle all players passed or finished but one
            print("ending trick")
            self.end_trick()
        return self.current_player
    
    def play(self, hand):
        print("Player " + str(self.current_player + 1) + ": please play some cards.")
        print("The last cards played were: " + str(self.last_played))
        finished = False
        played_cards,temp_hand = self.reset_cards_selected(hand)
        while(not finished):
            print("Pending cards: " + str(played_cards))
            action = input(temp_hand)
            if(action == "reset"):
                played_cards,temp_hand = self.reset_cards_selected(hand)
            elif(action == "play"):
                if(self.validate_play(played_cards, self.last_played)):
                    special_played = self.check_special(played_cards)
                    self.last_played = played_cards
                    if(len(temp_hand) == 0):
                        self.passed_players.append(self.current_player)
                    finished = True
                else:
                    print("The cards played are invalid, please pick new cards.")
                    played_cards,temp_hand = self.reset_cards_selected(hand)
            elif(action == "skip"):
                self.passed_players.append(self.current_player)
                played_cards,temp_hand = self.reset_cards_selected(hand)
                finished = True
            else:
                if(action in temp_hand):
                    played_cards.append(action)
                    temp_hand.remove(action)
        return temp_hand
    
    def __init__(self, finished_players, current_player):
        print("finished: " + str(finished_players))
        self.passed_players = copy.deepcopy(finished_players)
        self.current_player = current_player