import pyodbc

# Define your database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=lab-mssql;'
    'DATABASE=Options;'
    'UID=jserver-user;'
    'PWD=password'
)
cursor = conn.cursor()

# SQL insert statement
sql = """
INSERT INTO OptionContracts (symbol_id, contract_symbol, description, call_put, strike_price, exp_date)
VALUES (?, ?, ?, ?, ?, ?)
"""

def insert_into_mssql(contract_list):
    # Insert data
    for contract in contract_list:
        cursor.execute(sql, contract['symbol_id'], contract['symbol'], contract['description'], contract['putCall'], contract['strikePrice'], contract['exp_date'])

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
