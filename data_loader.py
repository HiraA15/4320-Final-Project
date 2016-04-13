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
    
def haversine(a, b, R=EarthRadius):
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
                
    def query(self, location, radius, categories):
        #get all businesses in radius!!!
        distances, potentialBusinessSet = self.Map.query_ball_point(location, radius)
        #Categorize businesses in radius by interested category tags
        subsetsByCategory = {}
        for category in categories:
            subsetsByCategory[category] = self.contains(potentialBusinessSet, 'categories', category)
        
        #if there are more than a single category, find the closest clusters within the categories
        #Hrm.... should I think of something more efficient than brute force comparisons
        results = self.groupings(subsetsByCategory)
        
        #TODO: sort groupings?
        return results
       
    def contains(self, subset, field, value):
        result = []
        for i in subset:
            if value in self.data[i][field]:
                result.append(i)
        return result

    #TODO!: returns a ranked list of groupings where there is one element from each set
    def groupings(self, sets):
        #TODO: Maybe make a new KDTree for some of the groupings and query for nearest at each location?
        #IDEA!: Make a KDTree for every category type?  Maybe figure out merges?
            #Important note: each new KDTree needs a mapping to the main data (since the numberings will be for the subset)
        pass

#TODO: Advanced query
#input = location to focus on, categories to look for
#first step: use KDTree to cull the dataset down to only locations in the area
#next, find closest neighbors that fit the criteria (brute force it)
#rank results and return them

#TODO: Distance using haversine formula

#TODO?: Commuting distance using google maps api

#TODO?: query latitude/longitude from street address? (or other google maps api interaction)

test = KDMap(loadData(target))