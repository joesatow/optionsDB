import mysql.connector
from aws_jserver import GetSecret

mysql_pass = GetSecret("mysql-pass")

mydb = mysql.connector.connect(
        host="localhost",
        user="jsat",
        password=mysql_pass,
        database="options"
    )

mycursor = mydb.cursor()

def insert_into_db(insert_statement):
    try:
        mySql_insert_query = insert_statement
        mycursor.execute(mySql_insert_query)
        mydb.commit()
        print(mycursor.rowcount, "records inserted successfully into cons table")
        mycursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into cons table {}".format(error))
    finally:
        if mydb.is_connected():
            mydb.close()
            print("MySQL connection is closed")