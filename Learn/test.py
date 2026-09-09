import psycopg


with psycopg.connect("dbname=sementic_search user=arpit") as conn:
    print("Connected")
    with conn.cursor() as cursor:
        # table_data = cursor.execute('SELECT * from documents;')
        # result = table_data.fetchall()
        row = cursor.execute("""INSERT INTO documents(content)
                           VALUES('My self Arpit and i am AI Develooper');""")
        result = row.fetchall()
        print("result: ", result)
    # conn.commit()