# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:51:47 2016

@author: Austin
"""
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
"""
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)
"""
class ActiveData:
    def __init__(self, keys_file, categories_file):
        with open(keys_file) as cred_file:
            creds = json.load(cred_file)
            yelp_credentials = creds["yelp"]
            auth = Oauth1Authenticator(**yelp_credentials)
    
        with open(categories_file) as cat_file:
            self.categories = json.load(cat_file)

        self.client = Client(auth)
    
    #Intends to check the categories list for the query category
    def _cat_check(self, q):
        for i in self.categories:
            if i["title"].lower() == q.lower() or i["alias"].lower() == q.lower():
                return i['alias']
        return False
    
    def textQuery(self, location, categories):
        #get preliminary of EVERY category
        base = []
        for cat in categories:
            base.append(self.client.search(location, category_filter = cat))
        
        
        
        
    def closest(self, latitude, longitude, category):
        cat = self._cat_check(category)
        if cat == False:
            return False
        params = {
            'category_filter' : cat,
            'sort' : 1
        }
        
        return self.client.search_by_coordinates(latitude, longitude, **params)
        
       
    #TODO: Don't crash on crappy location argument

test = ActiveData('API_Keys.json', 'categories.json')
    