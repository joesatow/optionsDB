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

def getSymbols():
    mycursor.execute("SELECT * FROM Symbols")
    return mycursor.fetchall()


def main():
    # test_statement = """
    # INSERT IGNORE INTO Contracts (symbol_id, contract_symbol, description, call_put, strike_price, exp_date) 
    # VALUES 
    # ('1', 'aapl2311sd30150c', 'aapl 150c sdfs', 'CALL', 150.00, '2023-11-28'), 
    # ('1', 'aapl231130154c', 'aapl 150c sdfs', 'CALL', 150.00, '2023-11-28'), 
    # ('1', 'aapl23113d0150c', 'aapl 150c sdfs', 'CALL', 150.00, '2023-11-28');
    # """
    # insert_into_db(test_statement)
    mycursor.execute("SELECT * FROM Symbols")
    print(mycursor.fetchall())

if __name__ == "__main__":
    main()