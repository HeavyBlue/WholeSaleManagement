import os
import threading
from database_manager import DatabaseConnection, DatabaseManager
import random
from datetime import datetime
import time

db_manager1 = DatabaseConnection()
db_manager = DatabaseManager()
conn, cursor = db_manager1.open()

def addi(table_name, path):
    with open(path, "r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            values = []
            i = i.split(",")
            for k in range(3):
                if (k == 1):
                    number = random.randint(40000, 50000)
                    values.append(number)
                else:
                    values.append(i[k])
            values.append("1")
            db_manager.add_to_table(table_name, values)


def add(table_name, path):
    with open(path, "r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            values = []
            i = i.split(",")
            for k in i[1:]:
                if (k == ""):
                    values.append("1")
                else:
                    values.append(k)
            db_manager.add_to_table(table_name, values)

def concurent_test():
    db_manager.add_to_table("Orders", ["2", "2", "50"])
    t1 = threading.Thread(target=concurent_test)
    t2 = threading.Thread(target=concurent_test)
    t1.start()
    t2.start()
    cursor.close()
    conn.close()

def add2(table_name, path):
    with open(path, "r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            time.sleep(0.1)
            values = []
            i = i.split(",")
            for k in i[1:]:
                if (k == ""):
                    number = random.randint(1, 100)
                    values.append(number)
                else:
                    if ("/" in k):
                        date_obj = datetime.strptime(k, "%m/%d/%Y")
                        k = date_obj.strftime("%Y/%m/%d")
                    values.append(k)
            db_manager.add_to_table(table_name, values)


"""folder_path = "/home/heavyblue/Desktop/dbms/WholeSaleManagement/photos/customers"

cursor.execute("SELECT customer_id FROM customer")
customer_ids = cursor.fetchall()

for ind, customer_id in enumerate(customer_ids):

    file_path = os.path.join(folder_path, os.listdir(folder_path)[ind % 10])

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        update_query = "UPDATE customer SET image = %s WHERE customer_id = %s"
        cursor.execute(update_query, (binary_data, customer_id[0]))
        conn.commit()
        print(f"Müşteri ID {customer_id[0]} için resmi güncellendi.")

cursor.close()
conn.close()
print("Tüm resimler güncellendi ve veritabanı bağlantısı kapatıldı.")"""


"""
output_folder = "/home/cihaneray/Project/WholeSaleManagement/photos/download"
os.makedirs(output_folder, exist_ok=True)

cursor.execute("SELECT customer_id, image FROM customer")
rows = cursor.fetchall()

for row in rows:
    customer_id = row[0]
    image_data = row[1]

    filename = f"customer_{customer_id}.jpg" 
    file_path = os.path.join(output_folder, filename)

    with open(file_path, 'wb') as file:
        file.write(image_data)
    print(f"Müşteri ID {customer_id} için fotoğraf {filename} olarak kaydedildi.")

cursor.close()
conn.close()
print("Tüm fotoğraflar indirildi.")"""


"""folder_path = "/home/heavyblue/Desktop/dbms/WholeSaleManagement/photos/items"

cursor.execute("SELECT item_id FROM item")
item_ids = cursor.fetchall()

for ind, item_id in enumerate(item_ids):

    file_path = os.path.join(folder_path, os.listdir(folder_path)[ind % 9])

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        update_query = "UPDATE item SET image = %s WHERE item_id = %s"
        cursor.execute(update_query, (binary_data, item_id[0]))
        conn.commit()
        print(f"Item ID {item_id[0]} için resmi güncellendi.")

cursor.close()
conn.close()
print("Tüm resimler güncellendi ve veritabanı bağlantısı kapatıldı.")"""