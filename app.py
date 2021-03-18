from flask import Flask,request,render_template,redirect
#pip3 install flask-mysqldb
from flask_mysqldb import MySQL

import sys

app=Flask(__name__)

#configuring db
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='*********'
app.config['MYSQL_DB']='url'
app.config['MYSQL_PORT']=3308

mysql=MySQL(app)#sending our app db configuration to mysql

counter=4000
#counter is used to send a numeric value to our b62 algo to get back a unique combination,i.e. short url


#method for encoding our long url
def conv(num):
    BASE_ALPH = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    BASE_LEN = len(BASE_ALPH)
    if not num:
        return BASE_ALPH[0]

    encoding = ""
    while num:
        num, rem = divmod(num, BASE_LEN)
        encoding = BASE_ALPH[rem] + encoding
    return encoding

@app.route('/', methods=['POST','GET'])
def home():
    global counter
    if request.method=='POST':
        #fetching form data
        url_received=request.form['fullurl']
        cur=mysql.connection.cursor()
        shrt=conv(counter)#passing counter for each long_url entered
        counter+=1
        #now to store both short and long url in our db
        cur.execute("INSERT INTO urls(long_url,short_url) VALUES(%s,%s)",(url_received,shrt))
        mysql.connection.commit()
        cur.close()
        return render_template('result.html',long_url=url_received,short_url=shrt)
    else:
        return render_template('home.html')

#the route to get redirected to long url page
@app.route('/<short_url>')
def result(short_url):#when user enter shrt url as localhost:<port>/<shrt_url>,this method receives it as parameter
    short_url=str(short_url)
    cur=mysql.connection.cursor()#creating cursor to search for the shrt url in MySql
    result=cur.execute(f"SELECT long_url FROM url.urls where short_url='{short_url}' limit 1")
    if result>0:
        long_url=cur.fetchone()#but it will return a tuple,so we loop through the tuple once
        for i in long_url:
            return redirect(i)
            
    mysql.connection.commit()
    cur.close()


@app.route('/all-urls')
def urls():
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT * FROM urls")#this will return all the rows not the data in it
    if result>0:
        urls=cur.fetchall()
        return render_template('table.html',urls=urls)#we will loop through the tuple on our html template
    else:
        return render_template('table.html')

port=5000#This will be our default port
if __name__=='__main__':
    if sys.argv.__len__()>1:#incase we want to run multiple instances of our server on different ports
        port=sys.argv[1]
    app.run(port=port,debug=True)
