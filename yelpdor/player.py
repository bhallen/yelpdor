from game_obj import GameObj

class Player(GameObj):

    def __init__(self, x, y, char, color):
        GameObj.__init__(self, x, y, char, color)
        self.review_count = 0
        self.reputation = 0

    def update_reviewing_stats(self, facet_to_player_rating, business):
        self.review_count += 1
        self.reputation += business.get_review_similarity(facet_to_player_rating)

