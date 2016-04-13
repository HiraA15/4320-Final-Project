import json
from scipy import spatial
import math

#from pprint import pprint

target = "business_data.txt"

#TODO?: data as numpy array for cooler manipulation!
class KDMap:
    def __init__(self, target):
        self.data = []
        locations = []
        count = 0
        with open(target, 'r') as inF:
            for line in inF:
                self.data.append(json.loads(line))
                locations.append([self.data[count]['latitude'], self.data[count]['longitude']])
                count += 1
        self.Map = spatial.cKDTree(locations)

    def query(self, location, distance, categories):

        pass

    #TODO: some sort of function to cull a subset for those with a given attribute
    def contains(self, subset, category):
        result = []
        for i in subset:
            if category in self.data[i]['categories']:
                result.append(i)
        return result

#TODO: Advanced query
#input = location to focus on, categories to look for
#first step: use KDTree to cull the dataset down to only locations in the area
#next, find closest neighbors that fit the criteria (brute force it)
#rank results and return them

#TODO: Distance using haversine formula

        dlati = math.radians(lati2-lati1)
        a = math.sin(dlati/2) * math.sin(dlati/2) + math.cos(math.radians(lati1)) \
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        return d

#TODO?: Commuting distance using google maps api

#TODO: Parse for every category option
