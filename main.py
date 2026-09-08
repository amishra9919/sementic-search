import psycopg

# Real applications commonly use Python's with context manager so resources are cleaned up automatically


with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="sementic_search",
    user="arpit",
    password="arpitm11814"
) as conn :
    with conn.cursor() as cursor:
        print("Connected")
        cursor.execute("SELECT id, content FROM documents;")
        result = cursor.fetchall()
        print("result: ", result)