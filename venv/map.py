import pickle
from math import pi , acos , sin , cos
import random
import heapq
from tkinter import *

file_id = open('data1', "rb")
file_city = open("data2", "rb")
file_graph = open("data3", "rb")
id_dict = pickle.load(file_id)
city_dict = pickle.load(file_city)
graph_dict = pickle.load(file_graph)

def calcd(y1,x1, y2,x2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   # if (and only if) the input is strings
   # use the following conversions
   if y1==y2 and x1==x2:
       return 0
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

"""class Node:
    def __init__(self, v, lat, long, children, g, h):
        self.id = v
        self.coord = (lat, long)
        self.children = children
        self.g = g
        self.h = h
        self.f = g+h
    def __lt__(self, other):
        return self.f < other.f
def A_star(start, end):
    fringe = []
    visited = set()
    heapq.heapify(fringe)
    start_id = city_dict[start]
    goal_id = city_dict[end]
    lat, long = id_dict[start_id]
    latEnd, longEnd = id_dict[goal_id]
    state = Node(start_id, lat, long, graph_dict[start_id], 0, calcd(lat, long, latEnd, longEnd))
    #goal = Node(goal_id, latEnd, longEnd, graph_dict[goal_id], 0, 0)
    heapq.heappush(fringe, state)
    while len(fringe)!=0:
        v = heapq.heappop(fringe)
        if v.coord==id_dict[goal_id]: return v, v.g
        if v in visited: continue
        visited.add(v)
        for c in v.children:
            if c!=v.id:
                lat1, long1 = id_dict[c]
                child = Node(c, lat1, long1, graph_dict[c], v.g+graph_dict[v.id][c], calcd(lat1, long1, latEnd, longEnd))
                heapq.heappush(fringe, child)"""

def findMin():
    minLat = 100
    minLong = 100
    maxLat = 0
    maxLong = -80
    for key in id_dict:
        lat, long = id_dict[key]
        #print(lat + " " + long)
        if float(lat)<minLat:
            minLat = float(lat)
        if float(long)<minLong:
            minLong = float(long)
        if float(lat)>maxLat:
            maxLat = float(lat)
        if float(long)>maxLong:
            maxLong = float(long)
    return minLat, minLong, maxLat, maxLong

minLat, minLong, maxLat, maxLong = findMin()
#print(str(maxLong-minLong)+ " "+str(maxLat-minLat))
#input()
long_scale = 1000 / (maxLong-minLong)
lat_scale = 650 / (maxLat-minLat)


def drawMap():
    print("What is the start city: ")
    start = input()
    print("What is the end city: ")
    end = input()
    master = Tk()
    map = Canvas(master, width=1110, height=690)
    map.pack()
    map.configure(background = "black")
    for key in graph_dict:
        lat, long = id_dict[key]
        for v in graph_dict[key]:
            lat2, long2 = id_dict[v]
            map.create_line(1050-((maxLong-float(long))*long_scale), ((maxLat-float(lat))*lat_scale)+10, 1050-((maxLong-float(long2))*long_scale), ((maxLat-float(lat2))*lat_scale)+10, fill = "white")
    map.update()
    print(Astar(start, end, map))
    map.mainloop()

def Astar(state, goal, map):
    fringe = []
    visited = set()
    heapq.heapify(fringe)
    og_id = city_dict[state]
    lat, long = id_dict[city_dict[state]]
    latEnd, longEnd = id_dict[city_dict[goal]]
    heapq.heappush(fringe, (calcd(lat, long, latEnd, longEnd), 0,  city_dict[state], lat, long, "none", []))
    count = 0
    while len(fringe)!=0:
        gc, g, id, lat1, long1, parent, ancestors = heapq.heappop(fringe)
        #update line to red
        count += 1
        if parent != "none":
            plat, plong = id_dict[parent]
            map.create_line(1050-((maxLong-float(plong))*long_scale), ((maxLat-float(plat))*lat_scale)+10, 1050-((maxLong-float(long1))*long_scale), ((maxLat-float(lat1))*lat_scale)+10, fill = "red")
            if count%100==0:
                map.update()
        if id==city_dict[goal]:
            cur_lat, cur_long = lat1, long1
            temp = ancestors
            for p_id in temp:
                if p_id != og_id:
                    p_lat, p_long = id_dict[p_id]
                    map.create_line(1050 - ((maxLong - float(cur_long)) * long_scale), ((maxLat - float(cur_lat)) * lat_scale) + 10, 1050 - ((maxLong - float(p_long)) * long_scale), ((maxLat - float(p_lat)) * lat_scale) + 10, fill="yellow")
                    cur_lat, cur_long = p_lat, p_long
            map.update()
            return g
        if id in visited: continue
        visited.add(id)
        for c in graph_dict[id]:
            lat2, long2 = id_dict[c]
            #update line to green
            g1 = g+graph_dict[id][c]
            plat2, plong2 = id_dict[id]
            heapq.heappush(fringe, (g1+calcd(lat2, long2, latEnd, longEnd), g1, c, lat2, long2, id, [id]+ancestors))
            map.create_line(1050 - ((maxLong - float(plong2)) * long_scale), ((maxLat - float(plat2)) * lat_scale) + 10, 1050 - ((maxLong - float(long2)) * long_scale), ((maxLat - float(lat2)) * lat_scale) + 10, fill="green")
            if count % 100 == 0:
                map.update()

#print(Astar("Washington", "Merida"))
drawMap()
