#this code needs to be executed only once just to set up our database
import mysql.connector
my_db=mysql.connector.connect(host='localhost',user='root',password='*********',port=3308)
if my_db:
    print("Connection established")
    c=my_db.cursor()#cursor object helps us do sql operations in python
    c.execute('Create database Url')
    c.execute('USE url')#to select the created database
    c.execute('Create table urls(long_url varchar(50),short_url varchar(10));')
    my_db.commit()#this is important to mention,it makes sure operations done above reflect on our workbench
else:
    print("Error Connecting")