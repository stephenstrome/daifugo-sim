class Game:
    player_count = 0
    current_player = 0
    last_played = ()
    shibari = False # must play same suit for rest of trick
    geki_shibari = False # must play same suit and next card in order for rest of trick 
    reverse_flow = False # cards strength is in reverse order for remainder of trick
    kakumei = False

    def new_trick(self):
        self.last_played = ()
        self.shibari = False
        self.geki_shibari = False
        self.reverse_flow = False

    def play_cards(cards):
        print("test")
        last_played = cards

    def validate_play(cards):
        print("test")

    def __init__(self, player_count, hands):
        self.player_count = player_count
        for i,k in hands.items():
            if("3d" in k):
                self.current_player = i
        print(self.current_player)