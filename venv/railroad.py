import pickle
from math import pi , acos , sin , cos

ID_DICT = {} #maps the id to (lat, long)
CITY_DICT = {}  #maps the cty name to id
GRAPH = {}

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

infile1 = open("rrNodes.txt", "r")
for val in infile1.readlines():
    thing = val.split(" ")
    ID_DICT[thing[0].strip()] = (thing[1].strip(), thing[2].strip())
infile2 = open("rrNodeCity.txt", "r")
for val in infile2.readlines():
    thing1 = val.split(" ")
    CITY_DICT[thing1[1].strip()]= thing1[0].strip()
infile3 = open("rrEdges.txt", "r")
for key in ID_DICT:
    GRAPH[key] = {}
for val in infile3.readlines():
    thing2 = val.split(" ")
    v1, v2 = thing2[0].strip(), thing2[1].strip()
    lat1, long1 = ID_DICT[v1]
    lat2, long2 = ID_DICT[v2]
    dist = calcd(lat1, long1, lat2, long2)
    GRAPH[v1][v2] = dist
    GRAPH[v2][v1] = dist

#print(GRAPH["4801193"]["4800797"])
myFile = open("data1", "wb")
myFile2 = open("data2", "wb")
myFile3 = open("data3", "wb")
pickle.dump(ID_DICT, myFile)
pickle.dump(CITY_DICT, myFile2)
pickle.dump(GRAPH, myFile3)

