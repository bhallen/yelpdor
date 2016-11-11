import random
import numpy.random

import utils

class Experience:

    def __init__(self, business):
        self.business = business
        self.category_to_steps = {
            'Restaurant': [
                (self.initial_impression, 1.0),
                # (self.ordering, 1.0),
                # (self.waiting, 1.0),
                (self.eating, 1.0)
            ]
        }

    def describe(self):
        print 'You visit a {} called {}.'.format(str(self.business.__class__.__name__).lower(), self.business.name)
        for step in self.category_to_steps[self.business.__class__.__name__]:
            if random.random() < step[1]:
                print step[0]()

    def initial_impression(self):
        quality = self.business.facet_ratings['Cleanliness']
        events = utils.load_eventset('cleanliness')

        return numpy.random.choice(events[str(quality)])

    def eating(self):
        quality = self.business.facet_ratings['Food/Drinks']
        events = utils.load_eventset('fooddrink')

        return numpy.random.choice(events[str(quality)])


class EventSet:

    def __init__(self, texts, probabilities):
        self.texts = texts
        self.probabilities = probabilities

    def sample(self):
        return numpy.random.choice(self.texts, p=self.probabilities)
