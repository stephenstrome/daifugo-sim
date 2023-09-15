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