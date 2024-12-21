import psycopg2

def connect_db():
    with open('credential.txt', 'r') as f:
        f = f.read()
        credential: list = f.split('\n')
    conn = psycopg2.connect(
        dbname=credential[0],
        user=credential[1],
        password=credential[2],
        host=credential[3],
        port=credential[4])

    cursor = conn.cursor()
    return conn, cursor

def close_db(conn, cursor):
    cursor.close()
    conn.close()

def main():
    conn, cursor = connect_db()
    print("Connected to database")
    close_db(conn, cursor)

if __name__ == "__main__":
    main()