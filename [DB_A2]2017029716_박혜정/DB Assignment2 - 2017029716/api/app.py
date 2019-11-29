from flask import Flask, render_template, request, json
import pymysql
import csv
import re

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/showInsert', methods=['GET', 'POST'])
def showInsert():
    rows=""
    if request.method == "POST":
        _name = request.form['inputName']
        _phone = request.form['inputPhone']

        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='maria',charset='utf8')
        cursor = db.cursor()
        sql = '''insert into info (name, phone) values (%s, %s)'''
        cursor.execute(sql, (_name, _phone))
        db.commit()
        db.close()
        rows = "< name : "+_name+", phone : "+_phone+"> is inserted."

    return render_template("insert.html", result=rows)


@app.route('/showDelete', methods=['GET','POST'])
def showDelete():
    ro=""
    if request.method == 'POST':
        _name = request.form['inputName']
        _phone = request.form['inputPhone']
        print("_name : ", _name)

        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='maria',charset='utf8')
        cursor = db.cursor()
        sql = '''delete from info where name = %s and phone = %s'''
        cursor.execute(sql, (_name, _phone))

        db.commit()
        db.close()
        ro = "deleted."
    return render_template("delete.html", result=ro)


@app.route('/showSearch', methods=['GET', 'POST'])
def showSearch():
    ro = ""
    if request.method == 'POST':
        _name = request.form['inputName']
        print(_name)

        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='maria', charset='utf8')
        cursor = db.cursor()
        sql = '''select * from info where name like %s'''
        cursor.execute(sql, (_name+'%'))
        rows = cursor.fetchall()

        for line in rows:
            ro = ro +line[0]+" "+line[1]+'\r\n'

        db.commit()
        db.close()

    return render_template("search.html", result=ro)

@app.route('/showUpdate', methods=['GET','POST'])
def showUpdate():
    rows=""
    if request.method == "POST":
        _name = request.form['inputName']
        _phone = request.form['inputPhone']
        _edit = request.form['inputEdit']

        db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='maria',charset='utf8')
        cursor = db.cursor()
        sql = '''update info set phone = %s where name = %s and phone = %s'''
        cursor.execute(sql, (_edit, _name, _phone))
        db.commit()
        db.close()

        rows = "updated."

    return render_template("update.html", result = rows)



if __name__ == ("__main__"):
    '''
    # 접속
    db = pymysql.connect(host='localhost', port=3306, user='parkhyejeong', passwd='wldwld01!', db='maria',
                         charset='utf8')

    # 커서 가져오기
    cursor = db.cursor()

    try:
        # SQL문

        sql = 
                CREATE TABLE info (
                name CHAR(100) NOT NULL,
                phone CHAR(100) NOT NULL,
                PRIMARY KEY(name, phone)
            );

        # 실행하기
        cursor.execute(sql)

        # DB에 Complete 하기
        db.commit()

        # 초기 데이터 저장
        f = open('contact.csv', 'r', encoding='UTF-8')
        rdr = csv.reader(f)

        sql = INSERT INTO info(name, phone)
                        VALUES(%s, %s)

        linecount = 0

        for line in rdr:
            if linecount == 0:
                linecount = linecount + 1
            else:
                nameInput = line[0]
                phoneInput = line[1]

                # 실행하기
                cursor.execute(sql, (nameInput, phoneInput))

                # DB에 Complete 하기
                db.commit()

        f.close()

    finally:
        # DB 연결 닫기
        db.close()
    '''

    app.run(debug=True)
