import json
from scipy import spatial


#from pprint import pprint

target = "business_data.txt"

def loadData(infile):
    data = []
    with open(infile, 'r') as inF:
        for line in inF:
            data.append(json.loads(line))
    return data

#TODO?: data as numpy array for cooler manipulation!
class KDMap:
    def __init__(self, data):
        self.data = []
        self.cities = set()
        self.categories = set()
        locations = []
        for entry in data:
            self.data.append(entry)
            locations.append([entry['latitude'], entry['longitude']])
            self.cities.add(entry['city'])
            for c in entry['categories']:
                self.categories.add(c)
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

#TODO?: Commuting distance using google maps api

#TODO: Parse for every category option
