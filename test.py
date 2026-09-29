from database import pool

with pool.connection() as conn:
        print("connected")
