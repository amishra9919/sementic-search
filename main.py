import psycopg

# Real applications commonly use Python's with context manager so resources are cleaned up automatically

with psycopg.connect(
    host="localhost",
    port=5432,
    user='postgres',
    password='arpitm11814',
    dbname='sementic_search',
) as conn:
    with conn.cursor() as cursor:
        
        print('connected')