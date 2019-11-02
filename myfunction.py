"""This file helps mainly to trasform data from db in JSON using MyTools class"""

from manager import *
import json
from datetime import timedelta,datetime
from netCDF4 import Dataset
from shapely.geometry import Polygon,Point

#insert your path where there are netCDF file
localPath = "<insert your path where there are netCDF file>"

url = "http://193.205.230.6:8080/opendap/hyrax/opendap/wrf5"

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

    #Manage Point in Polygon's algorithm-------------------------------------------------------

    def validityCheckDB(self,managedb):
        """This method allows:
        A) to check if DB was actived
        B) to check if labels existed
        C) to check if polygons existed
        D) to check if every polygon had its label
        """
        try:
            result, cursorLabelCollection = managedb.listLabelDB()
            if result == False:
                print("Error: there aren't label")
                return result
            result1, cursorClassPolygon = managedb.groupByClassPolygonDBNoDate()
            if result1 == False:
                print("Error: there aren't polygon")
                return result
            for polygon in cursorClassPolygon:
                # print(polygon)
                if (polygon["_id"]["name"] == ""):
                    print("----------------------------------------")
                    print("Error: there are polygons without its label")
                    print("list of polygon without its label")
                    name = polygon["_id"]["name"]
                    result3,cursorPolygon = managedb.getPolygonOnName(name)
                    if result3 == False:
                        return result3
                    else:
                        for pol in cursorPolygon:
                            print("id", pol["_id"], "datetime", pol["properties"]["dateStr"])
                        result4 = False
                        return result4
            return True
        except Exception as e:
            print("error DB:",str(e))
            result5 = False
            return result5

    def getUrls(self,rStart,rEnd,yStart,mStart,dStart,hStart,yEnd,mEnd,dEnd,hEnd):
        """This method callows to seek netCDF in local/online of specific range of time"""
        urls = []
        ncfiles = []
        for r in range(rStart,rEnd+1):
            r1 = "d0" + str(r)
            sdate = datetime(yStart,mStart,dStart,hStart)
            edate = datetime(yEnd,mEnd,dEnd,hEnd)
            delta = int((edate-sdate).total_seconds()/3600)
            for i in range(delta+1):
                tempDate = sdate + timedelta(hours=i)
                time1 = tempDate.strftime("%Y%m%dZ%H%M")
                year = tempDate.strftime("%Y")
                month = tempDate.strftime("%m")
                day = tempDate.strftime("%d")
                url1 = url + "/" + r1 + "/" + "archive" + "/" + year + "/" + month + "/" + day + "/" + "wrf5_" + r1 + "_" + time1 + ".nc"
                fname = "wrf5_"+ r1 + "_" + time1 + ".nc"
                print(url1)
                print(fname)
                #http://193.205.230.6:8080/opendap/hyrax/opendap/wrf5/d01/archive/2018/08/01/wrf5_d01_20180801Z0000.nc
                #http://193.205.230.6:8080/opendap/hyrax/opendap/wrf5/d01/archive/2018/10/29/wrf5_d01_20181029Z0200.nc

                localPath1 = localPath + "/" + r1
                localPath2 = localPath1 + "/" + fname
                print(localPath2)
                if not os.path.isfile(localPath2):
                    print("file isn't in local: " + fname)
                    try:
                        nc = Dataset(url1)
                        nc.close()
                        urls.append(url1)
                        print("file is online: " + fname)
                    except Exception as e:
                        print("file isn't online")
                else:
                    print("file is in local: " + fname)
                    ncfiles.append(localPath2)
        return ncfiles,urls

    def getPolygon(self, date1, managedb):
        """this method gets the polygons of specific date"""
        polygons = []
        typePolygons = []
        try:
            count,cursorPolygon = managedb.getPolygonOnDate(date1)
            if count > 0:
                for polygon in cursorPolygon:
                    coords = []
                    print("Info of polygon:")
                    print(polygon)
                    # print(polygon["properties"]["name"].upper())
                    # print(polygon["geometry"]["coordinates"])
                    # print("lunghezza",len(polygon["geometry"]["coordinates"][0]))
                    for i in range(0, len(polygon["geometry"]["coordinates"][0])):
                        # print("lng:",polygon["geometry"]["coordinates"][0][i][0],"lat:",polygon["geometry"]["coordinates"][0][i][1])
                        coords.append(tuple(
                            (polygon["geometry"]["coordinates"][0][i][0], polygon["geometry"]["coordinates"][0][i][1])))
                    result,labelId = self.assignTypeStorm(managedb, polygon)
                    if result == False:
                        polygons= None
                        typePolygons = None
                        return polygons, typePolygons
                    else:
                        typePolygons.append(labelId)
                    print("class of polygon:", typePolygons[-1])
                    # print("geometric polygon")
                    # print(coords)
                    poly = Polygon(coords)
                    # print(poly)
                    polygons.append(poly)
                # print("Number of polygon saved on DB n.",len(polygons))
                return polygons, typePolygons
            else:
                return polygons, typePolygons
        except Exception as e:
            print("Error DB:", str(e))
            polygons = None
            typePolygons = None
            return polygons, typePolygons

    def assignTypeStorm(self, managedb, polygon):
        try:
            result, cursorLabelCollection1 = managedb.listLabelDB()
            if result == False:
                print("Error: there aren't labels")
                labelId = None
                return result,labelId
            name = polygon["properties"]["name"].upper()
            for label in cursorLabelCollection1:
                name1 = label["labelName"].upper()
                # print(name,name1)
                if (name == name1):
                    # print("assignment",name,name1)
                    labelId = label["labelId"]
                    # print("type",labelId)
                    result = True
                    return result,labelId
        except Exception as e:
            print("exception", str(e))
            result = False
            labelId = None
            return result, labelId

mytools = MyTools()
