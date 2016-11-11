import random
import numpy.random

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
        events = {
            1: EventSet(['You see insects crawling all over the floor. One of the chefs pokes her head out from the kitchen, '
                    'stomps on a roach, and tosses it in her mouth.',
                 "You notice a huge raccoon gnawing on a bone in the corner of the room. "
                 "It pauses momentarily and glances at you calmly, then returns to its bone."],
                [0.5, 0.5]),
            2: EventSet(["There's a thick layer of dust and grime covering most of the tables."],
                [1.0]),
            3: EventSet(["There are some mysterious stains on your silverware, but otherwise the place looks tidy."],
                [1.0]),
            4: EventSet(["The restaurant looks like it's been remodeled recently, although it could use some dusting."],
                [1.0]),
            5: EventSet(["Everything from the legs of your chair to the waiters' foreheads is squeaky clean."],
                [1.0])
        }

        return events[quality].sample()

    def eating(self):
        quality = self.business.facet_ratings['Food/Drinks']
        events = {
            1: EventSet(['Food is 1.',
                 "Food is 1... you think."],
                [0.5, 0.5]),
            2: EventSet(["Food is 2."],
                [1.0]),
            3: EventSet(["Food is 3."],
                [1.0]),
            4: EventSet(["Food is 4."],
                [1.0]),
            5: EventSet(["Food is 5."],
                [1.0])
        }

        return events[quality].sample()


class EventSet:

    def __init__(self, texts, probabilities):
        self.texts = texts
        self.probabilities = probabilities

    def sample(self):
        return numpy.random.choice(self.texts, p=self.probabilities)
