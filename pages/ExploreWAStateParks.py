import requests
from bs4 import BeautifulSoup
import json


output_dist = {}
url = "https://washington.goingtocamp.com/api/maps/mapdatabyid"

def getTitle(map_id):
    j = {
        "mapId": map_id,
        "generateBreadcrumbs": "false"
    }

    res = requests.post(url, json=j)
    if res.status_code != 200:
        print(f"request for {map_id} failed")
    else:
        print(f"request for {map_id} succeeded")
        thisMap = res.json()['map']
        output_dist[map_id] = thisMap['localizedValues'][0]['title']
        list_child_maps = thisMap['mapLinks']
        for child_map in list_child_maps:
            getTitle(child_map['childMapId'])
    


init_map_id = -2147483335
getTitle(init_map_id)

with open("WA_State_Park_MapId.json", "w") as outfile: 
    json.dump(output_dist, outfile)

