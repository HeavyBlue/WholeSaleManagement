import psycopg2


class DatabaseConnection:
    def __init__(self):
        with open('../credential.txt', 'r') as f:
            f = f.read()
            credential: list = f.split('\n')

        self.conn = psycopg2.connect(
            dbname=credential[0],
            user=credential[1],
            password=credential[2],
            host=credential[3],
            port=credential[4]
        )
        self.cursor = self.conn.cursor()

    def open(self):
        return self.conn, self.cursor

    def close(self):
        self.cursor.close()
        self.conn.close()


class DatabaseManager:
    def __init__(self):
        self.conn, self.cursor = DatabaseConnection().open()

    def get_table_column_name(self, table_name: str) -> list:
        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 0;")
        column_variables: list = [desc[0] for desc in self.cursor.description]
        return column_variables

    def add_to_table(self, table_name: str, values: list):
        column_variables = self.get_table_column_name(table_name)
        query_req1: str = ("%s, " * (len(column_variables) - 1))[:-2]
        col_names: str = ','.join(column_variables[1:])
        add_query = f"INSERT INTO `{table_name}` ({col_names}) VALUES {query_req1}"
        self.cursor.execute(add_query, values)
        try:
            self.conn.commit()
            print("Values added to table")
        except Exception as e:
            print(e)

    def get_table_values(self, table_name: str) -> list:
        get_query: str = f"SELECT * FROM `{table_name}`;"
        self.cursor.execute(get_query)
        values: list = self.cursor.fetchall()
        return values
    def most_profitable(self):
        query: str = f"SELECT * FROM calculate_monthly_profit();"
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values
    def check_customer_debts(self):
        query: str = f"SELECT * FROM show_customers_whose_debts_are_past_due();"
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values
    def monthly_profit(self):
        query: str = f"SELECT * FROM calculate_monthly_profit();"
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values

