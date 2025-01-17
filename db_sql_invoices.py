import sqlite3

db_file = 'data.db'
connection = sqlite3.connect(db_file)

cursor = connection.cursor()

query = """
    SELECT *FROM 'invoices' WHERE BillingCountry = 'Germany' AND Total >= 2.0 ORDER BY Total Asc LIMIT 0,30    
        
"""

cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
      print(f'Customer ID: {row[1]}')

connection.close()

