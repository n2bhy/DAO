import pymssql

# Connect to the Sybase ASE server
conn = pymssql.connect(server='your_server', user='your_user', password='your_password')

# Create a cursor to execute SQL queries
cursor = conn.cursor()

# Query to retrieve a list of databases
cursor.execute("SELECT name FROM master..sysdatabases WHERE name NOT IN ('master', 'tempdb', 'model', 'sybsystemdb')")
databases = cursor.fetchall()

# Iterate over each database and perform the search
for db in databases:
    db_name = db[0]

    # Connect to the specific database
    conn.select_db(db_name)

    # Query to find tables with a column of type 'data'
    query = """
        SELECT t.name AS table_name, c.name AS column_name
        FROM syscolumns c
        JOIN systypes t ON c.usertype = t.usertype
        WHERE t.name = 'data' AND c.id IN (SELECT id FROM sysobjects WHERE type = 'U' AND name NOT LIKE 'sys%')
    """

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()

    # Process the results as desired
    for result in results:
        table_name = result[0]
        column_name = result[1]
        print(f"Database: {db_name}, Table: {table_name}, Column: {column_name}")

# Close the cursor and connection
cursor.close()
conn.close()
