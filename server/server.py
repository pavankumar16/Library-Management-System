# server.py
from flask import Flask, render_template
from flask import jsonify
from flask import request
import mysql.connector
import errorCodes
import json
import datetime


app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

#enter your username and password
cnx = mysql.connector.connect(user='root', password='password',database='lms',charset='utf8')
cursor = cnx.cursor(buffered=True)



@app.route('/', defaults={'path': ''},methods=['POST','GET'])
@app.route('/<path:path>')
def index(path):
    if request.method == 'POST':
        if not request.form['user'] or not request.form['password']:
            return render_template('home.html')
        if request.form['user'] != 'admin':
            return render_template('home.html')
        elif request.form['password'] != 'admin':
            return render_template('home.html')
    return render_template("index.html")

@app.route('/home',methods=['POST','GET'])
def display():
	return render_template("home.html")

@app.route("/addBorrower",methods=['GET', 'POST'])
def addBorrower():
    data = request.get_json(force=True)
    query = "select count(card_id) + 1 from borrower;"
    prefix = 'ID'
    cursor.execute(query)
    row = cursor.fetchone()
    temp = str(row[0])
    card_id_temp = ''
    for i in range(len(temp),6):
        card_id_temp = card_id_temp + '0'
    card_id = prefix+card_id_temp+temp
    query = "INSERT into BORROWER(card_id,ssn,bname,address,phone) values(%s,%s,%s,%s,%s)"
    response = None
    try:
        cursor.execute(query,(card_id,data["ssn"],data["name"],data["address"],data["phone"]))
        response = {'message':"New Borrower Created with ID:"+card_id,'success':True}
        cnx.commit()
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'message':'Borrower Creation failed','success':False}
    return jsonify(response)

@app.route("/searchBook",methods=['GET', 'POST'])
def searchBook():
    data = request.get_json(force=True)
    searchQuery = data["searchQuery"]
    searchResult = []
    query1 = 'select b.ISBN from Book b left outer join BOOK_AUTHORS ba on b.isbn = ba.isbn left outer join authors a on ba.author_id = a.author_id where b.isbn like %s or b.title like %s or a.name like %s'
    #query1 = 'select ISBN from Books where isbn like %s or title like %s or author like %s'

    ISBNList = []
    try:
        cursor.execute(query1,("%"+searchQuery+"%","%"+searchQuery+"%","%"+searchQuery+"%"))
        for row in cursor:
            type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            ISBNList.append(type_fixed_row[0])
        if(len(ISBNList)>0):
            ISBN = list(set(ISBNList))
            format_strings = '('+','.join(['%s'] * len(ISBN))+')'
            query2 = 'select b.ISBN,b.Title,GROUP_CONCAT(a.name),b.isCheckedOut from Book b left outer join BOOK_AUTHORS ba on b.isbn = ba.isbn left outer join authors a on ba.author_id = a.author_id where b.isbn IN ' + format_strings + ' group by b.isbn'
            #query2 = 'select ISBN,title,author from Books where isbn IN ' + format_strings + ' group by isbn'
            cursor.execute(query2,tuple(ISBN))
            for row in cursor:
                type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row])
                searchResult.append(type_fixed_row)
            response = {'searchResult':searchResult,'message':'search success','success':True}
        else:
            response = {'searchResult':None,'message':'search success','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'searchResult':None,'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'searchResult':None,'message':'search failed','success':False}
    return jsonify(response)

@app.route("/checkoutBook",methods=['GET', 'POST'])
def checkoutBook():
    data = request.get_json(force=True)
    cardId = data["borrowerId"]
    isbn = data["isbn"]
    response = None
    try:
        query = 'select 1 from BORROWER where card_id = %s'
        cursor.execute(query,(cardId,))
        isBorrower = 0
        for row in cursor:
            isBorrower = row[0]
        if(isBorrower):
            query = 'select isCheckedOut from BOOK where isbn = %s'
            isCheckedOut = 1
            cursor.execute(query,(isbn,))
            for row in cursor:
                isCheckedOut = row[0]
            query = 'select count(*) >= 3 from BOOK_LOANS where card_id = %s and date_in is null'
            isCountExceeded = 1
            cursor.execute(query,(cardId,))
            for row in cursor:
                isCountExceeded = row[0]
                app.logger.info("%s is the count",isCountExceeded)
            if(isCheckedOut):
                response = {'message':'Book already issued','success':False}
            elif(isCountExceeded):
                response = {'message':'Maximum limit of 3 reached. You cannot issue.','success':False}
            else:
                query1 = 'Insert into BOOK_LOANS values(0,%s,%s,%s,%s,null)'
                query2 = 'update BOOK set isCheckedOut = True where isbn = %s'
                dateOut = datetime.date.today() - datetime.timedelta(days=25)
                dueDate = dateOut + datetime.timedelta(days=14)
                app.logger.info("before q1")
                cursor.execute(query1,(isbn,cardId,dateOut,dueDate))
                app.logger.info("execited q1")
                cursor.execute(query2,(isbn,))
                app.logger.info("execited q2")
                cnx.commit()
                response = {'message':'Book Issued. ','success':True}
        else:
            response = {'message':'Invalid Library Id','success':False}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'message':'Borrower Creation failed','success':False}
    return jsonify(response)

@app.route("/searchBookLoan",methods=['GET', 'POST'])
def searchBookLoan():
    data = request.get_json(force=True)
    searchQuery = data["searchQuery"]
    searchResult = []
    query = 'select bl.loan_id,bl.isbn,bl.card_id,b.bname,bl.date_out,bl.due_date from BOOK_LOANS bl join BORROWER b on bl.card_id = b.card_id where (bl.isbn like %s or bl.card_id like %s or b.bname like %s) and date_in is null'
    try:
        cursor.execute(query,("%"+searchQuery+"%","%"+searchQuery+"%","%"+searchQuery+"%"))
        for row in cursor:
            type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            searchResult.append(type_fixed_row)
        response = {'searchResult':searchResult,'message':'search success','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'searchResult':None,'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'searchResult':None,'message':'searchFailed','success':False}
    return jsonify(response)


@app.route("/searchHistory",methods=['GET', 'POST'])
def searchHistory():
    data = request.get_json(force=True)
    searchQuery = data["searchQuery"]
    searchResult = []
    query = 'select bb.isbn, bb.title, bi.tag,bi.avgrating from BOOK_LOANS bl join BORROWER b on bl.card_id = b.card_id join BOOK bb on bb.isbn = bl.isbn join bookinfo bi on bi.isbn = bb.isbn where (bl.isbn like %s or bl.card_id like %s or b.bname like %s)'
    try:
        cursor.execute(query,("%"+searchQuery+"%","%"+searchQuery+"%","%"+searchQuery+"%"))
        for row in cursor:
            type_fixed_row = list([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            type_fixed_row[3]=str(type_fixed_row[3])
            searchResult.append(type_fixed_row)
        response = {'searchResult':searchResult,'message':'search success','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'searchResult':None,'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'searchResult':None,'message':str(err),'success':False}
    return jsonify(response)


@app.route("/getRecommendation",methods=['GET', 'POST'])
def getRecommendation():
    data = request.get_json(force=True)
    searchQuery = data["searchQuery"]
    searchResult = []

    query = 'select bb.isbn, bb.title, bi.tag,bi.avgrating from BOOK_LOANS bl join BORROWER b on bl.card_id = b.card_id join BOOK bb on bb.isbn = bl.isbn join bookinfo bi on bi.isbn = bb.isbn where (bl.isbn like %s or bl.card_id like %s or b.bname like %s)'
    try:
        cursor.execute(query,("%"+searchQuery+"%","%"+searchQuery+"%","%"+searchQuery+"%"))
        copy=cursor
        d={}
        for row in copy:
            #type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            #app.logger.info("the vale here is %s",type_fixed_row)
            #now each row gives previous books of the user
            type_fixed_row = list([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            type_fixed_row[3]=str(type_fixed_row[3])

            if(type_fixed_row[2] not in d):
                d[type_fixed_row[2]]=0
            d[type_fixed_row[2]]+=float(type_fixed_row[3])

        mvalue = 0
        app.logger.info("Dictionary value: %s",d)
        mkey = ""
        for key,value in d.items():
            if(value>mvalue):
                mvalue=value
                mkey=key

        #ldic = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        query4 = "SELECT B.ISBN,B.TITLE,BI.TAG,BI.AVGRATING FROM LMS.BOOK B JOIN LMS.BOOKINFO BI ON B.ISBN = BI.ISBN WHERE BI.TAG = '"+mkey+"' AND BI.AVGRATING>=4.5 order by RAND() limit 1"
        cursor.execute(query4)
        for row in cursor:
            onemorerow = list([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            onemorerow[3]=str(onemorerow[3])
            app.logger.info("how the final search result looks like %s",onemorerow)
            searchResult.append(onemorerow)
    
        response = {'searchResult':searchResult,'message':'search success','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'searchResult':None,'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'searchResult':None,'message':str(err),'success':False}
    return jsonify(response)


@app.route("/checkinBook",methods=['GET', 'POST'])
def checkinBook():
    data = request.get_json(force=True)
    loanId = data["loanId"]
    response = None
    format_strings = ','.join(['%s'] * len(loanId))
    query1 = 'update BOOK_LOANS set date_in = curdate() where loan_id in (%s)'
    query2 = 'update BOOK set isCheckedOut = False where isbn in (select isbn from BOOK_LOANS where loan_id in (%s))'
    try:
        cursor.execute(query1%format_strings,tuple(loanId))
        cursor.execute(query2%format_strings,tuple(loanId))
        cnx.commit()
        response = {'message':'Book Checked In','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'message':'Book Check In fail','success':False}
    return jsonify(response)

@app.route("/calculateFines",methods=['GET', 'POST'])
def calculateFines():
    response = None
    query = 'select loan_id,due_date,date_in from BOOK_LOANS where date_in > due_date or curdate() > due_date'
    cursor.execute(query)
    today = datetime.datetime.today()
    rows = cursor.fetchall()
    resultSet = []
    for row in rows:
        if(row[2] == None):
            diff = today - row[1]
            fine = round(diff.days * 2,2)
        else:
            diff = row[2] - row[1]
            fine = round(diff.days * 2,2)
        try:
            query = 'Insert into fines values(%s,%s,%s)'
            cursor.execute(query,(row[0],fine,False))
            cnx.commit()
            response = {'message':'fines updated','success':True}
        except mysql.connector.Error as err:
            if(err.errno in errorCodes.errorCodeMessage):
                if(err.errno==1062):
                    query = 'update fines set fine_amt = %s where loan_id = %s and paid = false'
                    cursor.execute(query,(fine,row[0]))
                    cnx.commit()
                    response = {'message':'fines updated','success':True}
                else:
                    response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
            else:
                response = {'message':'Fine calculation failed','success':False}
    return jsonify(response)

@app.route("/fetchFines",methods=['GET','POST'])
def fetchFines():
    resultSet = []
    try:
        query = 'select b.card_id,b.bname,SUM(f.fine_amt) from fines f join book_loans bl on f.Loan_id = bl.Loan_id join borrower b on bl.card_id = b.Card_id where f.paid=false group by bl.Card_id'
        cursor.execute(query)
        rows = cursor.fetchall()
        resultSet = []
        childMap = {}
        for row in rows:
            query = 'select bl.loan_id,bl.isbn,f.fine_amt,bl.date_in from fines f join book_loans bl on f.Loan_id = bl.Loan_id join borrower b on bl.card_id = b.Card_id where f.paid=false and b.card_id=%s'
            cardId = row[0]
            cursor.execute(query,(cardId,))
            childSet = []
            for row1 in cursor:
                type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row1])
                childSet.append(type_fixed_row)
            childMap[cardId] = childSet
            type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row])
            resultSet.append(type_fixed_row)
        response = {'aggregateData':resultSet,'finesDataForCardId':childMap, 'message':'fines update','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'message':'Fines update failed','success':False}
    return jsonify(response)

@app.route("/settleFines",methods=['GET', 'POST'])
def settleFines():
    data = request.get_json(force=True)
    loanId = data["loanId"]
    response = None
    format_strings = ','.join(['%s'] * len(loanId))
    query = 'update fines set paid = true where loan_id in (%s)'
    try:
        cursor.execute(query%format_strings,tuple(loanId))
        cnx.commit()
        response = {'message':'fine settled','success':True}
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
        else:
            response = {'message':'Fine settlement failed','success':False}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
