import random
import functools

import numpy.random

from yelpdor.gui.messenger import Messenger
import utils

FACET_EVENT_MAP = {
    'Cleanliness': 'cleanliness',
    'Food/Drinks': 'fooddrink',
    'Service': 'service'
}

class Experience:

    def __init__(self, business):
        self.business = business
        self.category_to_steps = {
            'Restaurant': [
                (functools.partial(self.facet_experience,'Cleanliness'), 1.0),
                (functools.partial(self.facet_experience,'Food/Drinks'), 1.0),
                (functools.partial(self.facet_experience,'Service'), 1.0),
            ]
        }

    def describe(self):
        Messenger().message('You visit a {} called {}.'.format(
            str(self.business.__class__.__name__).lower(), self.business.name)
        )
        for step in self.category_to_steps[self.business.__class__.__name__]:
            if random.random() < step[1]:
                Messenger().message(step[0]())

    def facet_experience(self, facet):
        quality = self.business.facet_ratings[facet]
        events = utils.load_eventset(FACET_EVENT_MAP[facet])

        return numpy.random.choice(events[str(quality)])

class EventSet:

    def __init__(self, texts, probabilities):
        self.texts = texts
        self.probabilities = probabilities

    def sample(self):
        return numpy.random.choice(self.texts, p=self.probabilities)
