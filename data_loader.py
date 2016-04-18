import json
import math
from scipy import spatial

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
        
        #TODO?: Return distances?
        #if there are more than a single category, find the closest clusters within the categories
        if(len(categories) == 0):
            return potentialBusinessSet
        elif(len(categories) == 1):
            return subsetsByCategory[0]
        else:
            KDMaps = self.groupings(subsetsByCategory)
            
            results = self.unorderedMinimum(KDMaps, potentialBusinessSet)
            #TODO: based on query type, either look for unordered minimums or ordered minimum groupings
            #TODO: sort groupings?
            return results
        
       
    def contains(self, subset, field, value):
        result = []
        for i in subset:
            if value in self.data[i][field]:
                result.append(i)
        return result

    #TODO!: returns a ranked list of groupings where there is one element from each set
    def groupings(self, groups):
        #TODO: Maybe make a new KDTree for some of the groupings and query for nearest at each location?
        KDMaps = []
        
        for group in groups:
            locations = []
            for index in group:
                entry = self.data[index]
                locations.append([entry['latitude'], entry['longitude']])
            KDMaps.append(spatial.cKDTree(locations))
        
        return KDMaps
        
       


    #Now we have our KDMaps, and groups to hold the linking indicies to 
    #For each point in one of the sets, find the nearest point from every other set
    #For all points in each in-progress group, find the closest point of the new type to add to the group
    def unorderedMinimum(self, groupings, links):
        self.Map.query
        results = []
        for i, seed in enumerate(groupings[0].data):
            points = [seed]
            totalDist = 0
            for KDTree in groupings[1:]:
                nearest = []
                distance = float("inf")
                #TODO!!: Fix this.  If the 3rd location is between the first two, the distance calculation is wrong...
                    #Either recalculate distance after points are chosen or use some sort of centroid approach?
                for point in points:
                    d, n = KDTree.query(point)
                    if d < distance:
                        distance = d
                        nearest = n
                points.append(nearest)
                totalDist
        #Get first location, query into first group
        #query first and second into third group
        #query 1,2,3 into next... etc.
        pass
    
    #TODO: Ordered query, modify the search for business types in-order!
    #This means that you intend to visit each business category in the order they were given, rather than just checking overall proximity
    def orderedMinimum(self, groupings):
        pass
    
    
#TODO: Advanced query
#input = location to focus on, categories to look for
#first step: use KDTree to cull the dataset down to only locations in the area
#next, find closest neighbors that fit the criteria (brute force it)
#rank results and return them

#TODO?: Commuting distance using google maps api

#TODO?: query latitude/longitude from street address? (or other google maps api interaction)

test = KDMap(loadData(target))