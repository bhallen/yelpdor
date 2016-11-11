import os
import json


def load_eventset(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'res', 'events', name + '.json')
    fp = open(path).read()
    return json.loads(fp)
