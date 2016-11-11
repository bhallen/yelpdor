from collections import defaultdict
import math
import numpy as np
import numpy.linalg
import numpy.random
import os
import random

import lib.libtcodpy as libtcod

from yelpdor.experience import Experience
from yelpdor.gui.messenger import Messenger
from yelpdor.npc import NPC
import utils

BIZ_COUNT = 10
BIZ_TRUE_RATING_DISTRIBUTION = [0.2, 0.2, 0.2, 0.2, 0.2]


FACET_SD = 1.5
FACET_REVIEW_SD = 1.5
REVIEW_COUNT_SD = 5
REVIEW_COUNT_MEAN = 3
RESTAURANT_COST = 5

REGION_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/jice_region.cfg'

class District:
    """A level or floor of the city containing Businesses.

    distribution: list of floats (length 5)
        Probability of businesses having true score means with the values [1, 2, 3, 4, 5], respectively.
    review_count_mean: int
        mean for generating review count
    bizname_data: dict from biznames.json
    """

    def __init__(self,
                 distribution=BIZ_TRUE_RATING_DISTRIBUTION,
                 review_count_mean=REVIEW_COUNT_MEAN):
        self.businesses = []
        self.business_coords_to_name = {}
        self.distribution = distribution
        self.review_count_mean = review_count_mean
        self.bizname_data = utils.load_name_recipes('biznames')

    def __repr__(self):
        return '\n\n'.join([str(business) for business in self.businesses])

    def __str__(self):
        return self.__repr__()

    def add_business(self, room):
        biz = Restaurant(numpy.random.choice(range(1, 6), p=self.distribution),
                         self.review_count_mean,
                         RESTAURANT_COST,
                         room,
                         self.bizname_data)
        self.businesses.append(biz)
        return biz

    def find_business_containing_player(self, player):
        for biz in self.businesses:
            if biz.room.contains(player.x, player.y):
                return biz

        return None

    def sorted_by_distance(self, player):
        return sorted(self.businesses, key=lambda biz: self.player_biz_distance(player, biz))

    def player_biz_distance(self, player, biz):
        # euclidean distance, i.e. distance as the crow flies
        return numpy.linalg.norm(np.array(biz.room.center()) - np.array((player.x, player.y)))


class Business:
    """A Business with its true scores, category, reviews, etc.
    """
    def __init__(self):
        self.fulfillment_multiplier = 1

    def generate_facet_score(self):
        score = -1
        while not score in range(1, 6):
            score = round(numpy.random.normal(loc=self.true_rating, scale=FACET_SD))
        return int(score)

    def determine_review_count(self, review_count_mean):
        count = round(numpy.random.normal(loc=review_count_mean, scale=REVIEW_COUNT_SD))
        if count < 0:
            count = 0
        return int(count)

    def generate_reviews(self):
        return [self.generate_review() for i in range(self.review_count)]

    def generate_review(self):
        return Review([(facet, self.sample_facet_review(self.facet_ratings[facet])) for facet in self.ordered_facets])

    def aggregate_facet_reviews(self):
        if not self.review_count:
            return {facet: 0 for facet in self.ordered_facets}
        else:
            facet_to_reviews = defaultdict(list)
            for review in self.reviews:
                for facet in self.ordered_facets:
                    facet_to_reviews[facet].append(review.ratings[facet])
            return {facet: sum(facet_to_reviews[facet])/float(self.review_count) for facet in self.ordered_facets}

    def aggregate_overall_reviews(self):
        return sum([rating for facet, rating in self.aggregated_facet_ratings.items()])/float(len(self.ordered_facets))

    def sample_facet_review(self, facet_rating):
        rating = -1
        while not rating in range(1, 6):
            rating = round(numpy.random.normal(loc=facet_rating, scale=FACET_REVIEW_SD))
        return int(rating)

    def get_review_similarity(self, player_review):
        """In range [0, 1], with 0 for all reviews differing from the true ratings by more than half of
        the maximum possible difference"""
        raw_difference = (((self.max_player_review_difference / 2.) -
                sum([abs(player_review.ratings[facet] - self.facet_ratings[facet]) for facet in self.ordered_facets])) /
                self.max_player_review_difference)
        return raw_difference if raw_difference >= 0 else 0

    def visit(self, player):
        if self.visited:
            Messenger().message('You\'ve already visited this business. Try going somewhere else.')
        elif player.dollars < self.cost:
             Messenger().message('You can\'t afford to eat here.')
        else:
            e = Experience(self)
            e.describe()
            Messenger().message(' ')
            player.hunger = max(0, player.hunger - self.facet_ratings['Food/Drinks'] * self.fulfillment_multiplier)
            player.dollars -= self.cost

    def leave_review(self, player):
        self.visited = True
        fake_player_review = self.generate_review()
        Messenger().message('You leave a review of {}...'.format(self.name))
        Messenger().message(' ')
        player.update_reviewing_stats(fake_player_review, self)


class Restaurant(Business):
    """A Restaurant with its true scores, category, reviews, etc.

    mean: int in range(1,6)
        The true overall rating of a Restaurant
    review_count_mean: int
        mean for generating review count
    room: Rect
    bizname_data: dict from biznames.json
    """

    ordered_facets = ['Food/Drinks', 'Service', 'Cleanliness'] # ordered for display

    def __init__(self, mean, review_count_mean, cost, room, bizname_data, fulfillment_multiplier=4):
        libtcod.namegen_parse(REGION_NAME_CFG_PATH)

        self.visited = False
        self.bizname_data = bizname_data
        self.fulfillment_multiplier = fulfillment_multiplier
        self.owner = NPC()
        self.name = self.generate_name()
        self.true_rating = mean
        self.facet_ratings = {facet: self.generate_facet_score() for facet in self.ordered_facets}
        self.review_count = self.determine_review_count(review_count_mean)
        self.reviews = self.generate_reviews()
        self.aggregated_facet_ratings = self.aggregate_facet_reviews()
        self.rounded_aggregated_facet_ratings = {facet: int(round(rating))
                                                 for facet, rating in self.aggregated_facet_ratings.items()}
        self.aggregated_overall_rating = self.aggregate_overall_reviews()
        self.rounded_aggregated_overall_rating = int(round(self.aggregated_overall_rating))
        self.max_player_review_difference = 4.0 * len(self.ordered_facets)
        self.cost = cost
        self.room = room
        self.attributes = [] # not yet implemented

    def __repr__(self):
        return '\n'.join([
            'Name: {}'.format(self.name),
            'True rating: {}'.format(format_rating(self.true_rating)),
            '\n'.join(['> True {}: {}'.format(
                facet, format_rating(self.facet_ratings[facet])) for facet in self.ordered_facets]),
            'Review aggregate: {} (based on {} reviews)'.format(
                format_rating(self.rounded_aggregated_overall_rating), self.review_count),
            '\n'.join(['> {}: {}'.format(
                facet, format_rating(self.rounded_aggregated_facet_ratings[facet])) for facet in self.ordered_facets]),
            'Check business.reviews to see individual reviews.'
            # '\n'.join(['> Review {}\n{}'.format(i+1, review) for i, review in enumerate(self.reviews)])
            ])

    def generate_name(self):
        recipe = random.choice(self.bizname_data['recipes'])
        fillers = {label: random.choice(content) for label, content in self.bizname_data.items() if label != 'recipes'}
        fillers.update({'owner': self.owner.name, 'region': libtcod.namegen_generate('region')})
        return recipe.format(**fillers)


class Review:

    def __init__(self, facet_ratings):
        self.ordered_facets = [facet for facet, rating in facet_ratings]
        self.ratings = {facet: rating for facet, rating in facet_ratings}

    def __repr__(self):
        return '\n'.join(['> > {}: {}'.format(facet, format_rating(self.ratings[facet])) for facet in self.ordered_facets])


def format_rating(rating):
    if rating > 0:
        return '[{}{}]'.format('*'*rating, ' '*(5-rating))
    else:
        return '[  ?  ]'


if __name__ == "__main__":
    d = District()
    print(d)
