from flask import Flask
from flask import Flask, jsonify,flash
from flask import request
from flaskext.mysql import MySQL
from flask import render_template
import json

from flask import Response
from flask_cors import CORS
from flask import request
import requests
from bs4 import BeautifulSoup
import re

basic = {'1.1': "Moores law", '1.2': "Computer organization"}

#Dictonary som innehåller Javaboken: early objects
javaboken = {

    'Chapter 1':'Introduction to Computers, the Internet and Java',
    'Chapter 2': 'Introduction to Java Applications; Input/Output and Operators',
    'Chapter 3': 'Introduction to Classes, Objects, Methods and Strings',
    'Chapter 4': 'Control Statements: Part 1; Assignment, ++ and — Operators',
    'Chapter 5': 'Control Statements: Part 2; Logical Operators',
    'Chapter 6': 'Methods: A Deeper Look',
    'Chapter 7': 'Arrays and ArrayLists',
    'Chapter 8': 'Classes and Objects: A Deeper Look',
    'Chapter 9': 'Object-Oriented Programming: Inheritance',
    'Chapter 10': 'Object-Oriented Programming: Polymorphism and Interfaces',
    'Chapter 11': 'Exception Handling: A Deeper Look',
    'Chapter 12': 'GUI Components: Part 1',
    'Chapter 13': 'Graphics and Java 2D',
    'Chapter 14': 'Strings, Characters and Regular Expressions',
    'Chapter 15': 'Files, Streams and Object Serialization',
    'Chapter 16': 'Generic Collections',
    'Chapter 17': 'Java SE 8 Lambdas and Streams',
    'Chapter 18': 'Recursion',
    'Chapter 19': 'Searching, Sorting and Big O',
    'Chapter 20': 'Generic Classes and Methods',
    'Chapter 21': 'Custom Generic Data Structures',
    'Chapter 22': 'GUI Components: Part 2',
    'Chapter 23': 'Concurrency',
    'Chapter 24': 'Accessing Databases with JDBC',
    'Chapter 25': 'JavaFX GUI: Part 1'

}




javaBook = json.dumps(javaboken)



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#MySQL-config
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'newuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty'
app.config['MYSQL_DATABASE_DB'] = 'gggg'
app.config['MYSQL_DATABASE_HOST'] = '92.32.45.159'
mysql.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


#Frågor
@app.route('/questions')
def getQuestions():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return Response(json.dumps(json_data, ensure_ascii=False), mimetype='application/json')

    #return jsonify({'questions':questions})

#Svar
@app.route("/answers", methods=['GET'])
def getAnswers():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM answer ")

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return json.dumps(json_data,ensure_ascii=False)

@app.route("/quizanswers/<string:quizID>", methods=["GET"])
def getQuizAnswers(quizID):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizanswers WHERE quizID="+quizID)

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    json_data = []
    for result in questions:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return Response(json.dumps(json_data,ensure_ascii=False),mimetype='application/json')



@app.route("/dashboard")
def getDashboard():
    return render_template('Dashboardtest.html')

@app.route("/getBookChapter/<string:chapterID>")
def getChapter(chapterID):


    return Response ((javaBook),mimetype='application/json' )


@app.route("/createuser/<string:name>", methods=['POST'])
@app.route("/createuser/<string:nameID>", methods=['POST'])
def createUser(nameID):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO `user` (`name`) VALUES"+"("+"'"+nameID+"'"+");")
    conn.commit()
    conn.close()

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user ORDER BY iduser DESC LIMIT 0, 1")
    row_headers2 = [x[0] for x in cursor.description]

    json_data = []

    userid=cursor.fetchall()

    for i in userid:
        json_data.append(dict(zip(row_headers2,i)))


    conn.close()
    print(userid)








    return Response(json.dumps(json_data, ensure_ascii=False), mimetype='application/json')



@app.route("/getUser/<string:u_id>")
def getUser(u_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE iduser="+u_id)

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    print(questions)
    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))


    conn.close()
    sucess = {'isUser': False,"userID":u_id}
    unsucess = {'isUser': True,"userID":u_id}
    if len(json_data)<1:

       return Response(json.dumps(sucess, ensure_ascii=False), mimetype='application/json')
    else:
        return Response(json.dumps(unsucess, ensure_ascii=False), mimetype='application/json')

@app.route("/titles/<string:keyword>")
def getTitles(keyword):
    headers = {'Accept-Encoding': 'identity'}
    test = requests.get("https://www.tutorialspoint.com/java/", headers=headers)

    oracle = requests.get("https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html", headers=headers)

    w3 = requests.get("https://www.w3schools.com/java/", headers=headers)

    htmlW3 = BeautifulSoup(w3.content, 'html.parser')

    jsonW3 = []
    jsonW3Links = []

    html = BeautifulSoup(test.content, 'html.parser')

    htmlOracle = BeautifulSoup(oracle.content, 'html.parser')

    for linkd in htmlW3.find_all("a", href=re.compile(keyword)):
        links = "https://www.w3schools.com/java/" + linkd.get("href")
        w3link = requests.get("https://www.w3schools.com/java/" + linkd.get("href"))

        w3LinkSoup = BeautifulSoup(w3link.content, 'html.parser')

        jsonW3Links.append(w3LinkSoup.title.string)

        jsonW3.append(links)
    jsonOracle = []
    jsonOracleLink = []

    for li in htmlOracle.find_all("a", href=re.compile(keyword)):
        links = "https://docs.oracle.com/javase/7/docs/api/" + li.get("href")

        oracleLink = requests.get(links)
        oracleLinkSoup = BeautifulSoup(oracleLink.content, 'html.parser')
        jsonOracleLink.append(oracleLinkSoup.title.string)

        jsonOracle.append(links)

    jsonLink = []
    jsonTutorial = []

    for link in html.find_all("a", href=re.compile(keyword)):
        wholeLink = "https://www.tutorialspoint.com" + link.get("href")

        tutorialLink = requests.get(wholeLink)
        tutorialLinkSoup = BeautifulSoup(tutorialLink.content, 'html.parser')
        jsonTutorial.append(tutorialLinkSoup.title.string)

        jsonLink.append(wholeLink)

    geeks = requests.get("https://www.geeksforgeeks.org/java/")

    htmlGeeks = BeautifulSoup(geeks.content, 'html.parser')
    jsonGeeks = []
    JsonGeeksLink = []

    for lins in htmlGeeks.find_all("a", href=re.compile(keyword)):
        if "http" not in lins.get("href"):
            linkG = "https://www.geeksforgeeks.org/java/" + lins.get("href")
            linkG = linkG.replace(" ", "%20")
        else:
            linkG = lins.get("href")

        geeksLink = requests.get(linkG)
        geeksLinkSoup = BeautifulSoup(geeksLink.content, 'html.parser')
        JsonGeeksLink.append(geeksLinkSoup.title.string)

        jsonGeeks.append(linkG)

    return jsonify({'TutoiralLinks': jsonTutorial, 'OracleLinks': jsonOracleLink, "W3Links": jsonW3Links, "GeeksLinks": JsonGeeksLink})


@app.route("/scrape/<string:keyword>")
def getScrape(keyword):

    if keyword=="Object oriented":
        keyword="Object"
    print("Keyword: "+keyword )
    headers = {'Accept-Encoding': 'identity'}
    test=requests.get("https://www.tutorialspoint.com/java/",headers=headers)

    oracle=requests.get("https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html",headers=headers)

    w3 = requests.get("https://www.w3schools.com/java/",headers=headers)

    htmlW3 = BeautifulSoup(w3.content, 'html.parser')



    jsonW3 = []
    jsonW3Links = []

    html = BeautifulSoup(test.content, 'html.parser')

    htmlOracle = BeautifulSoup(oracle.content, 'html.parser')



    for linkd in htmlW3.find_all("a", href=re.compile(keyword.lower())):
        links="https://www.w3schools.com/java/"+linkd.get("href")
        w3link = requests.get("https://www.w3schools.com/java/"+linkd.get("href"))

        w3LinkSoup = BeautifulSoup(w3link.content, 'html.parser')

        jsonW3Links.append(w3LinkSoup.title.string)



        jsonW3.append(links)
    jsonOracle =[]
    jsonOracleLink = []


    for li in htmlOracle.find_all("a", href=re.compile(keyword)):

        links ="https://docs.oracle.com/javase/7/docs/api/"+li.get("href")

        oracleLink = requests.get(links)
        oracleLinkSoup = BeautifulSoup(oracleLink.content, 'html.parser')
        jsonOracleLink.append(oracleLinkSoup.title.string)

        jsonOracle.append(links)




    jsonLink = []
    jsonTutorial =  []


    for link in html.find_all("a",href=re.compile(keyword.lower())):



        wholeLink = "https://www.tutorialspoint.com"+link.get("href")

        tutorialLink = requests.get(wholeLink)
        tutorialLinkSoup = BeautifulSoup(tutorialLink.content, 'html.parser')
        jsonTutorial.append(tutorialLinkSoup.title.string)

        jsonLink.append(wholeLink)


    geeks = requests.get("https://www.geeksforgeeks.org/java/")

    htmlGeeks = BeautifulSoup(geeks.content,'html.parser')
    jsonGeeks = []
    JsonGeeksLink = []

    for lins in htmlGeeks.find_all("a", href=re.compile(keyword)):
        if "http" not in lins.get("href"):
            linkG = "https://www.geeksforgeeks.org/java/" + lins.get("href")
            linkG = linkG.replace(" ", "%20")
        else:
            linkG=lins.get("href")

        geeksLink = requests.get("https://www.geeksforgeeks.org/java/" + lins.get("href"))
        geeksLinkSoup = BeautifulSoup(geeksLink.content, 'html.parser')
        JsonGeeksLink.append(geeksLinkSoup.title.string)

        jsonGeeks.append(linkG)




    return jsonify({'Subject':keyword,'Links':[{'linksArray':jsonLink, 'title': "Tutorialpoints"},{'linksArray':jsonOracle, 'title': 'Oracle'},{"linksArray":jsonW3, 'title': 'W3'},{"linksArray":jsonGeeks, 'title': 'Geeks'}]})

@app.route("/array", methods=["POST"])
def arr():
    count =0
    antalJava = 0
    antalObject= 0
    antalArv=0
    antalInterface=0
    antalExe=0

    answers=request.get_json()
    select_answer = "SELECT * FROM answer WHERE idanswer = (%(aID)s)"


    select_inner ="SELECT answer.answer, answer.rightAnswer, questions.subject FROM answer  INNER JOIN questions on answer.rightAnswer=1 and questions.idquestions  = "

    for attribute,value in answers.items():
        conn = mysql.connect()
        cursor = conn.cursor()
        qqW=attribute.split("n")

        print("Split"+qqW[1])
        cursor.execute(select_inner+qqW[1])
        row_headers = [x[0] for x in cursor.description]
        json_data = []


        fetchedAnswers=cursor.fetchall()
    #TODO Score för delmoment


        print(json_data)
        counter=0
        for ans in fetchedAnswers:
            json_data.append(dict(zip(row_headers,ans)))

            if str(value)==str(json_data[counter].get("answer")):
                print("DEBUG:!!!!!!"+json_data[counter].get("subject")== "Inheritance")
                if json_data[counter].get("subject")== "Inheritance":

                    antalArv+=1
                elif json_data[counter].get("subject")=="Objectoriented":
                    antalObject+=1
            counter+=1

        print(fetchedAnswers)

        conn.close()
#TODO FORTSÄTT RÄTTNING
    print("Antal rätt Arv:"+str(antalArv)+"Antal rätt: " + str(antalObject))
        #Rättning


    #Sammantsällning


    #Länkar




    return ('', 204)
@app.route("/setquizresult", methods=["POST"])
def testRoute():
    selectArvAnser = "SELECT answer.idanswer,questions.idquestions,questions.questiontype,answer.answer, answer.rightAnswer,answer.questions_idquestions, questions.subject FROM answer  INNER JOIN questions ON idquestions=questions_idquestions AND rightAnswer=1"
    #selectArvAnser = "SELECT answer.idanswer,questions.idquestions,questions.questiontype,answer.answer, answer.rightAnswer,answer.questions_idquestions, questions.subject FROM answer  INNER JOIN questions ON idquestions=questions_idquestions AND subject= 'Arv' AND rightAnswer=1"
    answers = request.get_json()
    ID=answers['userID']
    result = answers['resultat']
    print("****"*5)
    print(answers)
    print("****" * 5)
    jsonArv = []
    arvCounter=0
    ooCounter=0
    overrideCounter=0
    javaCounter=0
    exeCounter=0
    interfaceCounter=0

    select_count = "select count(*) from questions where subject="

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(selectArvAnser)

    arvAnswer = cursor.fetchall()
    row_headers = [x[0] for x in cursor.description]
    conn.close()

    for arv in arvAnswer:
        jsonArv.append(dict(zip(row_headers,arv)))

    print(jsonArv[0].get('rightAnswer'))



    dbLen = len(jsonArv)
    for attribute, value in result.items():

        att = attribute.split("n")
        if len(att)>1:
            questionnumber = att[1]
        else:
            questionnumber= attribute
        for x in range (0,dbLen):


            if str(questionnumber)==str(jsonArv[x].get("idquestions")):
                print("Svarsnummer från JSON"+str(value))
                print("Svarsnummer från DB"+str(jsonArv[x].get("idanswer")))


                #Skriv
                if str(value)==str(jsonArv[x].get('idanswer')):

                    print("Subject"+str(jsonArv[x].get('subject')))
                    if str(jsonArv[x].get('subject'))=="Objectoriented":
                        ooCounter+=1

                    if str(jsonArv[x].get('subject'))=="Inheritance":
                        arvCounter+=1
                    if str(jsonArv[x].get('subject')) == "Java":
                        javaCounter+=1
                    if str(jsonArv[x].get('subject')) == "Override":
                        overrideCounter+=1
                    if str(jsonArv[x].get('subject')) == "Exception handling":
                        exeCounter+=1


                    if str(jsonArv[x].get('subject')) == "Interface":
                        interfaceCounter+=1


        print("arv")
        print(arvCounter)
        print("OO")
        print(ooCounter)



    insert_result = "INSERT INTO RESULTS"

    insert_insert = "INSERT INTO `gggg`.`results` ( `antalPolymorfism`, `antalMVC`, `antalSyntax`, `antalInterface`, `antalExpH`, `antalBib`, `idUser`, `antalOverride`, `antalOO`, `antalArv`) VALUES (%(poly)s, %(mvc)s, %(syntax)s, %(a_interface)s, %(excepH)s, %(antalbib)s, %(iduser)s,%(override)s,%(antal_obj)s,%(arv)s);"



    #VALUES (%(poly)s, %(mvc)s, %(syntax)s, %(a_interface)s, %(excepH)s, %(antalbib)s, %(iduser)s,%(override)s,%(antal_obj)s,%(arv)s);"
    data_result ={
        'poly':0,
        'mvc':0,
        'syntax':javaCounter,
        'a_interface':interfaceCounter,
        'excepH':exeCounter,
        'antalbib':0,
        'iduser':int(ID),
        'override':overrideCounter,
        'antal_obj':ooCounter,
        "arv":arvCounter
    }
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(insert_insert,data_result)
    conn.commit()
    conn.close()


    print(data_result)
    return jsonify({'Interface':interfaceCounter,'MaxInterface':getMaxFromDb('Interface'),'Inheritance':arvCounter,'MaxInheritance':getMaxFromDb('Inheritance'),'Exception handling':exeCounter,'MaxException':getMaxFromDb('Exception handling'),'Override':overrideCounter,'MaxOverride':getMaxFromDb('Override'),'Objectoriented':ooCounter,'MaxObjectoriented':getMaxFromDb('Objectoriented'),'Java':javaCounter,'MaxJava':getMaxFromDb('Java')})
def getMaxFromDb(sub):

    select_count = "select count(*) from questions where subject= '"+sub+"'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(select_count)
    maxQ=cursor.fetchall()
    conn.close()
    cursor.close()

    maxxad=maxQ[0][0]


    return int(maxxad)
@app.route("/youtube/<string:subj>")
def getYoutube(subj):

    par={'maxResults':25,'q':subj,"key":"AIzaSyAmJ9nChEujZVT8IfaMN1RzlALsygVxgT0"}
    yott=requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet",params=par)

    print(yott)
    return json.dumps(yott.json())
@app.route("/getresult/<string:userid>")
def getResultat(userid):

    resultJson = {

    }
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results WHERE idUser = "+ userid+ " ORDER BY idresults DESC LIMIT 1")
    row_headers = [x[0] for x in cursor.description]

    results = cursor.fetchall()

    json_data = []
    conn.close()

    for result in results:

        tempdict=(dict(zip(row_headers, result)))
        for key, value in tempdict.items():

            resultDict = {}

            if key=="antalPoly":
                resultDict["Field"]="Polymorphism"
                resultDict["Resultat"]=tempdict["antalPoly"]
                resultDict["Max"]=getMaxFromDb("Poly")
                json_data.append(resultDict)



            elif key=="antalMVC":
                resultDict["Field"] = "MVC"
                resultDict["Resultat"] = tempdict["antalMVC"]
                resultDict["Max"] = getMaxFromDb("MVC")
                json_data.append(resultDict)

            elif key=="antalSyntax":
                resultDict["Field"] = "Syntax"
                resultDict["Resultat"] = tempdict["antalSyntax"]
                resultDict["Max"] = getMaxFromDb("Syntax")
                json_data.append(resultDict)
            elif key=="antalInterface":
                resultDict["Field"] = "Interface"
                resultDict["Resultat"] = tempdict["antalInterface"]
                resultDict["Max"] = getMaxFromDb("Interface")
                json_data.append(resultDict)

            elif key=="antalExpH":
                resultDict["Field"] = "Exceptions"
                resultDict["Resultat"] = tempdict["antalExpH"]
                resultDict["Max"] = getMaxFromDb("Exception handling")
                json_data.append(resultDict)

            elif key=="antalBib":
                resultDict["Field"] = "Bibliotek"
                resultDict["Resultat"] = tempdict["antalBib"]
                resultDict["Max"] = getMaxFromDb("Bibliotek")
                json_data.append(resultDict)

            elif key=="antalOverride":
                json_data.append(resultDictionary(tempdict,"Override","antalOverride","Override"))
                #resultDict(tempdict, field, antal, max)

            elif key=="antalOO":
                json_data.append(resultDictionary(tempdict,"Object oriented","antalOO","Objectoriented"))

            elif key=="antalArv":
                json_data.append(resultDictionary(tempdict,"Inheritance","antalArv","Inheritance"))












    return json.dumps(json_data,ensure_ascii=False)
def resultDictionary(tempdict,field,antal,max):
    reDict = {}

    reDict["Field"] = field
    reDict["Resultat"] = tempdict[antal]
    reDict["Max"] = getMaxFromDb(max)

    return reDict

@app.route("/testoverride", methods=["POST"])
def test3():
    answers = request.get_json()

    print(answers)
    return "Hello"
@app.route("/checkresult/<string:id>", methods=["GET"])
def checkresult(id):

    select_result = "SELECT * FROM results WHERE  idUser= " +id
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(select_result)
    json_data = []
    row_headers = [x[0] for x in cursor.description]

    results = cursor.fetchall()

    for result in results:

        json_data.append((dict(zip(row_headers, result))))

    conn.close()









    if len(json_data)<1:

        return jsonify({"result":False})
    else: return jsonify({"result":True})

if __name__ == '__main__':
    app.run()
