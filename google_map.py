# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:32:18 2016

@author: Austin
"""

import googlemaps as gm
import json

with open('API_Keys.json') as cred_file:
    creds = json.load(cred_file)
    server_key = creds["google_maps"]
    
gmaps = gm.Client(key=server_key)

result = gmaps.reverse_geocode((40.714224, -73.961452))