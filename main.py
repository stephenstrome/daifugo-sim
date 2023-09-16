import cards
from game import Game

player_count = 4

hands = cards.deal(player_count)
for i in range(0, len(hands)):
    hands[i] = cards.sort_hand(hands[i])
game = Game(player_count, hands)
game.start(hands)

