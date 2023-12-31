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
    special_played = False
    cards_to_pass = 0
    second_turn = False
    kakumei_trigger = False

    def check_kakumei(self, played_cards):
        if(self.run_validated and len(played_cards) >= 5):
            return True
        elif(not self.run_validated and len(played_cards) == 4):
            return True
        else:
            return False

    def check_valid_shibari(self, played_cards):
        shibari = True
        for i in range(0, len(self.last_played)):
            if(self.last_played[i][1] != played_cards[i][1]):
                shibari = False
        return shibari
    
    def check_valid_geki_shibari(self, played_cards):
        geki_shibari = True
        for i in range(0, len(self.last_played)):
            if(self.last_played[i][1] != played_cards[i][1]):
                geki_shibari = False
            if((not cards.check_next_in_order(self.last_played[i], played_cards[i]) and not self.reverse_flow) or (not cards.check_next_in_order(played_cards[i], self.last_played[i]) and self.reverse_flow)):
                geki_shibari = False
        return geki_shibari

    def update_shibari_status(self, played_cards):
        self.shibari = self.check_valid_shibari(played_cards)
        self.geki_shibari = self.check_valid_geki_shibari(played_cards)
        self.second_turn = False

    def end_trick(self):
        self.finished = True

    def check_special(self, played_cards):
        jack_repeat = False
        special_played = False
        for card in played_cards:
            if(card[0] == "8"):
                special_played = True
                self.end_trick()
            elif(card[0] == "J"):
                special_played = True
                if not jack_repeat:
                    self.reverse_flow = not self.reverse_flow
                    jack_repeat = True
            elif(card[0] == "7"):
                self.cards_to_pass = self.cards_to_pass + 1
            elif((card[0] == "2" and not self.reverse_flow) or (card[0] == "3" and self.reverse_flow)):
                special_played = True
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
        for i in range(0, len(played_cards)):
            if(played_cards[i][0] != card_value):
                return False

        return True

    def validate_play(self, next_play, last_play):
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
                # check shibari
                if(self.geki_shibari):
                    # check same suit and next in order
                    if(self.check_valid_geki_shibari(next_play)):
                        valid = True
                elif(self.shibari):
                    # check same suit
                    if(self.check_valid_shibari(next_play)):
                        valid = True
                else:
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
            self.end_trick()
        return self.current_player
    
    def pass_cards(self, hand, player_count, finished_players):
        player_receiving = self.current_player
        while(self.current_player == player_receiving or player_receiving in finished_players):
            player_receiving = self.next_player(player_receiving, player_count)
        print("Player " + str(self.current_player + 1) + ": pass up to " + str(self.cards_to_pass) + " cards to player " + str(player_receiving + 1) + ". Type play when ready to pass.")
        finished = False
        played_cards,temp_hand = self.reset_cards_selected(hand)
        while(not finished):
            print("Pending cards: " + str(played_cards))
            action = input(temp_hand)
            if(action == "reset"):
                played_cards,temp_hand = self.reset_cards_selected(hand)
            elif(action == "play"):
                if(len(played_cards) <= self.cards_to_pass):
                    if(len(temp_hand) == 0):
                        self.passed_players.append(self.current_player)
                    finished = True
                else:
                    print("The cards played are invalid, please pick new cards.")
                    played_cards,temp_hand = self.reset_cards_selected(hand)
            elif(action == "skip"):
                played_cards,temp_hand = self.reset_cards_selected(hand)
                finished = True
            else:
                if(action in temp_hand):
                    played_cards.append(action)
                    temp_hand.remove(action)
        return player_receiving,temp_hand,played_cards
    
    def play(self, hand):
        self.special_played = False
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
                    self.special_played = self.check_special(played_cards)
                    if(self.check_kakumei(played_cards)):
                        self.reverse_flow = not self.reverse_flow
                        self.kakumei_trigger = True
                    if(self.second_turn):
                        self.update_shibari_status(played_cards)
                    if(len(self.last_played) == 0):
                        self.second_turn = True
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
    
    def __init__(self, finished_players, current_player, kakumei):
        self.passed_players = copy.deepcopy(finished_players)
        self.current_player = current_player
        if(kakumei):
            self.reverse_flow = True