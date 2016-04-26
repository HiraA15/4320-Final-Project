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
    
    def rAll(self):
        return range(len(self.data))            
                
    def query(self, location, categories, radius=.1):
        if type(location) == type(u"string") or type(location) == type("string"):
            #TODO?: input string parsing for non-exact matches
            #Check that location is in the cities set
            if location in self.cities:
                #Cull-by-city
                potentialBusinessSet = self._contains(range(len(self.data)), 'city', location)
            else:
                print "The City: " + location + " is unknown!"
        else:
            #get all businesses in radius!!!
            potentialBusinessSet = self.Map.query_ball_point(location, radius)
        
        #Categorize businesses in radius by interested category tags
        subsetsByCategory = []
        for category in categories:
            #Check that all categories are valid
            if category in self.categories:
                subset = self._contains(potentialBusinessSet, 'categories', category)
                if len(subset) > 0:
                    subsetsByCategory.append(subset)
            else:
                print "The category: " + category + " is unknown!"
        
        #TODO?: Some sort of query abort if one of the categories has none of that business type in the region
        
        #if there are more than a single category, find the closest clusters within the categories
        if(len(categories) == 0):
            return potentialBusinessSet
        elif(len(categories) == 1):
            return subsetsByCategory[0]
        else:
            KDMaps = self._groupings(subsetsByCategory)
            
            clusters = self._unorderedMinimum(KDMaps, subsetsByCategory)
            
            #TODO?: sort by distance to initial location, as well as cluster tightness?
            
            #Convert indicies back to data entries
            results = []
            for cluster in clusters:
                c = []
                for index in cluster[0]:
                    c.append(self.data[index])
                results.append((c, cluster[1]))
            return results 
    
    def significantCities(self, subset, cutoff):
        return self.significantData(subset, self.cities, "city", cutoff)
    
    def significantCategories(self, subset, cutoff):
        return self.significantData(subset, self.categories, "categories", cutoff)
    
    def significantData(self, subset, category_sets, field, cutoff):
        results = []
        for c in category_sets:
            r = self._contains(subset, field, c)
            if len(r) >= cutoff:
                results.append((len(r), c))
        return results
       
    def _contains(self, subset, field, value):
        result = []
        for i in subset:
            if value in self.data[i][field]:
                result.append(i)
        return result

    #Returns the KDTrees of the given groups
    def _groupings(self, groups):
        #Make a new KDTree for some of the groupings and query for nearest at each location?
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
    def _unorderedMinimum(self, groupings, links):
        self.Map.query
        results = []
        
        #Use the group of lowest length
        u = 0
        low = int("inf")
        for group in groupings:
            l = len(group)
            if l < low:
                low = l
                u = group
        
        for i in range(len(groupings[u].data)):
            points = [(u, i)]
            totalDist = 0
            remaining = range(len(groupings))
            remaining.remove(u)
            while len(remaining) > 0:
                #For each point in points, search each remaining group for the closest next business to add
                nearestPoint = (-1, -1)
                distance = float("inf")
                for group, index in points:
                    for r in remaining:
                        d, n = groupings[r].query(groupings[group].data[index])
                        if d < distance:
                            distance = d
                            nearestPoint = (r, n)
                remaining.remove(nearestPoint[0])
                points.append(nearestPoint)
                totalDist += distance
            #Convert back to global indicies
            complete = []
            for group, index in points:
                complete.append(links[group][index])
            results.append((complete, totalDist))
        
        #return results sorted by total distance (cluster tightness)
        return sorted(results, key=lambda group: group[1])

#TODO?: Commuting distance using google maps api

#TODO?: query latitude/longitude from street address? (or other google maps api interaction)
