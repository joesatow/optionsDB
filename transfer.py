import mysql.connector
import pyodbc
from aws_jserver import GetSecret

mysql_pass = GetSecret("mysql-pass")


# MySQL connection details
mysql_config = {
    'host': 'localhost',
    'user': 'jsat',
    'password': mysql_pass,
    'database': 'options',
}

# MSSQL connection details
mssql_connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=lab-mssql;'
    'DATABASE=Options;'
    'UID=jserver-user;'
    'PWD=password;'
)

# Query to select data from MySQL
select_query = "SELECT symbol FROM Symbols"

# Query to insert data into MSSQL
insert_query = "INSERT INTO dbo.Symbols (symbol) VALUES (?)"

# Connect to MySQL
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Connect to MSSQL
mssql_conn = pyodbc.connect(mssql_connection_string)
mssql_cursor = mssql_conn.cursor()

# Fetch data from MySQL
mysql_cursor.execute(select_query)
rows = mysql_cursor.fetchall()

# Insert data into MSSQL
for row in rows:
    mssql_cursor.execute(insert_query, row)

# Commit and close connections
mssql_conn.commit()
mysql_cursor.close()
mysql_conn.close()
mssql_cursor.close()
mssql_conn.close()
