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

def insert_into_db(insert_statement, table):
    try:
        mySql_insert_query = insert_statement
        mycursor.execute(mySql_insert_query)
        mydb.commit()
        print(mycursor.rowcount, f"records inserted successfully into {table} table")
        #mycursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into {} table. \nError: {}".format(table, error))
    finally:
        if mydb.is_connected():
            #mydb.close()
            #print("MySQL connection is closed")
            pass

def get_symbols_from_table():
    mycursor.execute("SELECT * FROM Symbols")
    return mycursor.fetchall()

def getContracts():
    mycursor.execute("SELECT contract_symbol, contract_id FROM Contracts")
    return mycursor.fetchall()

def main():
    # mycursor.execute("SELECT * FROM Symbols")
    # print(mycursor.fetchall())
   insert_into_db("INSERT INTO Contracts VALUES ()", "Contracts")

if __name__ == "__main__":
    main()