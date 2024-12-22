import psycopg2
import datetime


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
        if(table_name=="Orders"):
            column_variables.remove("payment_id")
        query_req1: str = ("%s, " * (len(column_variables) - 1))[:-2]
        col_names: str = ','.join(column_variables[1:])
        add_query = f"INSERT INTO {table_name} ({col_names}) VALUES {query_req1}"
        self.cursor.execute(add_query, values)
        try:
            self.conn.commit()
            print("Values added to table")
        except Exception as e:
            self.conn.rollback()
            print(e)

    def get_table_values(self, table_name: str) -> list:
        get_query: str = f"SELECT * FROM {table_name};"
        self.cursor.execute(get_query)
        values: list = self.cursor.fetchall()
        return values

    def most_profitable(self):
        query: str = f"SELECT * FROM calculate_most_profitable_item();"
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values

    def get_customer_id_has_unpaid_amount(self) -> list[int]:
        query: str = f"SELECT customer_id FROM get_customer_have_unpaid_amount() group by customer_id order by customer_id;"  # TODO: change to get_customer_has_unpaid_amount() in db.
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values

    def get_customers_has_unpaid_amount(self,customer_id) -> list:
        query: str = f"SELECT * FROM get_customer_have_unpaid_amount() WHERE customer_id = {customer_id} order by customer_id , order_id;"  # TODO: change to get_customer_has_unpaid_amount() in db.
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

    def check_items(self):
        query: str = f"SELECT * FROM Item;"
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values

    def sell_item(self, item_id: int, quantity: int, customer_id: int):
        self.add_to_table("Orders", [customer_id, item_id, quantity])

    def buy_item(self, supp_item_id: int, quantity: int):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.add_to_table("Inbound_Items", [supp_item_id, quantity, date])

    def payment(self, payment_id: int, paid_amount: int):
        query = f"UPDATE Payment SET Paid_Amount = Paid_Amount + {int(paid_amount)}, Pending_Amount = Pending_Amount-{int(paid_amount)} WHERE payment_id = {int(payment_id)};"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            return e

    def get_pending_amount(self, customer_id: int):
        query = f"SELECT Pending_Amount FROM Payment WHERE Customer_ID = {customer_id};"
        self.cursor.execute(query)
        values: list = self.cursor.fetchall()
        return values

    def add_customer(self, name: str, second_name: str, address: str, phone: str, email: str, image: str):
        self.add_to_table("Customer", [name, second_name, address, phone, email, image])

    def login(self, customer_id: int):
        query = f"SELECT Customer_ID FROM Customer WHERE Customer_ID = {customer_id};"
        self.cursor.execute(query)
        if self.cursor.fetchall():
            return True
        else:
            return False
