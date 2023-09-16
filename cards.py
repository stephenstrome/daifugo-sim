import random

suits = ["d", "h", "c", "s"]
normal_cards = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2"]
special = {"jkr": 2}

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
    for i in normal_cards:
        value_list[i] = []
    for i in special.keys():
        value_list[i] = []
    for i in hand:
        if(i in special.keys()):
            value_list[i].append(i)
        else:
            if(i[0] in normal_cards):
                value_list[i[0]].append(i)

    # sort suits
    for i,k in value_list.items():
        if(i not in special.keys()):
            if(len(k) > 1):
                suit_indexes = []
                suit_sorted = []
                for card in k:
                    suit_indexes.append(suits.index(card[1]))
                for index in range(0,len(suits)):
                    try:
                        add_suit = suit_indexes.index(index)
                        suit_sorted.append(k[add_suit])
                    except:
                        add_suit = -1
                value_list[i] = suit_sorted

    