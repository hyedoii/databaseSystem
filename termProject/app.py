from flask import Flask, render_template, request, redirect
import pymysql
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import re
import math
import urllib
from urllib.request import urlretrieve
from urllib.parse import quote

clist =[]
dlist = []

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def callclinicname(name):
    db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',
                         charset='utf8')
    cursor = db.cursor()

    url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?yadmNm='+quote(str(name))+'&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    pagenum = soup.find_all('totalcount')
    print(pagenum)
    pagenum = math.ceil(int(pagenum[0].text) / 300)
    print(pagenum)

    for j in range(pagenum):
        url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?numOfRows=300&pageNo=' + str(
            j + 1) +'&yadmNm='+str(name)+'&radius=5000&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'
        print(url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('item'):
            clinicname = i.find('yadmnm')
            if (clinicname == None):
                clinicname = 'NULL'
            else:
                clinicname = clinicname.text
            codename = i.find('clcdnm')
            if (codename == None):
                codename = 'NULL'
            else:
                codename = codename.text
            addr = i.find('addr')
            if (addr == None):
                addr = 'NULL'
            else:
                addr = addr.text
            telno = i.find('telno')
            if (telno == None):
                telno = 'NULL'
            else:
                telno = telno.text
            xpos = i.find('xpos')
            if (xpos == None):
                xpos = 'NULL'
            else:
                xpos = xpos.text
            ypos = i.find('ypos')
            if (ypos == None):
                ypos = 'NULL'
            else:
                ypos = ypos.text

            print(clinicname, codename, addr, telno, xpos, ypos)

            sql = '''insert into clinic (name, codename, addr, telno, xpos, ypos) values (%s,%s,%s,%s,%s,%s);'''
            cursor.execute(sql, (clinicname, codename, addr, telno, xpos, ypos))
            db.commit()

    sql = '''select * from clinic where name = %s;'''
    cursor.execute(sql,(name))
    clist = cursor.fetchall()

    db.close()

    return clist

def calldrugname(name):
    db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',
                         charset='utf8')
    cursor = db.cursor()

    url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?yadmNm=' + quote(str(name)) + '&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    pagenum = soup.find_all('totalcount')
    print(pagenum)
    pagenum = math.ceil(int(pagenum[0].text) / 300)
    print(pagenum)

    for j in range(pagenum):
        url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?numOfRows=300&pageNo=' + str(j+1)+'&yadmNm=' + quote(str(name)) + '&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'
        print(url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('item'):
            drugname = i.find('yadmnm')
            if (drugname == None):
                drugname = 'NULL'
            else:
                drugname = drugname.text

            addr = i.find('addr')
            if (addr == None):
                addr = 'NULL'
            else:
                addr = addr.text

            telno = i.find('telno')
            if (telno == None):
                telno = 'NULL'
            else:
                telno = telno.text

            xpos = i.find('xpos')
            if (xpos == None):
                xpos = 'NULL'
            else:
                xpos = xpos.text

            ypos = i.find('ypos')
            if (ypos == None):
                ypos = 'NULL'
            else:
                ypos = ypos.text

            print(drugname, addr, telno, xpos, ypos)

            sql = '''insert into drug (name, addr, telno, xpos, ypos) values (%s,%s,%s,%s,%s);'''
            cursor.execute(sql, (drugname, addr, telno, xpos, ypos))
            db.commit()

    sql = '''select * from drug where name = %s;'''
    cursor.execute(sql, (name))
    dlist = cursor.fetchall()

    db.close()

    return dlist


def callclinic(xPos, yPos):
    global clist
    clist=[]
    # 병원 api
    db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',charset='utf8')
    cursor = db.cursor()

    url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?xPos='+xPos+'&yPos='+yPos+'&radius=5000&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    pagenum = soup.find_all('totalcount')
    print(pagenum)
    pagenum = math.ceil(int(pagenum[0].text)/300)
    print(pagenum)

    for j in range(pagenum):
        url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?numOfRows=300&pageNo='+str(j+1)+'&xPos=' + xPos + '&yPos=' + yPos + '&radius=5000&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'
        print(url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('item'):
            clinicname = i.find('yadmnm')
            if(clinicname==None):
                clinicname = 'NULL'
            else:
                clinicname = clinicname.text
            codename = i.find('clcdnm')
            if (codename==None):
                codename = 'NULL'
            else:
                codename = codename.text
            addr = i.find('addr')
            if (addr==None):
                addr = 'NULL'
            else:
                addr = addr.text
            telno = i.find('telno')
            if (telno==None):
                telno = 'NULL'
            else:
                telno = telno.text
            xpos = i.find('xpos')
            if (xpos==None):
                xpos = 'NULL'
            else:
                xpos = xpos.text
            ypos = i.find('ypos')
            if (ypos==None):
                ypos = 'NULL'
            else:
                ypos = ypos.text

            print(clinicname, codename, addr, telno, xpos, ypos)

            sql = '''insert into clinic (name, codename, addr, telno, xpos, ypos) values (%s,%s,%s,%s,%s,%s);'''
            cursor.execute(sql, (clinicname, codename, addr, telno, xpos, ypos))
            db.commit()

    sql = '''select * from clinic '''
    cursor.execute(sql)
    result = cursor.fetchall()
    for code in result:
        if haversine(float(code[4]), float(code[5]), float(xPos), float(yPos)) < 5000:
            clist.append(code)
    db.close()

    return clist

def calldrug(xPos,yPos):
    global dlist
    dlist = []
    # 병원 api
    db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',charset='utf8')
    cursor = db.cursor()

    url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?xPos=' + xPos + '&yPos=' + yPos + '&radius=5000&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    pagenum = soup.find_all('totalcount')
    print(pagenum)
    pagenum = math.ceil(int(pagenum[0].text) / 300)
    print(pagenum)

    for j in range(pagenum):
        url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?numOfRows=300&pageNo=' + str(j + 1) + '&xPos=' + xPos + '&yPos=' + yPos + '&radius=5000&ServiceKey=v9jY2QEWmiWpmzzCj5o%2FGjOEvDRd0eZcpaPl7wWjgz3nPw7kymwjsiXmt9DIr%2FSObx%2BlSpF%2F57gmuRcJTCXMBA%3D%3D'
        print(url)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('item'):
            drugname = i.find('yadmnm')
            if (drugname == None):
                drugname = 'NULL'
            else:
                drugname = drugname.text

            addr = i.find('addr')
            if (addr == None):
                addr = 'NULL'
            else:
                addr = addr.text

            telno = i.find('telno')
            if (telno == None):
                telno = 'NULL'
            else:
                telno = telno.text

            xpos = i.find('xpos')
            if (xpos == None):
                xpos = 'NULL'
            else:
                xpos = xpos.text

            ypos = i.find('ypos')
            if (ypos == None):
                ypos = 'NULL'
            else:
                ypos = ypos.text

            print(drugname, addr, telno, xpos, ypos)

            sql = '''insert into drug (name, addr, telno, xpos, ypos) values (%s,%s,%s,%s,%s);'''
            cursor.execute(sql, (drugname, addr, telno, xpos, ypos))
            db.commit()

    sql = '''select * from drug '''
    cursor.execute(sql)
    result = cursor.fetchall()
    for code in result:
        print(code)
        if haversine(float(code[3]), float(code[4]), float(xPos), float(yPos)) < 5000:
            dlist.append(code)
    db.close()

    return dlist

app = Flask(__name__)

# Ensure templates are quto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

inputlocal = ""
inputdomain = ""
passwd = ""
resultname = ""
loginxpos=""
loginypos=""


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/logedIn', methods=['GET', 'POST'])
def logedIn():
    global inputlocal, inputdomain, passwd, resultname, loginxpos, loginypos
    cliniclist = ""
    if request.method == "POST":
        email = request.form['inputemail']
        passwd = request.form['inputpasswd']
        list = email.split("@")
        print(list)
        inputlocal = list[0]
        inputdomain = list[1]
        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',charset='utf8')
        cursor = db.cursor()
        sql = '''select name, position, lat, lng from login where local = %s && domain=%s && pass = %s;'''
        cursor.execute(sql, (inputlocal, inputdomain, passwd))

        result = cursor.fetchall()
        db.commit()
        db.close()

        ok = len(result)
        print(ok)
        if ok > 0 :
            resultname = result[0][0]
            resultposition = result[0][1]
            loginypos = result[0][2]
            loginxpos = result[0][3]

            if (resultposition == None):
                return redirect('/setposition')
        else:
            return redirect('/')

    return render_template("logedIn.html", nn=resultname)


@app.route('/setposition', methods=['GET', 'POST'])
def setposition():
    global inputlocal, inputdomain, passwd, resultname
    if request.method == "POST":
        positionInput = request.form['inputposition']
        print(positionInput)
        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',charset='utf8')
        cursor = db.cursor()
        sql = '''UPDATE login SET position=%s WHERE local=%s && domain =%s && pass = %s;'''
        cursor.execute(sql, (positionInput, inputlocal, inputdomain, passwd))
        db.commit()
        result = cursor.fetchall()
        print(result)

        db.close()
        return redirect('/logedIn')

    return render_template("setposition.html", nn=resultname)

@app.route('/setsname', methods=['GET','POST'])
def setsname():
    global inputlocal, inputdomain, passwd, resultname
    if request.method == "POST":
        sname = request.form['inputsname']
        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',charset='utf8')
        cursor = db.cursor()
        sql = '''UPDATE login SET sname=%s WHERE local=%s && domain =%s && pass = %s;'''
        cursor.execute(sql, (sname, inputlocal, inputdomain, passwd))
        db.commit()
        db.close()
        return redirect('/')

    return render_template("setsname.html", nn=resultname)



@app.route('/signup', methods=['GET','POST'])
def signup():
    global inputlocal, inputdomain, passwd, resultname
    if request.method == "POST":
        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',charset='utf8')
        cursor = db.cursor()

        name = str(request.form['inputname'])
        email = str(request.form['inputemail'])
        list = email.split("@")
        sinputlocal = str(list[0])
        sinputdomain = str(list[1])
        spasswd = str(request.form['inputpasswd'])
        phone = str(request.form['inputphone'])
        lat = str(request.form['inputlat'])
        lng = str(request.form['inputlng'])
        position = str(request.form['inputposition'])

        sql = '''insert into login (name, phone, local, domain ,pass,lat,lng,position) values (%s,%s,%s,%s,%s,%s,%s,%s);'''
        cursor.execute(sql, (name, phone, sinputlocal,sinputdomain,spasswd,lat,lng,position))
        db.commit()
        db.close()
        if position != 'patient' :
            inputlocal = sinputlocal
            inputdomain = sinputdomain
            passwd = spasswd
            resultname = name
            return redirect('/setsname')

    return render_template("signup.html")

@app.route('/searchclinicname', methods=['GET','POST'])
def searchclinicname():
    message=""
    if request.method == "POST":
        clinicname = request.form['inputname']
        result = callclinicname(clinicname)
        print(len(result))
        if len(result) == 0 :
            message = "검색결과가 없습니다."
        else:
            message = result
            for code in result:
                print(code)

    return render_template("searchclinicname.html", resultlist=message)


@app.route('/searchdrugname', methods=['GET','POST'])
def searchdrugname():
    message=""
    if request.method == "POST":
        drugname = request.form['inputname']
        result = calldrugname(drugname)
        print(len(result))
        if len(result) == 0 :
            message = "검색결과가 없습니다."
        else:
            message = result
            for code in result:
                print(code)

    return render_template("searchdrugname.html", resultlist=message)


@app.route('/searchcliniclocation', methods=['GET', 'POST'])
def searchcliniclocation():
    message = ""
    if request.method == "POST":
        xPos = request.form['inputxpos']
        yPos = request.form['inputypos']
        result = callclinic(xPos, yPos)
        print(len(result))
        if len(result) == 0:
            message = "검색결과가 없습니다."
        else:
            message = result
            for code in result:
                print(code)

    return render_template("searchcliniclocation.html", resultlist = message)

@app.route('/searchdruglocation', methods=['GET', 'POST'])
def searchdruglocation():
    message = ""
    if request.method == "POST":
        xPos = request.form['inputxpos']
        yPos = request.form['inputypos']
        result = calldrug(xPos, yPos)
        print(len(result))
        if len(result) == 0:
            message = "검색결과가 없습니다."
        else:
            message = result
            for code in result:
                print(code)

    return render_template("searchdruglocation.html", resultlist = message)

@app.route('/searchnearclinic/', methods=['GET', 'POST'])
def searchnearclinic():
    global loginxpos, loginypos
    message = ""
    result = callclinic(loginxpos,loginypos)
    if len(result) == 0:
        message = "검색결과가 없습니다."
    else:
        message = result
        for code in result:
            print(code)
    return render_template("searchnearclinic.html",resultlist=message)


@app.route('/searchneardrug/', methods=['GET', 'POST'])
def searchneardrug():
    global loginxpos, loginypos
    message = ""
    result = calldrug(loginxpos,loginypos)
    if len(result) == 0:
        message = "검색결과가 없습니다."
    else:
        message = result
        for code in result:
            print(code)
    return render_template("searchneardrug.html",resultlist=message)


if __name__ == ("__main__"):
    app.run(debug=True)
'''
    db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='termProject',
                         charset='utf8')

    # 커서 가져오기
    cursor = db.cursor()

    try:
        # SQL문

        sql = CREATE TABLE login(
        name CHAR(100) NOT NULL,
        phone CHAR(100) NOT NULL,
        local CHAR(100) NOT NULL,
        domain CHAR(100) NOT NULL,
        pass CHAR(100) NOT NULL,
        lat CHAR(100) NOT NULL,
        lng CHAR(100) NOT NULL,
        position CHAR(100),
        sname char(100)
        );

        # 실행하기
        cursor.execute(sql)

        # DB에 Complete 하기
        db.commit()

        # 초기 데이터 저장
        f = open('customers.csv', 'r', encoding='UTF-8')
        rdr = csv.reader(f)

        sql = INSERT INTO login(name, phone,local, domain, pass, lat, lng)
                VALUES( %s, %s, %s, %s, %s, %s, %s)

        linecount = 0

        for line in rdr:
            if linecount == 0:
                linecount = linecount + 1
            else:
                nameInput = line[0]
                phoneInput = line[1]
                localInput = line[2]
                domainInput = line[3]
                passInput = line[4]
                latInput = line[6]
                lngInput = line[7]

                # 실행하기
                cursor.execute(sql, (nameInput, phoneInput, localInput, domainInput, passInput, latInput, lngInput))

                # DB에 Complete 하기
                db.commit()

        f.close()

    finally:
        # DB 연결 닫기
        db.close()
'''

