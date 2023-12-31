import random

suits = ["d", "h", "c", "s"]
normal_cards = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2"]
special = {"jkr": 2}

def same_suit(first_card, second_card):
    return first_card[1] == second_card[1]

def check_next_in_order(original_card, next_card):
    return (normal_cards.index(next_card[0]) - normal_cards.index(original_card[0]) == 1)

# Check if first card has a greater index in normal cards
def check_first_card_greater(first_card, second_card):
    if(normal_cards.index(first_card[0]) > normal_cards.index(second_card[0])):
        return True
    return False

def shuffle():
    deck = []
    for i in suits:
        for x in normal_cards:
            deck.append(x + i)
    for x,y in special.items():
        for i in range(0,y):
            deck.append(x)

    random.shuffle(deck)
    return deck

def deal(player_count):
    deck = shuffle()
    current_player = 0
    hands = {}
    for i in range(0, player_count):
        hands[i] = []
    for i in deck:
        hands[current_player].append(i)
        current_player += 1
        if(current_player == player_count):
            current_player = 0

    return hands

def sort_hand(hand):
    value_list = {}

    # sort value in ascending order
    for i in normal_cards: # build dictionary of each numerical card type
        value_list[i] = []
    for i in special.keys(): # sort special cards at very end of the list
        value_list[i] = []
    for i in hand: # add each numerical card to the appropriate list
        if(i in special.keys()):
            value_list[i].append(i)
        else:
            if(i[0] in normal_cards):
                value_list[i[0]].append(i)

    # sort suits
    for i,k in value_list.items():
        if(i not in special.keys()): # make sure it's not a non-numerical card
            if(len(k) > 1): # If there's only one card, no need to sort by suit
                suit_indexes = []
                suit_sorted = []
                for card in k: # Get the order of each suit
                    suit_indexes.append(suits.index(card[1]))
                for index in range(0,len(suits)): # loop through each suit in order, if suit present add that suit to beginning of new list
                    try:
                        add_suit = suit_indexes.index(index)
                        suit_sorted.append(k[add_suit])
                    except:
                        add_suit = -1
                value_list[i] = suit_sorted

    sorted_hand = []
    for cards in value_list.values(): # add every card to single list
        sorted_hand = sorted_hand + cards
    return sorted_hand

    