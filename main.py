import cards
from game import Game

player_count = 4

hands = cards.deal(player_count)
print(hands)
game = Game(player_count, hands)
hands[0] = cards.sort_hand(hands[0])
print(hands[0])