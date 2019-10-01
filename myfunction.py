"""This file helps mainly to trasform data from db in JSON using MyTools class"""

from manager import *
import json

class MyTools(object):

    def modifyLabelJSON(self,cursorListLabel):
        list1 = []
        for label in cursorListLabel:
            list1.append(label)
        for x in range(0, len(list1)):
            list1[x]["_id"] = str(list1[x]["_id"])
            #print("id",list1[x]["_id"])
        cursorListLabel = json.dumps(list1)
        return cursorListLabel

    def modifyClassPolygonJSON(self,cursorListClassPolygon):
        list1 = []
        for polygon in cursorListClassPolygon:
            list1.append(polygon)
        for x in range(0, len(list1)):
            count1 = int(list1[x]["count"])
            list1[x]["count"] = count1
            #print("count class polygon",list1[x]["_id"]["name"],count1)
            data1 = list1[x]["_id"]["dateStr"]
            list1[x]["_id"]["dateStr"] = data1.strftime('%Y%m%dZ%H%M')
            #print("Class polygon date")
            #print(list1[x]["_id"]["dateStr"])
        cursorListClassPolygon = json.dumps(list1)
        return cursorListClassPolygon

    def modifyPolygonJSON(self,cursorListPolygon):
        list1=[]
        for polygon in cursorListPolygon:
            list1.append(polygon)
        for x in range(0,len(list1)):
            list1[x]["_id"] = str(list1[x]["_id"])
            #print(list1[x]["_id"])
            list1[x]["properties"]["idDB"] = str(list1[x]["_id"])
            #print("pr",list1[x]["properties"]["idDB"])
            data1 = list1[x]["properties"]["dateStr"]
            list1[x]["properties"]["dateStr"] = data1.strftime('%Y%m%dZ%H%M')
            #print(list1[x]["properties"]["dateStr"])
        cursorListPolygon = json.dumps(list1)
        return cursorListPolygon

    def modifyClassClusterJSON(self, cursorListClassCluster):
        list1 = []
        for classCluster in cursorListClassCluster:
            list1.append(classCluster)
        for x in range(0, len(list1)):
            list1[x]["_id"] = str(list1[x]["_id"])
            #print(list1[x]["_id"])
        cursorListClassCluster = json.dumps(list1)
        return cursorListClassCluster

    def modifyPointClusterJSON(self, cursorListPointCluster):
        list1 = []
        for point in cursorListPointCluster:
            list1.append(point)
        for x in range(0, len(list1)):
            list1[x]["_id"] = str(list1[x]["_id"])
            #print(list1[x]["_id"])
            list1[x]["properties"]["idDB"] = str(list1[x]["_id"])
            #print("pr", list1[x]["properties"]["idDB"])
            data1 = list1[x]["properties"]["dateStr"]
            list1[x]["properties"]["dateStr"] = data1.strftime('%Y%m%dZ%H%M')
            #print(list1[x]["properties"]["dateStr"])
        cursorListPointCluster = json.dumps(list1)
        return cursorListPointCluster

    def getPolygon(self,date1,managedb):
        polygons = []
        typePolygons = []
        print("Richiesta Polygon in base a datetime:",date1)
        try:
            cursorPolygon = managedb.getPolygonOnDate(date1)
            for polygon in cursorPolygon:
                coords = []
                #print("polygon DB")
                #print(polygon)
                #print(polygon["properties"]["name"].upper())
                #print(polygon["geometry"]["coordinates"])
                #print("lunghezza",len(polygon["geometry"]["coordinates"][0]))
                for i in range(0,len(polygon["geometry"]["coordinates"][0])):
                    print("lng:",polygon["geometry"]["coordinates"][0][i][0],"lat:",polygon["geometry"]["coordinates"][0][i][1])
                    coords.append(tuple((polygon["geometry"]["coordinates"][0][i][0],polygon["geometry"]["coordinates"][0][i][1])))
                typePolygons.append(self.assignTypeStorm(polygon))
                #print(typePolygons[-1])
                #print("geometric polygon")
                #print(coords)
                poly = Polygon(coords)
                #print(poly)
                polygons.append(poly)
            #print(len(polygons),len(typePolygons))
            return polygons,typePolygons
        except Exception as e:
            print("exception error DB",e)
            return None,None

    def assignTypeStorm(self,polygon):
        name = polygon["properties"]["name"].upper()
        if name == "MEDICANE":
            return 1
        if name == "STORM":
            return 2
        if name == "THUNDERSTORM":
            return 3



mytools = MyTools()
