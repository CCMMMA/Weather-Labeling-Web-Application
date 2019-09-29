"""This file allows to manage the web site and web page server-side"""

from myfunction import *
import datetime
from flask_user import roles_required
import os

#these values allows to insert the default labels
flag = False
count12 = 0

app = Flask(__name__)
app.secret_key = 'Your_secret_string'
admin = Admin(app,"Admin's Area")
admin.add_view(UserView(managedb.db.UserCollection,"Manage Users"))

@app.route("/")
def index():
    """This function allows to execute the login; if user is already logged in , he will able to access the main page"""
    if "logged_in" in session and session["logged_in"] == True:
        print("User login",session["username"])
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route("/main")
def main():
    """This function allows to access the main page"""
    if "logged_in" in session and session["logged_in"] == True:
        #print("User login",session["username"])
        return render_template('main.html')
    return redirect(url_for('index'))

@app.route("/home")
def home():
    """This function allows to execute the login; if user is already logged in , he will able to access the main page"""
    if "logged_in" in session and session["logged_in"] == True:
        print("User login",session["username"])
        return render_template('/admin/index.html')
    return render_template('index.html')


@app.route("/registration")
def registration():
    """This function allows to register our account"""
    if "logged_in" in session and session["logged_in"] == True:
        return redirect(url_for('main'))
    return render_template('registration.html')

@app.route('/createUser',methods=["GET","POST"])
def createUser():
    """This function adds new user"""
    if "logged_in" in session and session["logged_in"] == True:
        return redirect(url_for('main'))
    if request.method == "POST":
        print("Create new user")
        name = request.form["name"]
        surname = request.form["surname"]
        username = request.form["username"]
        password = request.form["password"]
        pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            id = managedb.createUserDB(name,surname,username,pass_hash)
            session["registration"] = True
            return redirect(url_for("index"))
        except Exception as e:
            print("Error DB:",str(e))
            session["registration"] = False
            return redirect(url_for("registration"))

@app.route("/logout")
def logout():
    """This function allows to execute the logout"""
    if "logged_in" not in session or session["logged_in"] != True:
        print("Unregistered user")
    print("Logout",session["username"])
    session.clear()
    return redirect(url_for('index'))

@app.route('/login',methods=["GET","POST"])
def login():
    """This function allows to execute the login"""
    if request.method == "POST":
        print("Check login DB")
        username = request.form["username"]
        password = request.form["password"]
        try:
            count,userDB = managedb.loginDB(username)
            pass_hash = userDB["password"]
            if(count == 0):
                session["logged_in"] = False
                print("login failed")
                return redirect(url_for('index'))
            else:
                if (check_password_hash(pass_hash, password)):
                    session["logged_in"] = True
                    session["username"] = userDB["username"]
                    session["role"] = userDB["role"]
                    #print("Utente che accede nome:",session["username"])
                    #print("login corretto")
                    return redirect(url_for('main'))
                else:
                    session["logged_in"] = False
                    print("login failed")
                    return redirect(url_for('index'))
        except Exception as e:
            print("exception error DB", str(e))
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/listClassPolygon',methods=["GET","POST"])
def listClassPolygon():
    """This function allows to ask db for the polygons' classes list"""
    if request.is_xhr and request.method=="POST":
        try:
            dateold = request.form['dateStr']
            datenew = datetime.datetime(int(dateold[0:4]), int(dateold[4:6]), int(dateold[6:8]), int(dateold[9:11]))
            #print("Individuare classi di Polygon con datetime : ", str(datenew))
            result, cursorListClassPolygon = managedb.groupByClassPolygonDB(datenew)
            if (result == False):
                print("Polygons' classes: there aren't results")
                return json.dumps({"result": "empty"})
            else:
                print("Polygons' classes: there are results")
                print(cursorListClassPolygon)
                cursorListClassClusterJSON = mytools.modifyClassPolygonJSON(cursorListClassPolygon)
                return cursorListClassClusterJSON
                #return json.dumps({"result": "ok"})
        except Exception as e:
            print("exception error DB", str(e))
            return json.dumps({"result": "error"})

@app.route('/insertStorm',methods=["GET","POST"])
def insertStorm():
    """This function allows to insert the polygon into db"""
    if request.is_xhr and request.method=="POST":
        #print(type(request.form))
        #for a in request.form:
        #    print("dati:",a,request.form[a])
        polygonGeoJson = request.get_json()
        #print("Polygon da inserire con datetime: ",polygonGeoJson['properties']['dateStr'])
        #modifica data in stringa in datatime
        dateold = polygonGeoJson['properties']['dateStr']
        datenew = datetime.datetime(int(dateold[0:4]),int(dateold[4:6]),int(dateold[6:8]),int(dateold[9:11]))
        polygonGeoJson['properties']['dateStr'] = datenew
        #print("data nuova:",str(polygonGeoJson['properties']['dateStr']))
        polygonGeoJson["properties"]["name"] = polygonGeoJson["properties"]["name"].upper()
        #for key, value in polygonGeoJson.iteritems():
        #    print(key,value)
        #    print(" ")
        #print(type(polygonGeoJson))
        try:
            id = managedb.insertPolygonDB(polygonGeoJson)
            #print("Polygon da inserire con idDB:",str(id))
            return json.dumps({"id":str(id)})
        except Exception as e:
            print("exception error DB",str(e))
            return json.dumps({"id": "error"})

@app.route('/deleteStorm',methods=["GET","POST"])
def deleteStorm():
    """This function allows to remove a polygon from db"""
    if request.is_xhr and request.method=="POST":
        idDB = request.form['id']
        print("Polygon to be deleted with idDB",idDB)
        try:
            managedb.deletePolygonDB(idDB)
            return json.dumps({"result":"correct"})
        except Exception as e:
            print("exception error DB ",str(e))
            return json.dumps({"result" : "error"})

@app.route('/listStormOnDate',methods=["GET","POST"])
def listStormOnDate():
    """This function allows to ask the db for polygons' list of specific date"""
    if request.is_xhr and request.method=="POST":
        dateold = request.form['dateStr']
        datenew = datetime.datetime(int(dateold[0:4]), int(dateold[4:6]), int(dateold[6:8]), int(dateold[9:11]))
        print("Request Polygon list with datetime: ",str(datenew))
        try:
            result,cursorListPolygon = managedb.listPolygonOnDateDB(datenew)
            if(result == False):
                print("polygon: there aren't results")
                return json.dumps({"result": "empty"})
            else:
                print("polygon: there are results")
                cursorListPolygonJSON= mytools.modifyPolygonJSON(cursorListPolygon)
                return cursorListPolygonJSON
        except Exception as e:
            print("exception error DB",str(e))
            return json.dumps({"result":"error"})

@app.route('/listLabelsOnIdDB',methods=["GET","POST"])
def listLabelsOnIdDB():
    """This function allows to ask the db for labels' list"""
    if request.is_xhr and request.method=="POST":
        idDB = request.form["id"]
        global flag
        global count12
        try:
            count12 = managedb.countLabelDB()
            if(count12 == 0):
                print("Label count:",count12)
                flag = True
        except Exception as e:
            print("exception error DB", str(e))
            return json.dumps({"result": "error"})
        #the insertion default values
        if (flag):
            flag = False
            try:
                labels = ["","Medicane", "Storm", "Thunderstorm"]
                for l in labels:
                    label = {"labelName": l.upper(),"labelId":count12}
                    id = managedb.insertLabelDB(label)
                    #print("Label inserito id:", str(id))
                    count12 += 1
            except Exception as e:
                print("exception error DB", str(e))
                return json.dumps({"result": "error"})
        try:
            result,cursorListLabel = managedb.listLabelDB()
            if(result == False):
                print("label: there aren't results")
                return json.dumps({"result": "empty"})
            else:
                print("label: there are results")
                cursorListLabelJSON = mytools.modifyLabelJSON(cursorListLabel)
                return cursorListLabelJSON
        except Exception as e:
            print("exception error DB",str(e))
            return json.dumps({"result":"error"})

@app.route('/insertLabelsOnIdDB',methods=["GET","POST"])
def insertLabelsOnIdDB():
    """This function allows to add a new label"""
    global count12
    if request.is_xhr and request.method=="POST":
        try:
            count12 = managedb.countLabelDB()
        except Exception as e:
            print("exception error DB", str(e))
        l = request.form["label"]
        label = {"labelName":l.upper(),"labelId":count12}
        print("Label da inserire,",l.upper(), "labelId",count12)
        try:
            id = managedb.insertLabelDB(label)
            print("label id:", str(id))
            count12 += 1
            return json.dumps({"result": "correct"})
        except Exception as e:
            print("exception error DB", str(e))
            return json.dumps({"result": "error"})

@app.route('/modifyLabel',methods=["GET","POST"])
def modifyLabel():
    """This function allows to change the label of a polygon"""
    if request.is_xhr and request.method=="POST":
        idDB = request.form["id"]
        name = request.form["name"]
        #print("modifica label del Polygon con idDB",idDB)
        #print("nuova etichetta",name)
        try:
            managedb.modifyLabelPolygonOnIdDB(idDB,name)
            return json.dumps({"result": "correct"})
        except Exception as e:
            print("exception error DB",str(e))
            return json.dumps({"result": "error"})

@app.route('/listPointClusterOnDate',methods=["GET","POST"])
def listPointClusterOnDate():
    """This function asks the db for clusters' points list of specific date"""
    if request.is_xhr and request.method=="POST":
        dateold = request.form['dateStr']
        datenew = datetime.datetime(int(dateold[0:4]), int(dateold[4:6]), int(dateold[6:8]), int(dateold[9:11]))
        #print("Individuare i Point Cluster con datetime", str(datenew))
        try:
            result, cursorListPointCluster = managedb.listPointClusterOnDateDB(datenew)
            if (result == False):
                print("point: there aren't results")
                return json.dumps({"result": "empty"})
            else:
                print("point: there are results")
                cursorListPointClusterJSON = mytools.modifyPointClusterJSON(cursorListPointCluster)
                return cursorListPointClusterJSON
        except Exception as e:
            print("exception error DB", str(e))
            return json.dumps({"result": "error"})

@app.route('/listClassCluster',methods=["GET","POST"])
def listClassCluster():
    """This function asks the db for clusters' classes list"""
    if request.is_xhr and request.method=="POST":
        try:
            result, cursorListClassCluster = managedb.listClassClusterDB()
            if (result == False):
                print("clusters' classes: there aren't results")
                return json.dumps({"result": "empty"})
            else:
                print("clusters' classes: there are results")
                cursorListClassClusterJSON = mytools.modifyClassClusterJSON(cursorListClassCluster)
                return cursorListClassClusterJSON
        except Exception as e:
            print("exception error DB", str(e))
            return json.dumps({"result": "error"})
