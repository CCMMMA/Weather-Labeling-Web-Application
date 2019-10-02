"""This file contains the class ManageDB to manage every db operations"""

from pymongo import MongoClient
import sys
from bson.objectid import ObjectId


class ManageDB(object):
    def __init__(self):
        """This is constructor"""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client.MediStormSeekerDB
        except Exception as e:
            print("DB not ready " + str(e))
        self.db = db
        print("DB started, there are n. polygon: ",self.db.PolygonCollection.count())

    #---------------------POLYGON----------------------------------------

    def groupByClassPolygonDB(self,date1):
        """This method allows to ask the DB for the polygons's classes list grouped by classes"""
        count = self.db.PolygonCollection.find({"properties.dateStr": date1}).count()
        print(count)
        if count > 0:
            result = True
            cursorClassPolygon = self.db.PolygonCollection.aggregate(
                [{"$match" : { "properties.dateStr" : date1 }},{"$group": {"_id":{"name" : "$properties.name","dateStr":"$properties.dateStr"},"count": {"$sum": 1}}}])
            return result,cursorClassPolygon
        else:
            result = False
            cursorClassPolygon = None
            return result, cursorClassPolygon

    def insertPolygonDB(self,polygonGeoJson):
        """This method allows to add polygon"""
        count = self.db.PolygonCollection.find({"geometry.coordinates":polygonGeoJson["geometry"]["coordinates"],"properties.dateStr":polygonGeoJson["properties"]["dateStr"]})
        if count == 0:
            id = self.db.PolygonCollection.insert(polygonGeoJson)
            result = True
            return result,id
        else:
            result= False
            id = None
            return result,id

    def deletePolygonDB(self,id):
        """This method allows to remove polygon"""
        count = self.db.PolygonCollection.count({"_id":ObjectId(id)})
        print(count)
        if count == 1:
            result1 = self.db.PolygonCollection.delete_one({"_id":ObjectId(id)})
            print("Number polygon removed {}".format(result1.deleted_count))
            result = "correct"
            return result
        elif count == 0:
            print("polygon already removed")
            result = "empty"
            return result
        else:
            print("error: DB inconsistent")
            result = "inconsistent"
            return result

    def deletePolygonDBonUsername(self,username):
        """This method allows to remove all polygon of username"""
        result = self.db.PolygonCollection.remove({"properties.username":username})
        print("Number polygon removed {} di {}".format(result['n'],username))

    def listPolygonOnDateDB(self,date1):
        """This method allows to ask the DB for the polygons' list of specific date"""
        count = self.db.PolygonCollection.find({"properties.dateStr":date1}).count()
        if(count >= 1):
            result = True
            cursorListPolygon = self.db.PolygonCollection.find({"properties.dateStr":date1})
            return result,cursorListPolygon
        else:
            result = False
            cursorListPolygon = None
            return result,cursorListPolygon

    def checkLabelPolygononIdDB(self,id):
        count = self.db.PolygonCollection.find({"_id": ObjectId(id)}).count()
        if(count == 1):
            cursorPolygon = self.db.PolygonCollection.find_one({"_id": ObjectId(id)})
            result1 = "correct"
            return count,result1,cursorPolygon
        elif(count == 0):
            result1 = "empty"
            cursorPolygon = None
            return count, result1, cursorPolygon
        else:
            result1 = "inconsistent"
            cursorPolygon = None
            return count, result1, cursorPolygon

    def modifyLabelPolygonOnIdDB(self,id,name):
        """This method allows to modify polygon's label"""
        result1 = self.db.PolygonCollection.update_one({"_id":ObjectId(id)},{"$set":{"properties.name":name}})
        print("Number polygon modified {}".format(result1.modified_count))


    def getPolygonOnDate(self,date1):
        """This method allows to get a specific polygon"""
        count = self.db.PolygonCollection.find({"properties.dateStr":date1}).count()
        print("Numer Polygon of specific date",count)
        cursorPolygon = self.db.PolygonCollection.find({"properties.dateStr":date1})
        return cursorPolygon

    #------------------------POINT CLUSTER------------------------------------------

    def listClassClusterDB(self):
        """This method allows to ask the DB for clusters' classes list"""
        count = self.db.ClassClusterCollection.find().count()
        print("Number clusters' classes: ",count)
        if(count >= 1):
            result = True
            cursorListClassCluster = self.db.ClassClusterCollection.find()
            return result,cursorListClassCluster
        else:
            result = False
            cursorListClassCluster = None
            return result,cursorListClassCluster

    def listPointClusterOnDateDB(self,date1):
        """This method allows to ask the DB for clusters' points of specific date"""
        count = self.db.PointClusterCollection.find({"properties.dateStr":date1}).count()
        print("Number Point:",count)
        if(count >= 1):
            result = True
            cursorListPointCluster = self.db.PointClusterCollection.find({"properties.dateStr":date1})
            return result,cursorListPointCluster
        else:
            result = False
            cursorListPointCluster = None
            return result,cursorListPointCluster

    #---------------------------LABELING----------------------------------

    def countLabelDB(self):
        """This method gets the number of label"""
        count = self.db.LabelCollection.find().count()
        print("number Label:",count)
        return count

    def insertLabelDB(self, label):
        """This method insert a new label"""
        count = self.db.LabelCollection.find({"labelName":label["labelName"]}).count()
        if(count == 0):
            result = True
            id = self.db.LabelCollection.insert(label)
            return result,id
        else:
            result= False
            id = None
            return result,id


    def listLabelDB(self):
        """This method asks the DB the labels' list"""
        count = self.db.LabelCollection.find().count()
        #print("Number Label: ",count)
        if(count >= 1):
            result = True
            cursorListLabel = self.db.LabelCollection.find()
            return result,cursorListLabel
        else:
            result = False
            cursorListLabel = None
            return result,cursorListLabel
    #---------------------------LOGIN----------------------------------

    def loginDB(self,username):
        """This method checks userdata"""
        count = self.db.UserCollection.count({'username':username})
        if(count == 1):
            user = self.db.UserCollection.find_one({'username':username})
            return count,user
        else:
            user = None
            return count,user

    def createUserDB(self,name,surname,username,password):
        id = self.db.UserCollection.insert_one({'name':name,'surname':surname,'username':username,'password':password})
        return id

try:
    managedb = ManageDB()
except Exception as e:
    print("errore: DB not Ready")
    sys.exit(0)
