import requests
import math
import csv


dist_mat_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
snap_to_roads = "https://roads.googleapis.com/v1/snapToRoads?parameters&key=YOUR_API_KEY"

class node:
    # Initializer / Instance Attributes
    def __init__(self, name):
        self.name = name
        self.dest = []
        self.dist = 1000000

    def getDestNames(self):
        dest_names = []
        for i in self.dest:
            dest_names.append(i[0].name)
        return dest_names

    def getDests(self):
        dest_names = []
        for i in self.dest:
            dest_names.append([i[0].name,i[1]])
        return dest_names

    def getDestsDist(self):
        distance = 0
        for i in self.dest:
            distance += i[1]
        return distance

    def getStart(self, nodes):
        for i in nodes:
            if i.dist == 0:
                return i.name
        return "error"

    def dijkestra(self, nodes, start):
        start.dist = 0
        setNodes = [start]
        unSetNodes = nodes
        #unSetNodes.remove(start)
        name = None
        names = []
        totalDist = 0
        while len(unSetNodes) != 0:
            nodesToMaybeSet = []
            for k in setNodes:
                for l in k.getDests():
                    nodesToMaybeSet.append(l)
            for k in nodesToMaybeSet:
                for l in setNodes:
                    if k[0] == l.name:
                        nodesToMaybeSet.remove(k)
            thisDistance = 999999
            nodeToSet = start
            for i in nodesToMaybeSet:
                    if i[1] < thisDistance and i[0] not in names:
                        for j in nodes:
                            if j.name == i[0]:
                                name = i[0]
                                nodeToSet = j
                                thisDistance = i[1]
            nodeToSet.dist = thisDistance
            totalDist += thisDistance
            names.append(name)
            setNodes.append(nodeToSet)
            for i in unSetNodes:
                if i.name == nodeToSet.name:
                    unSetNodes.remove(i)
                    break
        if len(unSetNodes) != 0:
            setNodes.append(unSetNodes[0])
        return totalDist


def interpret_location_to_nodes(snappedpoints):
    last_lat = 0
    last_long = 0
    this_lat = 0
    this_long = 0
    origin = node("start")
    node2 = node("")

    this_node = origin
    street_name = "default"

    found_in_database = False

    getLat = False
    getLong = False
    snappedpoints = "".join(map(chr, snappedpoints))

    for i in snappedpoints.splitlines():

        if getLat == True and  getLong == True:
            #street name = ( thislat this) to get street name
            lat = str(this_lat) + ","+str(this_long)
            streetName = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "&key=AIzaSyDX743WS4HcdXdYBSm3fpsiVGlGcJSEdLE"
            streetNameResponce = requests.get(streetName)
            streetNameContent = streetNameResponce.content
            streetNameContent = "".join(map(chr, streetNameContent))
            long_nameCounter = 0
            actualStreetName = ""
            for i in streetNameContent.splitlines():
                if "long_name" in i:
                    long_nameCounter += 1
                if long_nameCounter == 2:
                    actualStreetName = i[30:len(i) - 2]
                    break
            #look up street in database, if found flip found in database flag
            with open('Existing_Bike_Network@.csv', newline='') as csvfile:
                fileReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for i in fileReader:
                    if actualStreetName in i:
                        found_in_database = True
                        break
            ################
            dist = math.sqrt(pow(this_lat-last_lat,2)+ pow(this_long-last_long,2))
            if  found_in_database == True:
                dist = dist * .80

            node2 = node(actualStreetName)
            origin.dest.append([node2,dist])
            this_node = node2

            getLat = False
            getLong = False
            last_lat = this_lat
            last_long = this_long
            found_in_database = False




        elif getLong == True:
            this_long = i[21:len(i)]
            this_long = float(this_long)
            getLat = True

        elif getLat == True:
            this_lat = i[20:len(i) - 1]
            this_lat = float(this_lat)
            getLat = False
            getLong = True

        elif "location" in i:
            getLat = True

    return origin

def getRoutes(start, end):
    i = 1
    route = []
    #if end is greater than start, need to add to start to get to end
    if start[0] - end[0] < 0:
        x = False
    else:
        x = True
    if start[1] - end[1] < 0:
        y = False
    else:
        y = True
    j = 0
    while j < 3:
     route.append([])
     if x is False and y is False:
        xx = end[0] - start[0]
        xx = xx / 20
        yy = end[1] - start[1]
        yy = yy / 20
        while i <= 20:
            if j is 0:
                route[j].append([start[0] + xx * i, start[1] + yy * i])
            elif j % 2 is 0:
                route[j].append([start[0] + xx * i + xx * j / 2, start[1] + yy * i + yy * j / 2])
            elif j % 2 is 1:
                route[j].append([start[0] + xx * i + xx * -(j - 1) / 2, start[1] + yy * i + yy * -(j - 1) / 2])
            i += 1

     elif x is False and y is True:
        xx = end[0] - start[0]
        xx = xx / 20
        yy = start[1] - end[1]
        yy = yy / 20
        while i < 20:
            if j is 0:
             route[j].append([start[0]+xx*i,start[1]-yy*i])
            elif j % 2 is 0:
                route[j].append([start[0] + xx * i + xx * j/2, start[1] - yy * i - yy * j/2])
            elif j % 2 is 1:
                route[j].append([start[0] + xx * i + xx * -(j-1)/ 2, start[1] - yy * i - yy * -(j-1)/ 2])
            i += 1

     elif x is True and y is False:
        xx = start[0] - end[0]
        xx = xx / 20
        yy = end[1] - start[1]
        yy = yy / 20
        while i <= 5:
            if j is 20:
             route[j].append([start[0]-xx*i,start[1]+yy*i])
            elif j % 2 is 0:
                route[j].append([start[0] - xx * i - xx * j/2, start[1] + yy * i + yy * j/2])
            elif j % 2 is 1:
                route[j].append([start[0] - xx * i - xx * -(j-1)/ 2, start[1] + yy * i + yy * -(j-1)/ 2])
            i += 1
     elif x is True and y is True:
        xx = start[0] - end[0]
        xx = xx / 20
        yy = start[1] - end[1]
        yy = yy / 20
        while i <= 20:
            if j is 0:
             route[j].append([start[0]-xx*i,start[1]-yy*i])
            elif j % 2 is 0:
                route[j].append([start[0] - xx * i - xx * j/2, start[1] - yy * i - yy * j/2])
            elif j % 2 is 1:
                route[j].append([start[0] - xx * i - xx * -(j-1)/ 2, start[1] - yy * i - yy * -(j-1)/ 2])
            i += 1
     route[j].append(end)
     j += 1
     i = 0
    return route

def interprateToPath(route):
    path = ""
    for i in route:
        path += str(i[0]) + "," + str(i[1]) + "|"
    path = path[0:len(path)-1]
    return path


#main

#these two values need to come from the front end, these are just testing values
start = [42.336937,-71.093587]
end = [42.379897,-71.128295]


safestDistance = 100000000
safestRoute = []

routes = [getRoutes(start, end)]
routes = routes[0]
for i in routes:
    path = interprateToPath(i)
    snapWebzone = "https://roads.googleapis.com/v1/snapToRoads?path="+path+"&interpolate=true&key=AIzaSyDX743WS4HcdXdYBSm3fpsiVGlGcJSEdLE"

    responce = requests.get(snapWebzone)
    resp_cont = responce.content
    a = interpret_location_to_nodes(resp_cont)
    b = a.getDestsDist()
    if b < safestDistance:
        b = safestDistance
        safestRoute = snapWebzone
print(safestRoute)