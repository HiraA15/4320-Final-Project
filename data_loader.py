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
    
def haversine(a, b, R):
    latDelta = a[0] - b[0]
    lonDelta = a[1] - b[1]
    a = math.pow(math.sin(latDelta/2), 2) +math.cos(a[0]) * math.cos(b[0]) * math.pow(math.sin(lonDelta/2),2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d
    

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