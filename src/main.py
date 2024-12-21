import psycopg2

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM test1;")
    x = cursor.fetchall()
    close_db(conn, cursor)
    return str(x)

def connect_db():
    with open('../credential.txt', 'r') as f:
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
    #cursor.execute("SELECT * FROM test1 LIMIT 0;")
    #colname = [desc[0] for desc in cursor.description]
    #query = f"INSERT INTO test1 ({", ".join(colname[1:])}) VALUES ({("%s, " * (len(colname) - 1))[:-2]});"
    #print(query)
    #cursor.execute(query, ("test1".strip(), "11010101", "15"))
    #conn.commit()
    cursor.execute("SELECT * FROM test1;")

    close_db(conn, cursor)

if __name__ == "__main__":
    app.run(debug=True)
