import json
import math
from scipy import spatial

#from pprint import pprint

target = "business_data.txt"
EarthRadius = 3959

def loadData(infile):
    data = []
    with open(infile, 'r') as inF:
        for line in inF:
            data.append(json.loads(line))
    return data

def haversine(begin, end):
    lati1, long1 = begin
    lati2, long2 = end
    radius = 6501

    dlati = math.radians(lati2-lati1)
    dlongi = math.radians(long2-long1)
    a = math.sin(dlati/2) * math.sin(dlati/2) + math.cos(math.radians(lati1)) \
        * math.cos(math.radians(lati2)) * math.sin(dlong/2) * math.sin(dlong/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


#TODO?: data as numpy array for cooler manipulation!
class KDMap:
    def __init__(self, data):
        self.data = []
        self.cities = set()
        self.categories = set()
        locations = []
        count = 0
        with open(target, 'r') as inF:
            for line in inF:
                self.data.append(json.loads(line))
                locations.append([self.data[count]['latitude'], self.data[count]['longitude']])
                count += 1
        self.Map = spatial.cKDTree(locations)

        for entry in data:
            self.data.append(entry)
            locations.append([entry['latitude'], entry['longitude']])
            self.cities.add(entry['city'])
            for c in entry['categories']:
                self.categories.add(c)
        self.Map = spatial.cKDTree(locations)

    def query(self, location, distance, categories):

        pass

    def contains(self, subset, field, value):
        result = []
        for i in subset:
            if value in self.data[i][field]:
                result.append(i)
        return result


#TODO: Advanced query
#input = location to focus on, categories to look for
#first step: use KDTree to cull the dataset down to only locations in the area
#next, find closest neighbors that fit the criteria (brute force it)
#rank results and return them

#TODO: Distance using haversine formula


#TODO?: Commuting distance using google maps api

#TODO?: query latitude/longitude from street address? (or other google maps api interaction)

#test = KDMap(loadData(target))
