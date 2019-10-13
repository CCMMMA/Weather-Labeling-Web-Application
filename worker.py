"""This file contains 2 functions to multiprocessor analysis"""

from myfunction import *
from netCDF4 import Dataset
import urlparse
import csv
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as po
from matplotlib.collections import PatchCollection
from shutil import copyfile

def workerUrl(username,url):
    """This method analyzes which point of online netCDF belong to polygon or not; then it create a csv file
    where it storage every info"""
    print("------------------------------------------------------------------------------------")
    print("Analysis online netCDF file")
    count = 0
    managedb = ManageDB()
    mytool = MyTools()
    pre, ext = os.path.splitext(os.path.basename(urlparse.urlsplit(url).path))
    csvfile = pre + ".csv"
    print(url)
    print(csvfile)
    if "_d01_" in csvfile:
        print("resolution d01")
        resolution = "d01"
    elif "_d02_" in csvfile:
        print("resolution d02")
        resolution = "d02"
    elif "_d03_" in csvfile:
        print("resolution d03")
        resolution = "d03"
    else:
        sys.exit(0)
    dirName = "static/user_files/" + username
    print(dirName)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")
    dirTemp = dirName + "/temp"
    if not os.path.exists(dirTemp):
        os.mkdir(dirTemp)
        print("Directory ", dirTemp, " Created ")
    else:
        print("Directory ", dirTemp, " already exists")
    pathCSVFile = dirName + "/temp/" + csvfile
    pathCSVFileDef = dirName + "/" + csvfile
    print(pathCSVFile)
    print(pathCSVFileDef)
    with open(pathCSVFile, "w") as f:
        fieldnames = ["j","i","T2C","SLP", "WSPD10","WDIR10","RH2","UH","MCAPE","TC500","TC850","GPH500", "GPH850","CLDFRA_TOTAL","U10M","V10M","DELTA_WSPD10", "DELTA_WDIR10","DELTA_RAIN","resolution", "type"]
        writer1 = csv.DictWriter(f,extrasaction='ignore', fieldnames=fieldnames)
        writer1.writeheader()
        pointX = []
        pointY = []
        polygonX = []
        polygonY = []
        nc = Dataset(url, "r")
        hours1 = int(nc.variables["time"][0])
        date1 = datetime(1900, 1, 1) + timedelta(hours=hours1)
        print("date of file :",date1)
        count1 = 0
        polygons, typePolygons = mytool.getPolygon(date1,managedb)
        if polygons == None:
            raise ValueError('problem with DB')
        if (len(polygons) >0):
            fig, ax = plt.subplots()
            patches = []
            # color = []
            # c = np.random.random((1, 3)).tolist()[0]

            for i in range(0, len(polygons)):
                print(polygons[i])
                x, y = polygons[i].exterior.xy
                po1 = po(zip(x, y))
                patches.append(po1)
            p = PatchCollection(patches, edgecolors=(0, 0, 0, 1), linewidths=1, alpha=0.5)
            ax.add_collection(p)
            #print(len(nc.dimensions['longitude']))
            #print(len(nc.dimensions['latitude']))
            for i in range(0, len(nc.dimensions['longitude'])):
                for j in range(0, len(nc.dimensions['latitude'])):
                    count1 = count1 + 1
                    # print("lng: {} | lat: {}".format(nc.variables["longitude"][i],nc.variables["latitude"][j]))
                    lng = nc.variables["longitude"][i]
                    lat = nc.variables["latitude"][j]
                    pt = Point(lng, lat)
                    flag = False
                    for k in range(0, len(polygons)):
                        if (polygons[k].contains(pt)):
                            flag = True
                            count = count + 1
                            pointX.append(lng)
                            pointY.append(lat)
                            print("count {}) lng: {} | lat: {} | type: {}".format(count, nc.variables["longitude"][i],
                                                                                  nc.variables["latitude"][j],
                                                                                  typePolygons[k]))
                            #writer1.writerow({"type": typePolygons[k]})
                            writer1.writerow({"j": j,
                                              "i": i,
                                              "T2C": nc.variables["T2C"][0][j][i],
                                              "SLP": nc.variables["SLP"][0][j][i],
                                              "WSPD10": nc.variables["WSPD10"][0][j][i],
                                              "WDIR10": nc.variables["WDIR10"][0][j][i],
                                              "RH2": nc.variables["RH2"][0][j][i],
                                              "UH": nc.variables["UH"][0][j][i],
                                              "MCAPE": nc.variables["MCAPE"][0][j][i],
                                              "TC500": nc.variables["TC500"][0][j][i],
                                              "TC850": nc.variables["TC850"][0][j][i],
                                              "GPH500": nc.variables["GPH500"][0][j][i],
                                              "GPH850": nc.variables["GPH850"][0][j][i],
                                              "CLDFRA_TOTAL": nc.variables["CLDFRA_TOTAL"][0][j][i],
                                              "U10M": nc.variables["U10M"][0][j][i],
                                              "V10M": nc.variables["V10M"][0][j][i],
                                              "DELTA_WSPD10": nc.variables["DELTA_WSPD10"][0][j][i],
                                              "DELTA_WDIR10": nc.variables["DELTA_WDIR10"][0][j][i],
                                              "DELTA_RAIN": nc.variables["DELTA_RAIN"][0][j][i],
                                              "resolution":resolution,
                                              "type": typePolygons[k]})

                    if (not flag):
                        #writer1.writerow({"type": 0})
                        writer1.writerow({"j": j,
                                          "i": i,
                                          "T2C": nc.variables["T2C"][0][j][i],
                                          "SLP": nc.variables["SLP"][0][j][i],
                                          "WSPD10": nc.variables["WSPD10"][0][j][i],
                                          "WDIR10": nc.variables["WDIR10"][0][j][i],
                                          "RH2": nc.variables["RH2"][0][j][i],
                                          "UH": nc.variables["UH"][0][j][i],
                                          "MCAPE": nc.variables["MCAPE"][0][j][i],
                                          "TC500": nc.variables["TC500"][0][j][i],
                                          "TC850": nc.variables["TC850"][0][j][i],
                                          "GPH500": nc.variables["GPH500"][0][j][i],
                                          "GPH850": nc.variables["GPH850"][0][j][i],
                                          "CLDFRA_TOTAL": nc.variables["CLDFRA_TOTAL"][0][j][i],
                                          "U10M": nc.variables["U10M"][0][j][i],
                                          "V10M": nc.variables["V10M"][0][j][i],
                                          "DELTA_WSPD10": nc.variables["DELTA_WSPD10"][0][j][i],
                                          "DELTA_WDIR10": nc.variables["DELTA_WDIR10"][0][j][i],
                                          "DELTA_RAIN": nc.variables["DELTA_RAIN"][0][j][i],
                                          "resolution":resolution,
                                          "type": 0})

            print("N. point",count1)
            #plt.plot(pointX, pointY, 'b,')
            #plt.show()

        else:
            print("No polygons")
            #print(len(nc.variables['longitude']))
            #print(len(nc.variables['latitude']))
            for i in range(0, len(nc.dimensions['longitude'])):
                for j in range(0, len(nc.dimensions['latitude'])):
                    count1 = count1 + 1
                    #writer1.writerow({"type": 0})
                    writer1.writerow({"j": j,
                                      "i": i,
                                      "T2C": nc.variables["T2C"][0][j][i],
                                      "SLP": nc.variables["SLP"][0][j][i],
                                      "WSPD10": nc.variables["WSPD10"][0][j][i],
                                      "WDIR10": nc.variables["WDIR10"][0][j][i],
                                      "RH2": nc.variables["RH2"][0][j][i],
                                      "UH": nc.variables["UH"][0][j][i],
                                      "MCAPE": nc.variables["MCAPE"][0][j][i],
                                      "TC500": nc.variables["TC500"][0][j][i],
                                      "TC850": nc.variables["TC850"][0][j][i],
                                      "GPH500": nc.variables["GPH500"][0][j][i],
                                      "GPH850": nc.variables["GPH850"][0][j][i],
                                      "CLDFRA_TOTAL": nc.variables["CLDFRA_TOTAL"][0][j][i],
                                      "U10M": nc.variables["U10M"][0][j][i],
                                      "V10M": nc.variables["V10M"][0][j][i],
                                      "DELTA_WSPD10": nc.variables["DELTA_WSPD10"][0][j][i],
                                      "DELTA_WDIR10": nc.variables["DELTA_WDIR10"][0][j][i],
                                      "DELTA_RAIN": nc.variables["DELTA_RAIN"][0][j][i],
                                      "resolution":resolution,
                                      "type": 0})
            print("N. point",count1)
        nc.close()
    managedb.client.close()
    copyfile(pathCSVFile, pathCSVFileDef)
    if os.path.exists( pathCSVFile):
        os.remove(pathCSVFile)
    else:
        print("The file does not exist")
    return True

def workerNcfile(username,ncfile):
    """This method analyzes which point of local netCDF  belong to polygon or not; then it create a csv file
        where it storage every info"""
    print("------------------------------------------------------------------------------------")
    print("Analysis local netCDF file")
    print(ncfile)
    count = 0
    managedb = ManageDB()
    mytool = MyTools()

    pre, ext = os.path.splitext(os.path.basename(urlparse.urlsplit(ncfile).path))
    csvfile = pre + ".csv"
    print(csvfile)

    if "_d01_" in csvfile:
        print("resolution d01")
        resolution = "d01"
    elif "_d02_" in csvfile:
        print("resolution d02")
        resolution = "d02"
    elif "_d03_" in csvfile:
        print("resolution d03")
        resolution = "d03"
    else:
        sys.exit(0)

    dirName = "static/user_files/" + username
    print(dirName)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")
    pathCSVFile = dirName + "/temp/" + csvfile
    pathCSVFileDef = dirName + "/" + csvfile
    dirTemp = dirName + "/temp"
    if not os.path.exists(dirTemp):
        os.mkdir(dirTemp)
        print("Directory ", dirTemp, " Created ")
    else:
        print("Directory ", dirTemp, " already exists")
    print(pathCSVFile)
    print(pathCSVFileDef)
    with open(pathCSVFile, "w") as f:
        # fieldnames = ["longitude", "latitude", "HOURLY_SWE", "DELTA_RAIN", "DAILY_RAIN", "T2C", "RH2", "UH",
        #               "MCAPE", "TC500", "TC850", "GPH500", "GPH850", "SLP", "CLDFRA_TOTAL", "U10M", "V10M", "WSPD10",
        #               "WDIR10", "DELTA_WSPD10", "DELTA_WDIR10", "resolution", "type"]
        fieldnames = ["j","i","T2C","SLP", "WSPD10","WDIR10","RH2","UH","MCAPE","TC500","TC850","GPH500", "GPH850","CLDFRA_TOTAL","U10M","V10M","DELTA_WSPD10", "DELTA_WDIR10","DELTA_RAIN","resolution", "type"]
        writer1 = csv.DictWriter(f, extrasaction='ignore',fieldnames=fieldnames)
        writer1.writeheader()
        pointX = []
        pointY = []
        polygonX = []
        polygonY = []
        nc = Dataset(ncfile, "r")
        hours1 = int(nc.variables["time"][0])
        date1 = datetime(1900, 1, 1) + timedelta(hours=hours1)
        print("date of file:",date1)
        count1 = 0
        polygons, typePolygons = mytool.getPolygon(date1,managedb)
        if (len(polygons) != 0 and polygons != None):
            print("Number of polygon n.",len(polygons))
            fig, ax = plt.subplots()
            patches = []
            # color = []
            # c = np.random.random((1, 3)).tolist()[0]

            for i in range(0, len(polygons)):
                #print(polygons[i])
                x, y = polygons[i].exterior.xy
                po1 = po(zip(x, y))
                patches.append(po1)
            p = PatchCollection(patches, edgecolors=(0, 0, 0, 1), linewidths=1, alpha=0.5)
            ax.add_collection(p)
            #print("longitude n.",len(nc.dimensions['longitude']))
            #print("latitude n.",len(nc.dimensions['latitude']))
            for i in range(0, len(nc.dimensions['longitude'])):
                for j in range(0, len(nc.dimensions['latitude'])):
                    count1 = count1 + 1
                    #print("lng: {} | lat: {}".format(nc.variables["longitude"][i],nc.variables["latitude"][j]))
                    lng = nc.variables["longitude"][i]
                    lat = nc.variables["latitude"][j]
                    pt = Point(lng, lat)
                    flag = False
                    for k in range(0, len(polygons)):
                        if (polygons[k].contains(pt)):
                            flag = True
                            count = count + 1
                            pointX.append(lng)
                            pointY.append(lat)
                            print("count {}) lng: {} | lat: {} | type: {}".format(count, nc.variables["longitude"][i],
                                                                                  nc.variables["latitude"][j],
                                                                                  typePolygons[k]))
                            #writer1.writerow({"type": typePolygons[k]})
                            writer1.writerow({"j": j,
                                              "i": i,
                                              "T2C": nc.variables["T2C"][0][j][i],
                                              "SLP": nc.variables["SLP"][0][j][i],
                                              "WSPD10": nc.variables["WSPD10"][0][j][i],
                                              "WDIR10": nc.variables["WDIR10"][0][j][i],
                                              "RH2": nc.variables["RH2"][0][j][i],
                                              "UH": nc.variables["UH"][0][j][i],
                                              "MCAPE": nc.variables["MCAPE"][0][j][i],
                                              "TC500": nc.variables["TC500"][0][j][i],
                                              "TC850": nc.variables["TC850"][0][j][i],
                                              "GPH500": nc.variables["GPH500"][0][j][i],
                                              "GPH850": nc.variables["GPH850"][0][j][i],
                                              "CLDFRA_TOTAL": nc.variables["CLDFRA_TOTAL"][0][j][i],
                                              "U10M": nc.variables["U10M"][0][j][i],
                                              "V10M": nc.variables["V10M"][0][j][i],
                                              "DELTA_WSPD10": nc.variables["DELTA_WSPD10"][0][j][i],
                                              "DELTA_WDIR10": nc.variables["DELTA_WDIR10"][0][j][i],
                                              "DELTA_RAIN": nc.variables["DELTA_RAIN"][0][j][i],
                                              "resolution":resolution,
                                              "type": typePolygons[k]})

                    if (not flag):
                        #writer1.writerow({"type": 0})
                        writer1.writerow({"j": j,
                                          "i": i,
                                          "T2C": nc.variables["T2C"][0][j][i],
                                          "SLP": nc.variables["SLP"][0][j][i],
                                          "WSPD10": nc.variables["WSPD10"][0][j][i],
                                          "WDIR10": nc.variables["WDIR10"][0][j][i],
                                          "RH2": nc.variables["RH2"][0][j][i],
                                          "UH": nc.variables["UH"][0][j][i],
                                          "MCAPE": nc.variables["MCAPE"][0][j][i],
                                          "TC500": nc.variables["TC500"][0][j][i],
                                          "TC850": nc.variables["TC850"][0][j][i],
                                          "GPH500": nc.variables["GPH500"][0][j][i],
                                          "GPH850": nc.variables["GPH850"][0][j][i],
                                          "CLDFRA_TOTAL": nc.variables["CLDFRA_TOTAL"][0][j][i],
                                          "U10M": nc.variables["U10M"][0][j][i],
                                          "V10M": nc.variables["V10M"][0][j][i],
                                          "DELTA_WSPD10": nc.variables["DELTA_WSPD10"][0][j][i],
                                          "DELTA_WDIR10": nc.variables["DELTA_WDIR10"][0][j][i],
                                          "DELTA_RAIN": nc.variables["DELTA_RAIN"][0][j][i],
                                          "resolution":resolution,
                                          "type": 0})

            print("N. point",count1)
            #plt.plot(pointX, pointY, 'b,')
            #plt.show()

        else:
            print("No polygon")
            #print(len(nc.variables['longitude']))
            #print(len(nc.variables['latitude']))
            for i in range(0, len(nc.dimensions['longitude'])):
                for j in range(0, len(nc.dimensions['latitude'])):
                    count1 = count1 + 1
                    #writer1.writerow({"type": 0})
                    writer1.writerow({"j": j,
                                      "i": i,
                                      "T2C": nc.variables["T2C"][0][j][i],
                                      "SLP": nc.variables["SLP"][0][j][i],
                                      "WSPD10": nc.variables["WSPD10"][0][j][i],
                                      "WDIR10": nc.variables["WDIR10"][0][j][i],
                                      "RH2": nc.variables["RH2"][0][j][i],
                                      "UH": nc.variables["UH"][0][j][i],
                                      "MCAPE": nc.variables["MCAPE"][0][j][i],
                                      "TC500": nc.variables["TC500"][0][j][i],
                                      "TC850": nc.variables["TC850"][0][j][i],
                                      "GPH500": nc.variables["GPH500"][0][j][i],
                                      "GPH850": nc.variables["GPH850"][0][j][i],
                                      "CLDFRA_TOTAL": nc.variables["CLDFRA_TOTAL"][0][j][i],
                                      "U10M": nc.variables["U10M"][0][j][i],
                                      "V10M": nc.variables["V10M"][0][j][i],
                                      "DELTA_WSPD10": nc.variables["DELTA_WSPD10"][0][j][i],
                                      "DELTA_WDIR10": nc.variables["DELTA_WDIR10"][0][j][i],
                                      "DELTA_RAIN": nc.variables["DELTA_RAIN"][0][j][i],
                                      "resolution":resolution,
                                      "type": 0})
            print("N. point",count1)
        nc.close()
    managedb.client.close()
    copyfile(pathCSVFile, pathCSVFileDef)
    if os.path.exists(pathCSVFile):
        os.remove(pathCSVFile)
    else:
        print("The file does not exist")
    return True
